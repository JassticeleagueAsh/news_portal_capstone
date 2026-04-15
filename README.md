# News Portal Capstone

## Project Overview

This project is a Django-based news portal web application developed as part of a capstone assignment.

The system allows multiple types of users to interact with news content based on their assigned roles. Each role has specific permissions that control what actions the user can perform.

The application supports content creation, moderation, subscriptions, API access, and automated testing to ensure reliability.

---

## User Roles

The application includes four main user roles:

* Reader
* Journalist
* Editor
* Publisher

Each role has distinct permissions and access within the system.

---

## Features

### Authentication and User Management

* Users can register an account
* Users can log in and log out
* Users select their role during registration
* A custom user model is implemented
* Users are redirected to role-specific pages after login

---

### Reader Features

* Readers can view approved articles only
* Readers can open article detail pages
* Readers cannot access unapproved content
* Readers can subscribe to publishers
* Readers can subscribe to journalists
* Readers can view newsletters from the newsletter feed
* Readers can access both articles and newsletters from the dashboard

---

### Journalist Features

* Journalists can access a personal dashboard
* Journalists can create articles
* Journalists can update their own articles
* Journalists can delete their own articles
* Journalists can create newsletters
* Journalists can update newsletters
* Journalists can delete newsletters
* Articles created by journalists require editor approval

---

### Editor Features

* Editors can access the article review page
* Editors can view all submitted articles
* Editors can approve articles
* Editors can update articles
* Editors can delete articles
* Editors can manage newsletters
* Editors can create publishers

---

### Publisher Features

* Publishers can register and log in as a user role
* Publishers act as content entities linked to articles
* Editors can create and manage publishers
* Articles are associated with publishers to represent the publishing source
* Publishers can view newsletters through the system

---

### Newsletter Features

* Newsletters can be created by journalists
* Articles can be added to newsletters
* A many-to-many relationship exists between articles and newsletters
* Newsletters are linked to the author (journalist)

Readers can access newsletters through:

* The Newsletter Feed page (`/newsletters/`)
* The Reader dashboard

---

### Subscription Features

* Readers can subscribe to publishers
* Readers can subscribe to journalists
* Subscriptions are implemented using many-to-many relationships
* Approved articles trigger notifications to subscribers

---

### Signals and Notifications

* When an article is approved, a notification process is triggered
* Email notifications are sent to subscribers
* An external API request is sent when an article is approved
* This simulates integration with external systems

---

## API Functionality

The application includes REST API support using Django REST Framework.

Configured API components include:

* `serializers.py`
* `api_views.py`
* `api_urls.py`
* `permissions.py`

### Available API Endpoints

Public endpoints:

* `GET /api/articles/` — returns all approved articles
* `GET /api/articles/<id>/` — returns a single approved article

Protected endpoints:

* `GET /api/articles/subscribed/` — returns approved articles from publishers and journalists the authenticated reader is subscribed to
* `POST /api/articles/create/` — allows an authenticated journalist to create an article
* `PUT /api/articles/<id>/update/` — allows an authenticated editor or journalist to update an article
* `DELETE /api/articles/<id>/delete/` — allows an authenticated editor or journalist to delete an article

---

## API Authentication

This project uses Django REST Framework token-based authentication to secure protected API endpoints.

Two authentication endpoints are available:

* `POST /api/token/` — generates an authentication token using Django REST Framework's built-in token view
* `POST /api/login/` — custom API login endpoint that validates credentials and returns a token

### Option 1: Obtain a token using `/api/token/`

Send a POST request to:

```text
/api/token/

### Obtain Token

Send a POST request to:

```
/api/token/
```

Request body (JSON):

```
{
    "username": "your_username",
    "password": "your_password"
}
```

Response:

```
{
    "token": "your_generated_token"
}
```

---

### Access Protected Endpoints

Include the token in request headers:

```
Authorization: Token your_generated_token
```

Example protected endpoint:

```
/api/articles/subscribed/
```

Only authenticated users can access protected API endpoints.

---

## Admin Features

* Admin access is available via the Django admin panel
* Admin can manage users, articles, newsletters, and publishers

---

## Styling

* The application uses Bootstrap for styling
* Includes a styled landing page
* Includes styled login and registration pages
* Role-based pages are styled consistently

---

## Technologies Used

* Python
* Django
* Django REST Framework
* MariaDB
* mysqlclient
* python-dotenv
* Bootstrap 5

---

## Project Structure

```
news_portal_capstone/
│
├── core/                 # Main application logic
├── news_portal/          # Project settings and URLs
├── planning/             # Planning documents
├── static/               # Static files (CSS)
├── templates/            # HTML templates
│   ├── core/
│   └── registration/
│
├── .env.example          # Example environment variables
├── .gitignore
├── manage.py
├── README.md
├── requirements.txt
```

---

## Database Setup

This project uses MariaDB instead of SQLite.

### 1. Create the database

Run:

```
CREATE DATABASE news_portal_db;
```

---

### 2. Environment Variables

Create a `.env` file in the root directory:

```
DB_NAME=news_portal_db
DB_USER=root
DB_PASSWORD=your_password_here
DB_HOST=127.0.0.1
DB_PORT=3306
SECRET_KEY=your_secret_key_here
```

---

## Installation Instructions

Clone the repository:

```
git clone <repository-url>
cd news_portal_capstone
```

Create and activate a virtual environment:

```
python -m venv .venv
.\.venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Apply migrations:

```
python manage.py makemigrations
python manage.py migrate
```

Run the development server:

```
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

---

## Running Tests

This project includes automated unit tests covering:

* User authentication
* Role-based permissions
* Article creation and approval
* Newsletter functionality
* API endpoints

Run tests using:

```
python manage.py test
```

---

## Role Permissions Summary

### Reader

* Can view approved articles
* Can view newsletters
* Can subscribe to publishers and journalists

### Journalist

* Can create, update, and delete articles
* Can create, update, and delete newsletters

### Editor

* Can review, approve, update, and delete articles
* Can manage newsletters
* Can create publishers

### Publisher

* Can register and log in
* Can view newsletters
* Is linked to articles as a publishing entity

---

## Academic Integrity Note

This project was developed as part of coursework. All implementation, configuration, and testing were completed independently. Official documentation and learning resources were used for guidance where necessary.

---

## Final Notes

This application demonstrates:

* Role-based access control
* Content creation and moderation workflows
* Database relationships and data modelling
* API integration and authentication
* Automated testing and validation
