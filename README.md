# News Portal Capstone

## Project Overview

This project is a Django-based News Portal web application developed as
part of a capstone assignment.

The system supports multiple user roles with role-based permissions and
allows for content creation, moderation, subscriptions, and API access.

---

## User Roles

* Reader
* Journalist
* Editor
* Publisher

Each role has specific permissions that control access and actions in
the application.

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

* `GET /api/articles/`
* `GET /api/articles/<id>/`

### Protected Endpoints

* `GET /api/articles/subscribed/`
* `POST /api/articles/create/`
* `PUT /api/articles/<id>/update/`
* `DELETE /api/articles/<id>/delete/`

---

## API Authentication

Token-based authentication is implemented.

### Get a Token

```bash
POST /api/token/
```

Request body:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

### Use the Token

```bash
Authorization: Token your_token
```

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

```text
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
```

---

## Database Setup (MariaDB)

This project uses MariaDB as the primary database.

### Step 1: Open MariaDB / MySQL

```bash
mysql -u root -p
```

Enter your password when prompted.

### Step 2: Create the Database

```sql
CREATE DATABASE news_portal_db;
```

---

## Environment Variables

### Step 1: Copy the Example File

```bash
copy .env.example .env
```

### Step 2: Update `.env`

```env
DB_NAME=news_portal_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=3306
SECRET_KEY=your_secret_key
DEBUG=True
SPHINX_BUILD=False
```

---

## Running the Project

### Option 1: Virtual Environment (venv)

```bash
git clone https://github.com/JassticeleagueAsh/news_portal_capstone.git
cd news_portal_capstone

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

---

### Option 2: Docker

Ensure Docker Desktop is running.

```bash
cd news_portal_capstone
docker-compose up --build
```

Open:

```
http://127.0.0.1:8000/
```

Stop:

```bash
docker-compose down
```

---

## Running Tests

```bash
python manage.py test
```

---

## Sphinx Documentation

```bash
cd docs
.\make.bat clean
.\make.bat html
```

Open:

```
docs\_build\html\index.html
```

---

## Key Concepts Demonstrated

* Role-based access control
* Django ORM relationships
* REST API development
* Token authentication
* Docker containerization
* Sphinx documentation
* Environment-based configuration

---

## Notes

* Sensitive data is not committed to the repository
* Use `.env.example` to configure your environment
* Sphinx uses `SPHINX_BUILD=True` to bypass MySQL during doc builds

---

## Author

Ashwin Jass

---

## Repository

https://github.com/JassticeleagueAsh/news_portal_capstone
