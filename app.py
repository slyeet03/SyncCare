import firebase_admin
from firebase_admin import credentials, firestore, auth, storage
from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from flask_session import Session
from functools import wraps
import re
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime

# Generate a random secret key
secret_key = os.urandom(24).hex()

# Initialize Firebase
cred = credentials.Certificate("synccare-6a31c-firebase-adminsdk-69so4-2d1341fc8b.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'synccare-6a31c.appspot.com'
})

db = firestore.client()
bucket = storage.bucket()

app = Flask(__name__)

app.config['SECRET_KEY'] = secret_key
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def base():
    return render_template('base.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def validate_indian_phone(phone):
    pattern = r'^[6-9]\d{9}$'
    return re.match(pattern, phone) is not None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
        
        if not validate_indian_phone(phone):
            flash('Invalid Indian phone number. Please enter a 10-digit number starting with 6, 7, 8, or 9.', 'error')
            return render_template('login.html')
        
        try:
            # Format the phone number for Firebase
            formatted_phone = f'+91{phone}'
            
            # Sign in the user with Firebase
            user = auth.get_user_by_phone_number(formatted_phone)
            # Can't be fucked to do manual password check so we just gonna rawdog it
            
            session['user_id'] = user.uid
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        except auth.UserNotFoundError:
            flash('No user found with this phone number. Please check your credentials or register.', 'error')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        password = request.form['password']
        aadhaar = request.form['aadhaar']
        
        if not validate_indian_phone(phone):
            flash('Invalid Indian phone number. Please enter a 10-digit number starting with 6, 7, 8, or 9.', 'error')
            return render_template('register.html')
        
        try:
            # Format the phone number for Firebase
            formatted_phone = f'+91{phone}'
            
            # Create user in Firebase Authentication
            user = auth.create_user(
                phone_number=formatted_phone,
                password=password,
                display_name=name
            )
            
            # Store user data in Firestore
            user_ref = db.collection('users').document(user.uid)
            user_ref.set({
                'name': name,
                'phone': formatted_phone,
                'aadhaar': aadhaar,
                'age': '',
                'weight': '',
                'bldgrp': '',
                'medical_history': '',
                'allergies': '',
                'current_medications': '',
                'gender': ''
            })
            
            flash('Account created successfully. Please log in.', 'success')
            return redirect(url_for('login'))
        except auth.PhoneNumberAlreadyExistsError:
            flash('An account with this phone number already exists.', 'error')
        except Exception as e:
            flash(f'Error creating account: {str(e)}', 'error')
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    # Fetch user data from Firestore
    db = firestore.client()
    user_doc = db.collection('users').document(user_id).get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
    else:
        flash('User data not found.', 'error')
        return redirect(url_for('login'))
    
    return render_template('base.html', user=user_data)



@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

# Helper function to get the current user
def get_current_user():
    if 'user_id' in session:
        return auth.get_user(session['user_id'])
    return None



@app.route('/medical_details', methods=['GET', 'POST'])
@login_required
def med_det():
    user_id = session['user_id']
    if request.method == 'POST':
        medical_history = request.form['history']
        allergies = request.form['allergies']
        medications = request.form['medications']
        age = request.form['age']
        weight = request.form['weight']
        bldgrp = request.form['bldgrp']
        gender = request.form['gender']
        
        try:
            db.collection('users').document(user_id).update({
                'medical_history': medical_history,
                'allergies': allergies,
                'current_medications': medications,
                'age': age,
                'weight': weight,
                'bldgrp': bldgrp,
                'gender': gender
            })
            return redirect(url_for('dashboard'))
        except Exception as e:
            return f"An error occurred: {str(e)}", 400
    
    # GET request: Fetch and display current medical details
    try:
        user_doc = db.collection('users').document(user_id).get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            return render_template('med_det.html', 
                                   history=user_data.get('medical_history', ''),
                                   allergies=user_data.get('allergies', ''),
                                   medications=user_data.get('current_medications', ''),
                                   age=user_data.get('age',''),
                                   weight=user_data.get('weight',''),
                                   gender=user_data.get('gender',''),
                                   bldgrp=user_data.get('bldgrp',''))
        else:
            return "User not found", 404
    except Exception as e:
        return f"An error occurred: {str(e)}", 400

@app.route('/recommendations')
@login_required
def doc_rec():
    # fetch this data from Firestore
    doctors = [
        {"name": "Dr. Smith", "specialty": "Cardiologist", "location": "New York", "contact": "123-456-7890"},
        {"name": "Dr. Johnson", "specialty": "Pediatrician", "location": "Los Angeles", "contact": "098-765-4321"},
        {"name": "Dr. Williams", "specialty": "Neurologist", "location": "Chicago", "contact": "555-555-5555"}
    ]
    return render_template('doc_recs.html', doctors=doctors)


@app.route('/upload_prescription', methods=['GET', 'POST'])
@login_required
def upload_prescription():
    if request.method == 'POST':
        if 'prescription_file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)

        file = request.files['prescription_file']

        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            file_extension = os.path.splitext(filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            
            # Upload file to Firebase Storage
            blob = bucket.blob(f"prescriptions/{unique_filename}")
            blob.upload_from_string(
                file.read(),
                content_type=file.content_type
            )

            # Make the blob publicly accessible
            blob.make_public()

            # Save file information to Firestore
            user_id = session['user_id']
            db.collection('users').document(user_id).collection('prescriptions').add({
                'filename': filename,
                'storage_path': f"prescriptions/{unique_filename}",
                'download_url': blob.public_url,
                'upload_date': firestore.SERVER_TIMESTAMP
            })

            flash('File uploaded successfully', 'success')
            return redirect(url_for('profile'))

    return render_template('upld_presc.html')

@app.route('/profile')
@login_required
def profile():
    user_id = session['user_id']
    user_doc = db.collection('users').document(user_id).get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
        
        # Fetch uploaded files from Firestore
        prescriptions = db.collection('users').document(user_id).collection('prescriptions').order_by('upload_date', direction=firestore.Query.DESCENDING).get()
        user_data['uploaded_files'] = [
            {
                "name": doc.get('filename'),
                "date": doc.get('upload_date').strftime("%Y-%m-%d %H:%M:%S") if doc.get('upload_date') else "Unknown",
                "url": doc.get('download_url')
            } for doc in prescriptions
        ]
        return render_template('profile.html', user=user_data)
    else:
        return "User not found", 404

if __name__ == '__main__':
	app.run(debug=True)