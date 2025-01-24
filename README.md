# Log_api_Application
This repository contains a simple Flask-based API for collecting and retrieving log records. It uses an SQLite database for data storage.

Features
Endpoints:
GET /: Welcome message with instructions on using the API.
POST /log: Collects log records by accepting JSON payloads.
GET /logs: Retrieves all stored logs.
Stores log records in an SQLite database.
Supports basic log levels and messages.
# Prerequisites
Ensure you have the following installed:
Python 3.x
Flask
Flask-SQLAlchemy
