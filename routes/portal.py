from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import datetime
from routes.auth import login_required, role_required
from models import query_db
from models import (
    get_user_by_id,
    get_user_by_email,
    get_enrollments,
    get_attendance,
    get_results,
    get_courses,
    get_course_by_id,
    add_attendance,
    get_students,
    get_faculty,
    get_departments,
    get_department_by_id,
    create_course,
    create_department,
    create_user,
    get_roles,
    get_role_by_name,
    update_user,
    delete_user,
    update_department,
    delete_department,
    get_news,
    get_news_by_id,
    create_news,
    update_news,
    delete_news,
    get_events,
    get_event_by_id,
    create_event,
    update_event,
    delete_event,
    get_programs,
    get_program_by_id,
    create_program,
    update_program,
    delete_program,
    get_admissions,
    get_admission_by_id,
    create_admission,
    update_admission,
    delete_admission,
    create_enrollment,
)

portal_bp = Blueprint('portal', __name__, url_prefix='/portal')


def current_user():
    return get_user_by_id(session.get('user_id')) if session.get('user_id') else None


@portal_bp.route('/student/dashboard')
@login_required
@role_required('student')
def student_dashboard():
    user = current_user()
    enrollments = get_enrollments(user['id'])
    attendance = get_attendance(student_id=user['id'])
    results = get_results(student_id=user['id'])
    attendance_summary = {
        'present': sum(1 for record in attendance if record['status'] == 'present'),
        'absent': sum(1 for record in attendance if record['status'] == 'absent'),
        'excused': sum(1 for record in attendance if record['status'] == 'excused'),
    }
    enrolled_course_ids = {enrollment['course_id'] for enrollment in enrollments}
    return render_template(
        'portal/student_dashboard.html',
        user=user,
        enrollments=enrollments,
        attendance=attendance,
        results=results,
        attendance_summary=attendance_summary,
        enrolled_course_ids=enrolled_course_ids,
    )


@portal_bp.route('/faculty/dashboard')
@login_required
@role_required('faculty')
def faculty_dashboard():
    user = current_user()
    courses = get_courses()
    return render_template('portal/faculty_dashboard.html', user=user, courses=courses)


@portal_bp.route('/admin/dashboard', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def admin_dashboard():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        if not name or not email or not password:
            flash('Please provide name, email, and password for the new admin.', 'danger')
            return redirect(url_for('portal.admin_dashboard'))
        if get_user_by_email(email):
            flash('A user with that email already exists.', 'warning')
            return redirect(url_for('portal.admin_dashboard'))
        admin_role = get_role_by_name('admin')
        if not admin_role:
            flash('Admin role not found. Please define roles before creating admins.', 'danger')
            return redirect(url_for('portal.admin_dashboard'))
        create_user(name, email, password, admin_role['id'])
        flash('New admin account created successfully.', 'success')
        return redirect(url_for('portal.admin_dashboard'))

    students = get_students()
    faculty = get_faculty()
    courses = get_courses()
    departments = get_departments()
    news_items = get_news()
    events = get_events()
    programs = get_programs()
    admissions = get_admissions()
    return render_template(
        'portal/admin_dashboard.html',
        students=students,
        faculty=faculty,
        courses=courses,
        departments=departments,
        news_count=len(news_items),
        event_count=len(events),
        program_count=len(programs),
        admission_count=len(admissions),
    )


@portal_bp.route('/student/profile')
@login_required
@role_required('student')
def student_profile():
    user = current_user()
    enrollments = get_enrollments(user['id'])
    attendance = get_attendance(student_id=user['id'])
    results = get_results(student_id=user['id'])
    return render_template(
        'portal/student_profile.html',
        user=user,
        enrollment_count=len(enrollments),
        attendance_count=len(attendance),
        result_count=len(results),
    )


@portal_bp.route('/student/register-courses', methods=['GET', 'POST'])
@login_required
@role_required('student')
def course_registration():
    user = current_user()
    enrollments = get_enrollments(user['id'])
    enrolled_course_ids = {enrollment['course_id'] for enrollment in enrollments}
    if request.method == 'POST':
        course_id = request.form.get('course_id')
        if not course_id:
            flash('Please select a course to register.', 'danger')
            return redirect(url_for('portal.course_registration'))
        course_id = int(course_id)
        if course_id in enrolled_course_ids:
            flash('You are already registered for that course.', 'warning')
            return redirect(url_for('portal.course_registration'))
        create_enrollment(user['id'], course_id)
        flash('Course registered successfully.', 'success')
        return redirect(url_for('portal.course_registration'))
    courses = get_courses()
    return render_template('portal/course_registration.html', courses=courses, enrolled_course_ids=enrolled_course_ids)


@portal_bp.route('/student/attendance', methods=['GET', 'POST'])
@login_required
@role_required('student')
def student_attendance():
    user = current_user()
    enrollments = get_enrollments(user['id'])
    enrolled_course_ids = {enrollment['course_id'] for enrollment in enrollments}
    attendance = get_attendance(student_id=user['id'])
    today = datetime.date.today()

    if request.method == 'POST':
        course_id = request.form.get('course_id')
        status = request.form.get('status')
        if not course_id or not status:
            flash('Please select a course and attendance status.', 'danger')
            return redirect(url_for('portal.student_attendance'))

        course_id = int(course_id)
        if course_id not in enrolled_course_ids:
            flash('You can only submit attendance for courses you are registered in.', 'warning')
            return redirect(url_for('portal.student_attendance'))

        course_attendance = get_attendance(student_id=user['id'], course_id=course_id)
        if any(record['date'] == today for record in course_attendance):
            flash('Attendance for this course has already been submitted for today.', 'warning')
            return redirect(url_for('portal.student_attendance'))

        add_attendance(user['id'], course_id, status, today)
        flash('Daily attendance submitted successfully.', 'success')
        return redirect(url_for('portal.student_attendance'))

    return render_template(
        'portal/attendance.html',
        attendance=attendance,
        enrolled_courses=enrollments,
        today=today,
    )



@portal_bp.route('/student/results')
@login_required
@role_required('student')
def student_results():
    user = current_user()
    results = get_results(student_id=user['id'])
    return render_template('portal/results.html', results=results)


@portal_bp.route('/admin/manage-users', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def manage_users():
    students = get_students()
    faculty = get_faculty()
    departments = get_departments()

    roles = get_roles()
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        department_id = request.form.get('department_id') or None
        role_id = request.form.get('role_id') or None
        if not role_id:
            flash('Please select a role.', 'danger')
            return redirect(url_for('portal.manage_users'))
        create_user(name, email, password, int(role_id), department_id)
        flash('Student account created successfully.', 'success')
        return redirect(url_for('portal.manage_users'))

    return render_template('portal/manage_users.html', students=students, faculty=faculty, departments=departments, roles=roles)


@portal_bp.route('/admin/user/delete/<int:user_id>')
@login_required
@role_required('admin')
def delete_user_account(user_id):
    delete_user(user_id)
    flash('User account deleted successfully.', 'success')
    return redirect(url_for('portal.manage_users'))


@portal_bp.route('/admin/user/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('portal.manage_users'))
    roles = get_roles()
    departments = get_departments()
    if request.method == 'POST':
        update_user(
            user_id,
            request.form['name'],
            request.form['email'],
            int(request.form['role_id']),
            request.form.get('department_id') or None,
            request.form.get('password') or None,
        )
        flash('User updated successfully.', 'success')
        return redirect(url_for('portal.manage_users'))
    return render_template('portal/edit_user.html', user=user, roles=roles, departments=departments)


@portal_bp.route('/admin/manage-news', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def manage_news():
    if request.method == 'POST':
        if request.form.get('news_id'):
            update_news(
                request.form['news_id'],
                request.form['title'],
                request.form['summary'],
                request.form.get('content'),
                request.form.get('image_url'),
                request.form.get('link_url'),
            )
            flash('News item updated successfully.', 'success')
        else:
            create_news(
                request.form['title'],
                request.form['summary'],
                request.form.get('content'),
                request.form.get('image_url'),
                request.form.get('link_url'),
            )
            flash('News item added successfully.', 'success')
        return redirect(url_for('portal.manage_news'))

    news_items = get_news()
    return render_template('portal/manage_news.html', news_items=news_items)





@portal_bp.route('/admin/news/delete/<int:news_id>')
@login_required
@role_required('admin')
def delete_news_item(news_id):
    delete_news(news_id)
    flash('News item deleted.', 'success')
    return redirect(url_for('portal.manage_news'))


@portal_bp.route('/admin/news/edit/<int:news_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_news(news_id):
    item = get_news_by_id(news_id)
    if not item:
        flash('News item not found.', 'danger')
        return redirect(url_for('portal.manage_news'))
    if request.method == 'POST':
        update_news(
            news_id,
            request.form['title'],
            request.form['summary'],
            request.form.get('content'),
            request.form.get('image_url'),
            request.form.get('link_url'),
        )
        flash('News item updated successfully.', 'success')
        return redirect(url_for('portal.manage_news'))
    return render_template('portal/edit_news.html', item=item)


@portal_bp.route('/admin/manage-events', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def manage_events():
    if request.method == 'POST':
        if request.form.get('event_id'):
            update_event(
                request.form['event_id'],
                request.form['title'],
                request.form['description'],
                request.form['event_date'],
                request.form.get('start_time'),
                request.form.get('end_time'),
                request.form.get('location'),
                request.form.get('category'),
                request.form.get('image_url'),
            )
            flash('Event updated successfully.', 'success')
        else:
            create_event(
                request.form['title'],
                request.form['description'],
                request.form['event_date'],
                request.form.get('start_time'),
                request.form.get('end_time'),
                request.form.get('location'),
                request.form.get('category'),
                request.form.get('image_url'),
            )
            flash('Event added successfully.', 'success')
        return redirect(url_for('portal.manage_events'))

    events = get_events()
    return render_template('portal/manage_events.html', events=events)


@portal_bp.route('/admin/events/delete/<int:event_id>')
@login_required
@role_required('admin')
def delete_event_item(event_id):
    delete_event(event_id)
    flash('Event deleted.', 'success')
    return redirect(url_for('portal.manage_events'))


@portal_bp.route('/admin/events/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_event(event_id):
    item = get_event_by_id(event_id)
    if not item:
        flash('Event not found.', 'danger')
        return redirect(url_for('portal.manage_events'))
    if request.method == 'POST':
        update_event(
            event_id,
            request.form['title'],
            request.form['description'],
            request.form['event_date'],
            request.form.get('start_time'),
            request.form.get('end_time'),
            request.form.get('location'),
            request.form.get('category'),
            request.form.get('image_url'),
        )
        flash('Event updated successfully.', 'success')
        return redirect(url_for('portal.manage_events'))
    return render_template('portal/edit_event.html', item=item)


@portal_bp.route('/admin/manage-programs', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def manage_programs():
    if request.method == 'POST':
        if request.form.get('program_id'):
            update_program(
                request.form['program_id'],
                request.form['title'],
                request.form['description'],
                request.form.get('details'),
                request.form.get('image_url'),
                request.form.get('link_url'),
            )
            flash('Program updated successfully.', 'success')
        else:
            create_program(
                request.form['title'],
                request.form['description'],
                request.form.get('details'),
                request.form.get('image_url'),
                request.form.get('link_url'),
            )
            flash('Program added successfully.', 'success')
        return redirect(url_for('portal.manage_programs'))

    programs = get_programs()
    return render_template('portal/manage_programs.html', programs=programs)


@portal_bp.route('/admin/programs/delete/<int:program_id>')
@login_required
@role_required('admin')
def delete_program_item(program_id):
    delete_program(program_id)
    flash('Program deleted.', 'success')
    return redirect(url_for('portal.manage_programs'))


@portal_bp.route('/admin/programs/edit/<int:program_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_program(program_id):
    item = get_program_by_id(program_id)
    if not item:
        flash('Program not found.', 'danger')
        return redirect(url_for('portal.manage_programs'))
    if request.method == 'POST':
        update_program(
            program_id,
            request.form['title'],
            request.form['description'],
            request.form.get('details'),
            request.form.get('image_url'),
            request.form.get('link_url'),
        )
        flash('Program updated successfully.', 'success')
        return redirect(url_for('portal.manage_programs'))
    return render_template('portal/edit_program.html', item=item)


@portal_bp.route('/admin/manage-admissions', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def manage_admissions():
    if request.method == 'POST':
        if request.form.get('admission_id'):
            update_admission(
                request.form['admission_id'],
                request.form['title'],
                request.form['description'],
                request.form.get('application_url'),
                request.form.get('start_date'),
                request.form.get('end_date'),
            )
            flash('Admission record updated successfully.', 'success')
        else:
            create_admission(
                request.form['title'],
                request.form['description'],
                request.form.get('application_url'),
                request.form.get('start_date'),
                request.form.get('end_date'),
            )
            flash('Admission record added successfully.', 'success')
        return redirect(url_for('portal.manage_admissions'))

    admissions = get_admissions()
    return render_template('portal/manage_admissions.html', admissions=admissions)


@portal_bp.route('/admin/admissions/delete/<int:admission_id>')
@login_required
@role_required('admin')
def delete_admission_item(admission_id):
    delete_admission(admission_id)
    flash('Admission record deleted.', 'success')
    return redirect(url_for('portal.manage_admissions'))


@portal_bp.route('/admin/admissions/edit/<int:admission_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_admission(admission_id):
    item = get_admission_by_id(admission_id)
    if not item:
        flash('Admission record not found.', 'danger')
        return redirect(url_for('portal.manage_admissions'))
    if request.method == 'POST':
        update_admission(
            admission_id,
            request.form['title'],
            request.form['description'],
            request.form.get('application_url'),
            request.form.get('start_date'),
            request.form.get('end_date'),
        )
        flash('Admission record updated successfully.', 'success')
        return redirect(url_for('portal.manage_admissions'))
    return render_template('portal/edit_admission.html', item=item)


@portal_bp.route('/admin/manage-courses', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def manage_courses():
    courses = get_courses()
    departments = get_departments()
    if request.method == 'POST':
        create_course(
            request.form['name'],
            request.form['code'],
            request.form['department_id'],
            request.form['credits'],
        )
        flash('Course added successfully.', 'success')
        return redirect(url_for('portal.manage_courses'))
    return render_template('portal/manage_courses.html', courses=courses, departments=departments)



@portal_bp.route('/admin/manage-departments', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def manage_departments():
    departments = get_departments()
    if request.method == 'POST':
        create_department(request.form['name'], request.form['code'], request.form.get('description'))
        flash('Department added successfully.', 'success')
        return redirect(url_for('portal.manage_departments'))
    return render_template('portal/manage_departments.html', departments=departments)


@portal_bp.route('/admin/department/delete/<int:department_id>')
@login_required
@role_required('admin')
def delete_department_item(department_id):
    delete_department(department_id)
    flash('Department deleted successfully.', 'success')
    return redirect(url_for('portal.manage_departments'))


@portal_bp.route('/admin/department/edit/<int:department_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_department(department_id):
    department = get_department_by_id(department_id)
    if not department:
        flash('Department not found.', 'danger')
        return redirect(url_for('portal.manage_departments'))
    if request.method == 'POST':
        update_department(
            department_id,
            request.form['name'],
            request.form['code'],
            request.form.get('description'),
        )
        flash('Department updated successfully.', 'success')
        return redirect(url_for('portal.manage_departments'))
    return render_template('portal/edit_department.html', department=department)
