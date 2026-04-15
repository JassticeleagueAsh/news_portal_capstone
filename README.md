# News Portal Capstone

## Project Overview

This project is a Django-based News Portal web application developed as part of a capstone assignment.

The system supports multiple user roles with role-based permissions and allows for content creation, moderation, subscriptions, and API access.

---

## User Roles

* Reader
* Journalist
* Editor
* Publisher

Each role has specific permissions controlling access and actions.

---

## Core Features

### Authentication & User Management

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
* Articles require editor approval

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

### Get Token

```bash
POST /api/token/
```

Body:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

### Use Token

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

---

## Project Structure

```
news_portal_capstone/
├── core/
├── news_portal/
├── planning/
├── static/
├── templates/
├── docs/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
```

---

## Database Setup (MariaDB)

Create database:

```sql
CREATE DATABASE news_portal_db;
```

Create `.env` file:

```env
DB_NAME=news_portal_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=3306
SECRET_KEY=your_secret_key
```

---

## Running the Project

### 1. Using Virtual Environment (venv)

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

### 2. Using Docker

Make sure Docker Desktop is running.

```bash
docker-compose build
docker-compose up
```

Open:

```
http://127.0.0.1:8000/
```

Stop containers:

```bash
docker-compose down
```

---

## Running Tests

```bash
python manage.py test
```

---

## Key Concepts Demonstrated

* Role-based access control
* Django ORM relationships
* REST API development
* Token authentication
* Docker containerization
* Sphinx documentation
* Clean project structuring

---

## Notes

* Sensitive data is not committed (see `.env.example`)
* Project follows best practices for deployment readiness

---

## Author

Ashwin Jass

---

## Repository

