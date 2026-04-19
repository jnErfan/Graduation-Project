from werkzeug.security import generate_password_hash, check_password_hash
from extensions import mysql


def query_db(query, args=(), one=False, commit=False):
    """Execute a database query."""
    cursor = mysql.connection.cursor()
    cursor.execute(query, args)
    if commit:
        mysql.connection.commit()
    rv = cursor.fetchone() if one else cursor.fetchall()
    cursor.close()
    return rv


def ensure_portal_tables():
    """Placeholder for table initialization. All tables should be created via schema.sql."""
    pass


# ===== USER MANAGEMENT =====

def get_user_by_email(email):
    return query_db(
        "SELECT u.*, r.name AS role_name, d.name AS department_name "
        "FROM users u "
        "LEFT JOIN roles r ON u.role_id = r.id "
        "LEFT JOIN departments d ON u.department_id = d.id "
        "WHERE u.email = %s",
        (email,),
        one=True,
    )


def get_user_by_id(user_id):
    return query_db(
        "SELECT u.*, r.name AS role_name, d.name AS department_name "
        "FROM users u "
        "LEFT JOIN roles r ON u.role_id = r.id "
        "LEFT JOIN departments d ON u.department_id = d.id "
        "WHERE u.id = %s",
        (user_id,),
        one=True,
    )


def authenticate_user(email, password):
    user = get_user_by_email(email)
    if user and check_password_hash(user["password_hash"], password):
        return user
    return None


def create_user(name, email, password, role_id, department_id=None):
    password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    query_db(
        "INSERT INTO users (name, email, password_hash, role_id, department_id) VALUES (%s, %s, %s, %s, %s)",
        (name, email, password_hash, role_id, department_id),
        commit=True,
    )


def update_user(user_id, name, email, role_id, department_id=None, password=None):
    if password:
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        query_db(
            "UPDATE users SET name = %s, email = %s, role_id = %s, department_id = %s, password_hash = %s WHERE id = %s",
            (name, email, role_id, department_id, password_hash, user_id),
            commit=True,
        )
    else:
        query_db(
            "UPDATE users SET name = %s, email = %s, role_id = %s, department_id = %s WHERE id = %s",
            (name, email, role_id, department_id, user_id),
            commit=True,
        )


def update_user_role(user_id, role_id):
    query_db("UPDATE users SET role_id = %s WHERE id = %s", (role_id, user_id), commit=True)


def delete_user(user_id):
    query_db("DELETE FROM users WHERE id = %s", (user_id,), commit=True)


# ===== ROLE MANAGEMENT =====

def get_role_by_name(role_name):
    return query_db("SELECT * FROM roles WHERE name = %s", (role_name,), one=True)


def get_roles():
    return query_db("SELECT * FROM roles ORDER BY name")


# ===== DEPARTMENT MANAGEMENT =====

def get_departments():
    return query_db("SELECT * FROM departments ORDER BY name")


def get_department_by_id(department_id):
    return query_db("SELECT * FROM departments WHERE id = %s", (department_id,), one=True)


def create_department(name, code, description=None):
    query_db(
        "INSERT INTO departments (name, code, description) VALUES (%s, %s, %s)",
        (name, code, description),
        commit=True,
    )


def update_department(department_id, name, code, description=None):
    query_db(
        "UPDATE departments SET name = %s, code = %s, description = %s WHERE id = %s",
        (name, code, description, department_id),
        commit=True,
    )


def delete_department(department_id):
    query_db("DELETE FROM departments WHERE id = %s", (department_id,), commit=True)


# ===== COURSE MANAGEMENT =====

def get_courses():
    return query_db("SELECT c.*, d.name AS department_name FROM courses c LEFT JOIN departments d ON c.department_id = d.id ORDER BY c.code")


def get_course_by_id(course_id):
    return query_db("SELECT c.*, d.name AS department_name FROM courses c LEFT JOIN departments d ON c.department_id = d.id WHERE c.id = %s", (course_id,), one=True)


def create_course(name, code, department_id, credits):
    query_db(
        "INSERT INTO courses (name, code, department_id, credits) VALUES (%s, %s, %s, %s)",
        (name, code, department_id, credits),
        commit=True,
    )


def update_course(course_id, name, code, department_id, credits):
    query_db(
        "UPDATE courses SET name=%s, code=%s, department_id=%s, credits=%s WHERE id=%s",
        (name, code, department_id, credits, course_id),
        commit=True,
    )


def delete_course(course_id):
    query_db("DELETE FROM courses WHERE id = %s", (course_id,), commit=True)


# ===== ENROLLMENT MANAGEMENT =====
def create_enrollment(student_id, course_id, status='enrolled'):
    query_db(
        "INSERT INTO enrollments (student_id, course_id, status, enrollment_date) VALUES (%s, %s, %s, CURRENT_DATE)",
        (student_id, course_id, status),
        commit=True,
    )


def get_enrollments(student_id=None):
    if student_id:
        return query_db(
            "SELECT e.*, c.name AS course_name, c.code AS course_code FROM enrollments e JOIN courses c ON e.course_id = c.id WHERE e.student_id = %s",
            (student_id,),
        )
    return query_db(
        "SELECT e.*, s.name AS student_name, c.name AS course_name, c.code AS course_code FROM enrollments e JOIN users s ON e.student_id = s.id JOIN courses c ON e.course_id = c.id"
    )


# ===== ATTENDANCE MANAGEMENT =====

def get_attendance(student_id=None, course_id=None):
    base_query = (
        "SELECT a.*, c.name AS course_name, c.code AS course_code "
        "FROM attendance a "
        "JOIN courses c ON a.course_id = c.id "
    )
    if student_id and course_id:
        return query_db(
            base_query + "WHERE a.student_id = %s AND a.course_id = %s ORDER BY a.date DESC",
            (student_id, course_id),
        )
    if student_id:
        return query_db(
            base_query + "WHERE a.student_id = %s ORDER BY a.date DESC",
            (student_id,),
        )
    return query_db(base_query + "ORDER BY a.date DESC")


def add_attendance(student_id, course_id, status, date):
    query_db(
        "INSERT INTO attendance (student_id, course_id, status, date) VALUES (%s, %s, %s, %s)",
        (student_id, course_id, status, date),
        commit=True,
    )


# ===== RESULTS MANAGEMENT =====

def get_results(student_id=None):
    if student_id:
        return query_db(
            "SELECT r.*, c.name AS course_name, c.code AS course_code FROM results r JOIN courses c ON r.course_id = c.id WHERE r.student_id = %s ORDER BY c.code",
            (student_id,),
        )
    return query_db(
        "SELECT r.*, u.name AS student_name, c.name AS course_name, c.code AS course_code FROM results r JOIN users u ON r.student_id = u.id JOIN courses c ON r.course_id = c.id"
    )


def add_result(student_id, course_id, grade, remarks):
    query_db(
        "INSERT INTO results (student_id, course_id, grade, remarks) VALUES (%s, %s, %s, %s)",
        (student_id, course_id, grade, remarks),
        commit=True,
    )


# ===== NEWS MANAGEMENT =====

def get_news():
    return query_db("SELECT * FROM news ORDER BY published_at DESC")


def get_news_by_id(news_id):
    return query_db("SELECT * FROM news WHERE id = %s", (news_id,), one=True)


def create_news(title, summary, content, image_url=None, link_url=None):
    query_db(
        "INSERT INTO news (title, summary, content, image_url, link_url) VALUES (%s, %s, %s, %s, %s)",
        (title, summary, content, image_url, link_url),
        commit=True,
    )


def update_news(news_id, title, summary, content, image_url=None, link_url=None):
    query_db(
        "UPDATE news SET title=%s, summary=%s, content=%s, image_url=%s, link_url=%s WHERE id=%s",
        (title, summary, content, image_url, link_url, news_id),
        commit=True,
    )


def delete_news(news_id):
    query_db("DELETE FROM news WHERE id = %s", (news_id,), commit=True)


# ===== EVENTS MANAGEMENT =====

def get_events():
    return query_db("SELECT * FROM events ORDER BY event_date DESC, start_time")


def get_event_by_id(event_id):
    return query_db("SELECT * FROM events WHERE id = %s", (event_id,), one=True)


def create_event(title, description, event_date, start_time=None, end_time=None, location=None, category=None, image_url=None):
    query_db(
        "INSERT INTO events (title, description, event_date, start_time, end_time, location, category, image_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (title, description, event_date, start_time, end_time, location, category, image_url),
        commit=True,
    )


def update_event(event_id, title, description, event_date, start_time=None, end_time=None, location=None, category=None, image_url=None):
    query_db(
        "UPDATE events SET title=%s, description=%s, event_date=%s, start_time=%s, end_time=%s, location=%s, category=%s, image_url=%s WHERE id=%s",
        (title, description, event_date, start_time, end_time, location, category, image_url, event_id),
        commit=True,
    )


def delete_event(event_id):
    query_db("DELETE FROM events WHERE id = %s", (event_id,), commit=True)


# ===== PROGRAMS MANAGEMENT =====

def get_programs():
    return query_db("SELECT * FROM programs ORDER BY created_at DESC")


def get_program_by_id(program_id):
    return query_db("SELECT * FROM programs WHERE id = %s", (program_id,), one=True)


def create_program(title, description, details=None, image_url=None, link_url=None):
    query_db(
        "INSERT INTO programs (title, description, details, image_url, link_url) VALUES (%s, %s, %s, %s, %s)",
        (title, description, details, image_url, link_url),
        commit=True,
    )


def update_program(program_id, title, description, details=None, image_url=None, link_url=None):
    query_db(
        "UPDATE programs SET title=%s, description=%s, details=%s, image_url=%s, link_url=%s WHERE id=%s",
        (title, description, details, image_url, link_url, program_id),
        commit=True,
    )


def delete_program(program_id):
    query_db("DELETE FROM programs WHERE id = %s", (program_id,), commit=True)


# ===== ADMISSIONS MANAGEMENT =====

def get_admissions():
    return query_db("SELECT * FROM admissions ORDER BY start_date DESC")


def get_admission_by_id(admission_id):
    return query_db("SELECT * FROM admissions WHERE id = %s", (admission_id,), one=True)


def get_notices():
    try:
        return query_db("SELECT * FROM notices ORDER BY created_at DESC")
    except Exception:
        return []


def get_testimonials(student_id=None):
    query = "SELECT * FROM testimonials"
    args = ()
    if student_id:
        query += " WHERE student_id = %s"
        args = (student_id,)
    query += " ORDER BY created_at DESC"
    try:
        return query_db(query, args)
    except Exception:
        return []


def get_campus_landscapes():
    try:
        return query_db("SELECT * FROM campus_landscapes ORDER BY id DESC")
    except Exception:
        return []


def get_teachers_authorities():
    try:
        return query_db("SELECT * FROM teachers_authority ORDER BY id DESC")
    except Exception:
        return []


def get_notice_by_id(notice_id):
    try:
        return query_db("SELECT * FROM notices WHERE id = %s", (notice_id,), one=True)
    except Exception:
        return None


def create_notice(title, content):
    try:
        query_db(
            "INSERT INTO notices (title, content) VALUES (%s, %s)",
            (title, content),
            commit=True,
        )
    except Exception:
        pass


def update_notice(notice_id, title, content):
    try:
        query_db(
            "UPDATE notices SET title=%s, content=%s WHERE id=%s",
            (title, content, notice_id),
            commit=True,
        )
    except Exception:
        pass


def delete_notice(notice_id):
    try:
        query_db("DELETE FROM notices WHERE id = %s", (notice_id,), commit=True)
    except Exception:
        pass


def get_campus_landscape_by_id(landscape_id):
    try:
        return query_db("SELECT * FROM campus_landscapes WHERE id = %s", (landscape_id,), one=True)
    except Exception:
        return None


def create_campus_landscape(image_url=None):
    try:
        query_db(
            "INSERT INTO campus_landscapes (image_url) VALUES (%s)",
            (image_url,),
            commit=True,
        )
    except Exception:
        pass


def update_campus_landscape(landscape_id, image_url=None):
    try:
        query_db(
            "UPDATE campus_landscapes SET image_url=%s WHERE id=%s",
            (image_url, landscape_id),
            commit=True,
        )
    except Exception:
        pass


def delete_campus_landscape(landscape_id):
    try:
        query_db("DELETE FROM campus_landscapes WHERE id = %s", (landscape_id,), commit=True)
    except Exception:
        pass


def get_teacher_authority_by_id(authority_id):
    try:
        return query_db("SELECT * FROM teachers_authority WHERE id = %s", (authority_id,), one=True)
    except Exception:
        return None


def create_teacher_authority(name, role, bio, image_url=None, profile_url=None):
    try:
        query_db(
            "INSERT INTO teachers_authority (name, role, bio, image_url, profile_url) VALUES (%s, %s, %s, %s, %s)",
            (name, role, bio, image_url, profile_url),
            commit=True,
        )
    except Exception:
        pass


def update_teacher_authority(authority_id, name, role, bio, image_url=None, profile_url=None):
    try:
        query_db(
            "UPDATE teachers_authority SET name=%s, role=%s, bio=%s, image_url=%s, profile_url=%s WHERE id=%s",
            (name, role, bio, image_url, profile_url, authority_id),
            commit=True,
        )
    except Exception:
        pass


def delete_teacher_authority(authority_id):
    try:
        query_db("DELETE FROM teachers_authority WHERE id = %s", (authority_id,), commit=True)
    except Exception:
        pass


def get_testimonial_by_id(testimonial_id):
    try:
        return query_db("SELECT * FROM testimonials WHERE id = %s", (testimonial_id,), one=True)
    except Exception:
        return None


def create_testimonial(student_id, content):
    try:
        query_db(
            "INSERT INTO testimonials (student_id, content) VALUES (%s, %s)",
            (student_id, content),
            commit=True,
        )
    except Exception:
        pass


def delete_testimonial(testimonial_id):
    try:
        query_db("DELETE FROM testimonials WHERE id = %s", (testimonial_id,), commit=True)
    except Exception:
        pass


def create_admission(title, description, application_url=None, start_date=None, end_date=None):
    query_db(
        "INSERT INTO admissions (title, description, application_url, start_date, end_date) VALUES (%s, %s, %s, %s, %s)",
        (title, description, application_url, start_date, end_date),
        commit=True,
    )


def update_admission(admission_id, title, description, application_url=None, start_date=None, end_date=None):
    query_db(
        "UPDATE admissions SET title=%s, description=%s, application_url=%s, start_date=%s, end_date=%s WHERE id=%s",
        (title, description, application_url, start_date, end_date, admission_id),
        commit=True,
    )


def delete_admission(admission_id):
    query_db("DELETE FROM admissions WHERE id = %s", (admission_id,), commit=True)


# ===== USER QUERIES =====

def get_students():
    return query_db("SELECT u.*, d.name AS department_name FROM users u LEFT JOIN departments d ON u.department_id = d.id WHERE u.role_id = 1 ORDER BY u.name")


def get_faculty():
    return query_db("SELECT u.*, d.name AS department_name FROM users u LEFT JOIN departments d ON u.department_id = d.id WHERE u.role_id = 2 ORDER BY u.name")


def get_admins():
    return query_db(
        "SELECT u.*, d.name AS department_name FROM users u "
        "LEFT JOIN departments d ON u.department_id = d.id "
        "JOIN roles r ON u.role_id = r.id "
        "WHERE r.name = 'admin' ORDER BY u.name"
    )
