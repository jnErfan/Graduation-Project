# University Website & Management System

A Flask + MySQL application with a public-facing university website and a role-based management portal for students, faculty, and admins.

## Features
- Public pages: Home, About, Admissions, Academics, Faculty & Staff, Student Life, Campus Facilities, News, Events, Alumni, Contact
- Management portal with student, faculty, and admin dashboards
- Role-based access control using Flask session management
- MySQL database schema for users, roles, departments, courses, enrollments, attendance, results
- Bootstrap 5 responsive UI

## Setup
1. Create a MySQL database named `university_portal`.
2. Import `schema.sql`.
3. Install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. Configure database credentials in `config.py` or via environment variables.
5. Run the app:
   ```bash
   python app.py
   ```

## Project Structure
- `app.py` - Flask app factory and blueprint registration
- `config.py` - MySQL and secret key configuration
- `models.py` - Database access and query functions
- `routes/` - Public website, authentication, and portal route handling
- `templates/` - Bootstrap templates for pages and portal views
- `static/` - CSS and JS assets
