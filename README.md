# Simple Blog App

A Django-based web application for managing and interacting with blog posts, comments, and user profiles. The app uses Django REST Framework to create APIs for blog posts, comments, and profiles, and includes user authentication.

## Features

- **Blog Post Management**: Create, update, and delete blog posts.
- **Comment Management**: Add, update, and delete comments on blog posts.
- **User Profiles**: View and update user profiles.
- **User Authentication**: Secure endpoints with authentication and permissions (JWT).

## Tools Used

- **Django**: High-level Python web framework.
- **Django REST Framework (DRF)**: Toolkit for building Web APIs.
- **Nginx**: Configured as a reverse proxy to serve static and media files.
- **Gunicorn**: WSGI HTTP server for serving the Django application.
- **Docker**: Containerized the application for consistent development and deployment.
- **MySQL**: Used as the database for the application.
- **DigitalOcean**: Hosted the Dockerized application.


## Swagger Documentation

To explore and test the API endpoints, visit the Swagger documentation at [http://165.22.20.68/swagger/schema/](http://165.22.20.68/swagger/schema/). This interactive documentation provides detailed information about each endpoint, including the expected request bodies, response formats, and query parameters.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/gurjika/blog-travelguide/
    ```

2. Change into the project directory:
    ```sh
    cd blog-travelguide
    ```

3. Create a `.env` file and specify the required environment variables:
    ```env
    MYSQL_DB_PASSWORD=your_db_password
    HOST=mysql
    DJANGO_SECRET_KEY=secret_key
    ```

4. Run the application using Docker Compose (Make sure shell scripts use LF line ending, Not CRLF):
    ```sh
    docker-compose up -d
    ```

5. Run the database migrations:
    ```sh
    docker-compose run django python manage.py migrate
    ```

6. Collect Static files:
    ```sh
    docker-compose run django python manage.py collectstatic --no-input
    ```

7. Create a superuser:
    ```sh
    docker-compose run django python manage.py createsuperuser
    ```

8. Access the development server at [http://localhost](http://localhost).

With these steps, your Blog app should be up and running using Docker Compose.

## Deployment

The application is deployed and hosted on DigitalOcean.