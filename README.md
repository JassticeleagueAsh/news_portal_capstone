# News Portal Capstone

## Project Overview

This project is a Django-based News Portal web application developed as part of a capstone assignment.

The system supports multiple user roles with role-based permissions and allows for content creation, moderation, subscriptions, and API access.

The project can be run either using a local Python virtual environment or Docker, making it easy to set up and run on different machines.

---

## User Roles

* Reader
* Journalist
* Editor
* Publisher

Each role has specific permissions that control access and actions in the application.

---

## Core Features

### Authentication and User Management

* User registration and login
* Custom user model
* Role selection during registration
* Role-based redirects after login

### Reader

* View approved articles only
* View newsletters
* Subscribe to journalists and publishers

### Journalist

* Create, update, and delete articles
* Create, update, and delete newsletters
* Submit articles for editor approval

### Editor

* Approve and manage articles
* Manage newsletters
* Create publishers

### Publisher

* Represents publishing entities
* Linked to articles

---

## API Functionality

Built using Django REST Framework.

### Public Endpoints

* GET /api/articles/
* GET /api/articles/<id>/

### Protected Endpoints

* GET /api/articles/subscribed/
* POST /api/articles/create/
* PUT /api/articles/<id>/update/
* DELETE /api/articles/<id>/delete/

---

## API Authentication

Token-based authentication is implemented.

### Get a Token

POST /api/token/

Request body:

{
"username": "your_username",
"password": "your_password"
}

### Use the Token

Authorization: Token your_token

---

## Technologies Used

* Python
* Django
* Django REST Framework
* MariaDB
* mysqlclient
* Bootstrap 5
* Docker
* Sphinx

---

## Project Structure

news_portal_capstone/
├── core/
├── news_portal/
├── planning/
├── static/
├── templates/
├── docs/
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── requirements.txt
├── manage.py
└── README.md

---

## Database Setup (MariaDB)

This project uses MariaDB as the primary database.

### Step 1: Open MariaDB / MySQL

mysql -u root -p

### Step 2: Create the Database

CREATE DATABASE news_portal_db;

---

## Environment Variables

### Step 1: Copy the Example File

copy .env.example .env

### Step 2: Update .env

DB_NAME=news_portal_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=3306
SECRET_KEY=your_secret_key
DEBUG=True
SPHINX_BUILD=False

---

## Running the Project

### Option 1: Virtual Environment (venv)

git clone https://github.com/JassticeleagueAsh/news_portal_capstone.git
cd news_portal_capstone

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver

Open in browser:
http://127.0.0.1:8000/

---

### Option 2: Docker

Docker support is included in this project to provide a consistent and portable environment.

#### What Docker is used for

* Containerises the Django application
* Ensures consistent setup across different machines
* Simplifies running the project without manual environment setup

#### Before running Docker

* Make sure Docker Desktop is installed
* Ensure Docker Desktop is running
* Navigate to the project root folder (where Dockerfile is located)

#### Run the project with Docker

cd news_portal_capstone
docker-compose up --build

Once running, open:
http://127.0.0.1:8000/

#### Stop Docker

Press Ctrl + C, then run:

docker-compose down

---

## Running Tests

python manage.py test

---

## Sphinx Documentation

cd docs
.\make.bat clean
.\make.bat html

Open:
docs_build\html\index.html

---

## Key Concepts Demonstrated

* Role-based access control
* Django ORM relationships
* REST API development
* Token authentication
* Docker containerisation
* Sphinx documentation
* Environment-based configuration

---

## Notes

* Sensitive data is not committed to the repository
* Use .env.example to configure your environment
* SPHINX_BUILD=True can be used to bypass database during documentation builds

---

## Author

Ashwin Jass

---

## Repository

https://github.com/JassticeleagueAsh/news_portal_capstone
