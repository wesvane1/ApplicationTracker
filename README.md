# Firebase User Management System

This Python application allows users to manage their accounts and applications using Firebase Firestore as the backend database. Users can sign in, create accounts, view data, add applications, and update their application status.

## Features

- User authentication (sign in and create an account)
- View user-specific data without exposing passwords
- Add and update application status for companies
- Update company names associated with applications
- Simple command-line interface for user interaction

## Prerequisites

To run this application, you need to have the following installed:

- Python 3.x
- `firebase-admin` package
- `python-dotenv` package

You can install the required packages using pip:

```bash
pip install firebase-admin python-dotenv