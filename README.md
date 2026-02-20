# FlaskAuthApp

FlaskAuthApp is a simple authentication system built using Flask.

This project fixes a backend validation bug in the registration process where
users were able to register without providing required details.

## Bug Fix Description

The following backend validations have been implemented in the `/register` route:

- Name cannot be empty
- Email cannot be empty
- Password cannot be empty
- Password must be at least 6 characters long
- Email must be unique (duplicate registration is prevented)
- All validations are handled on the server-side using Flask

> Note: HTML `required` attributes alone are not used; proper backend validation is implemented.

## Features

- User Registration
- User Login
- Session-based Authentication
- Flash messages for error and success handling

## Tech Stack

- Python
- Flask
- SQLite
- Gunicorn

## Deployment

This application is deployed on Render as a web service.

## How to Run Locally

1. Clone the repository
2. Install dependencies:pip install -r requirements.txt
3. Run the application:python app.py
