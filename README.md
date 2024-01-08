# Roadcast - Social Networking API

Roadcast is a social networking API built with Django and Django Rest Framework. It provides endpoints for user authentication, friend requests, and user profile management.

## Features

- User registration and authentication
- Sending and accepting friend requests
- Searching for users by email or name
- Sending, Accepting and Rejecting friend requests  
- Rate limiting on friend requests

## Prerequisites

Before running the project, make sure you have the following installed:

- Python 3.x
- PostgreSQL
- Django
- Django Rest Framework

## Getting Started

1. Clone the repository:

    ```bash
    git clone https://github.com/preeti-kashyap/roadcast.git
    
    ```

2. Install dependencies:

    ```bash
    python install virtualenv
    
    # Create a virtual environment named 'env'
    python -m venv env

    # Activate the virtual environment
    # On Windows
    .\env\Scripts\activate
    
    pip install -r requirements.txt

    cd roadcast
    ```
    




3. Database Setup:

    - Create a PostgreSQL database and update the settings in `settings.py`.
    - #Note: Please update name, user, server, host, password and port in `settings.py`
    - Run migrations:

        ```bash
        python manage.py makemigrations
        python manage.py migrate
        ```

4. Run the server:

    ```bash
    python manage.py runserver
    ```


## API Endpoints

- `/signup/`: User registration
- `/login/`: User login
- `/user-search/`: Search users by email or name
- `/friend-requests/send/`: Send friend requests
- `/update-friend-request/` : Accept or Reject fried requests
- `/friend-request/`: List of friend requests
- `/friend-list/`: List of accepted friend requests
- `/friend-requests/pending//`: List of pending friend requests

## Rate Limiting

The API applies rate limiting to friend requests to prevent abuse. Users can send a maximum of 3 friend requests within a minute.


