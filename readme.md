# Web SFTP Interface

A secure web-based SFTP interface built with Flask that provides controlled file access through a user-friendly interface.

## Features

- Secure user authentication and authorization
- Role-based access control for files and directories 
- Intuitive file browser interface with breadcrumb navigation
- File search functionality
- Clean and responsive UI design
- SQL Server backend for user and permission management

## Technical Stack

- **Backend**: Python/Flask
- **Database**: Microsoft SQL Server
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Flask-Login
- **Security**: Password hashing, Path traversal protection

## Setup

1. Create SQL Server database using the provided script in `database_scripts/databasev1.sql`

2. Configure environment variables:
   ```
   BASE_DIR=<path to root directory for file access>
   SQLALCHEMY_DATABASE_URI=<your SQL Server connection string>
   SECRET_KEY=<your secret key>
   ```

3. Install dependencies:
   ```
   pip install flask flask-login flask-sqlalchemy pyodbc
   ```

4. Run the application:
   ```
   python app.py
   ```

## Security Features

- Password hashing for secure credential storage
- Protection against directory traversal attacks
- Granular path-based permissions system
- Session-based authentication
- SQL injection prevention through SQLAlchemy ORM

## Directory Structure
