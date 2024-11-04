# SmartSuite APIs

This SmartSuite application provides a comprehensive API for managing a school or university system. It supports various user roles, each with specific permissions and capabilities, allowing for efficient management of students, teachers, departments, courses, batches, and subjects.

## Table of Contents
- Features
- Installation
- Configuration
- Usage
- Contributing
- License


## Features

1. User Roles and Permissions.

### Super Admin:
Full CRUD (Create, Read, Update, Delete) capabilities for:
- Students
- Teachers
- Departments
- Courses
- Batches
- Subjects
- Teacher

CRUD operations for:
- Subject Files
- Summaries
- Keypoints
- Quizzes
- Student

Access to:
- Subject Files (Read-only)
- Summaries (Read-only)
- Keypoints (Read-only)
- Quizzes (Take quizzes)


2. Robust API Endpoints
Designed using Django Rest Framework (DRF) for a RESTful API structure.
Secure and efficient handling of user data.
Token-based authentication for API access control.


3. Modular Design
Organized codebase with separation of concerns for easier maintenance and scalability.
Reusable components and services.
Installation


To run this Django application locally, follow the steps below:

Clone the Repository
```
git clone https://github.com/M-Shariq-546/SmartSuiteBackend.git
cd smartsuite
```

Create a Virtual Environment
```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```


Install Dependencies
```
pip install -r requirements.txt
```

Run Makemigrations
```
python manage.py makemigrations
```

Run Migrations
```
python manage.py migrate
```

Create a Superuser
```
python manage.py createsuperuser
```

Run the Development Server
```
python manage.py runserver
```

Access the Application

Open your browser and go to http://127.0.0.1:8000/.

Configuration
Ensure to configure your settings.py file for database settings, static files, and any third-party services used in the application.

Environment Variables
Use a .env file to securely store sensitive data like database credentials, secret keys, etc.

## Usage:
### Super Admin

CRUD Operations: Manage all aspects of the system, including users, departments, and academic content.
Teacher
Content Management: Create, update, and delete content related to subjects, such as files, summaries, keypoints, and quizzes.
Student
Learning and Assessment: Access learning materials and take quizzes to assess understanding.
API Documentation
This application uses Postman for API testing and documentation. To test the API endpoints, follow the steps below:


Fork the repository.
Create a new branch for your feature or bug fix.
Commit your changes.
Push the branch to your forked repository.
Open a pull request against the main branch.
License
This project is licensed under the MIT License. See the LICENSE file for details.
