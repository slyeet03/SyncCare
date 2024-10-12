# SyncCare

SyncCare is a web application designed to simplify medical management by synchronizing medical details, making it easier for users to manage their health records, medications, and doctor recommendations. The platform allows users to create an account, upload medical prescriptions, and order medicines and services, all while keeping their data securely stored and synchronized using Firebase.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Account Creation and Authentication**: Users can sign up using their phone number and Aadhaar. Firebase Authentication ensures secure login and session management.
- **Medical History Management**: Users can store and update their medical history, including allergies, current medications, and more.
- **Doctor Recommendations**: Based on the user’s medical history, SyncCare suggests appropriate doctors.
- **Medicine and Service Management**: Users can order medicines or request home services from compounders.
- **Prescription Upload**: Upload and store digital copies of prescriptions for future reference and doctor access.

## Tech Stack
- **Frontend**: 
  - HTML (for web page structure)
  - CSS (for styling and responsiveness)
  
- **Backend**: 
  - Flask (Python framework for routing and handling backend logic)

- **Authentication and Database**:
  - Firebase Authentication (for user login and session management)
  - Firebase Firestore (for storing user details, prescriptions, and doctor recommendations)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/SyncCare.git
    ```
   
2. Navigate to the project directory:
    ```bash
    cd SyncCare
    ```

3. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

5. Set up Firebase:
    - Obtain the Firebase Admin SDK private key (`.json` file) from your Firebase project settings.
    - Place it in the root of the project and name it `synccare-firebase-adminsdk.json`.

6. Run the Flask application:
    ```bash
    flask run
    ```

7. Visit `http://127.0.0.1:5000` in your browser.

## Usage

### User Flow:
- Register for an account by entering your name, phone number, Aadhaar, and other details.
- Once logged in, you can:
  - View or update your **medical details**.
  - Get **doctor recommendations** based on your medical history.
  - **Upload prescriptions** to make them accessible for doctors and yourself.
  - **Order medications** or request a compounder to visit your home.

### Key Pages:
- **/register**: Sign-up page for new users.
- **/login**: Login page for existing users.
- **/dashboard**: User dashboard with access to medical details, doctor recommendations, and uploaded prescriptions.
- **/medical_details**: Page for managing and updating medical history.
- **/upload_prescription**: Page to upload prescription files.
- **/recommendations**: Page showing doctor recommendations.

## Contributing
This project was developed as part of a hackathon. While it's not actively maintained, contributions, suggestions, and feedback are welcome. Please open an issue or submit a pull request if you'd like to contribute.

## Contributors

This project was developed by the team "We Can't Code" during the MUJ Hacks 9.0. The team members are:

- [bhavya nanda](https://www.linkedin.com/in/angeline-d’souza-a297992b8?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app)
- [slyeet03](https://github.com/slyeet03)
- [rudracodess](https://github.com/rudracodess)
- [angeline](https://www.linkedin.com/in/bhavya-nanda-567840309)
