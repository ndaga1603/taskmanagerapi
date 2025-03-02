# Task Manager API

A RESTful API built with Django and Django REST Framework (DRF) to manage tasks. Users can create, read, update, and delete (CRUD) tasks, mark them as completed, and filter by status—all secured with JWT authentication.

**Date:** March 02, 2025

**Author:** David A. Ndaga

**Built for:** Hands-on workshop demo

## Features

- **CRUD Operations:** Manage tasks via HTTP methods (GET, POST, PUT, DELETE).
- **JWT Authentication:** Secure endpoints with djangorestframework-simplejwt.
- **Filtering & Pagination:** Filter tasks by completed status and paginate results (10 tasks per page).
- **Secure Design:** Short-lived access tokens, HTTPS-ready, and blacklisted refresh tokens.

## Prerequisites

- Python 3.12+
- Virtual environment (e.g., venv)
- Git (optional, for cloning)

## Installation

### Clone the Repository

```bash
git clone <https://github.com/ndaga1603/taskmanagerapi.git>
cd task-manager-api
```

### Set Up Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the project root:

```text
SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=False
```

### Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create a Superuser

```bash
python manage.py createsuperuser
```

### Run the Server

```bash
python manage.py runserver
```

## Project Structure

```text
task-manager-api/
├── task_manager/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tasks/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── .env
├── manage.py
└── requirements.txt
```

## API Endpoints

### Authentication

**Login (Get Token):**

```text
POST /api/login/
Content-Type: application/json
{
    "username": "testuser",
    "password": "testpass123"
}
```

Returns: access and refresh tokens.

**Refresh Token:**

```text
POST /api/refresh/
{
    "refresh": "<refresh-token>"
}
```

**Logout (Blacklist Token):**

```text
POST /api/logout/
Authorization: Bearer <access-token>
{
    "refresh": "<refresh-token>"
}
```

### Tasks

All endpoints require `Authorization: Bearer <access-token>`.

**List/Create Tasks:**

```text
GET /api/tasks/          # List user’s tasks
POST /api/tasks/         # Create a task
{
    "title": "New Task",
    "description": "Do this",
    "completed": false
}
```

**Task Details (CRUD):**

```text
GET /api/task/<id>/     # Retrieve task
PUT /api/task/<id>/     # Update task
DELETE /api/task/<id>/  # Delete task
```

**Filtering & Pagination:**

```text
GET /api/tasks/?search=django  # Search tasks by title or description
GET /api/tasks/?completed=true   # Filter completed tasks
```

## Security Features

- **JWT Authentication:** Uses simplejwt with:
  - Access tokens: 15-minute lifetime.
  - Refresh tokens: 1-day lifetime, rotated and blacklisted on refresh via "jti" (token identifier).

## Usage Example

**Get a Token:**

```bash
curl -X POST <http://localhost:8000/api/login/> \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpass123"}'
```

**List Tasks:**

```bash
curl -X GET <http://localhost:8000/api/tasks/> \
-H "Authorization: Bearer <access-token>"
```

**Create a Task:**

```bash
curl -X POST http://localhost:8000/api/tasks/ \
-H "Authorization: Bearer <access-token>" \
-H "Content-Type: application/json" \
-d '{"title": "Test Task", "description": "Do this", "completed": false}'
```

## Contributing

Feel free to fork this repository, submit issues, or send pull requests. For the workshop, bring your questions to the Q&A!

## License

This project is unlicensed for workshop purposes—use it freely for learning!
