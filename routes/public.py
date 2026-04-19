from flask import Blueprint, render_template
from models import get_news, get_events, get_programs, get_admissions, query_db

public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def home():
    programs = get_programs()
    return render_template('public/home.html', programs=programs)


@public_bp.route('/about')
def about():
    return render_template('public/about.html')


@public_bp.route('/admissions')
def admissions():
    admissions_data = get_admissions()
    programs = get_programs()
    return render_template('public/admissions.html', admissions_data=admissions_data, programs=programs)


@public_bp.route('/academics')
def academics():
    programs = get_programs()
    return render_template('public/academics.html', programs=programs)


@public_bp.route('/faculty')
def faculty():
    return render_template('public/faculty.html')


@public_bp.route('/campus-facilities')
def campus_facilities():
    return render_template('public/campus_facilities.html')


@public_bp.route('/news')
def news():
    news_items = get_news()
    return render_template('public/news.html', news_items=news_items)


@public_bp.route('/events')
def events():
    events_list = get_events()
    return render_template('public/events.html', events_list=events_list)


@public_bp.route('/alumni')
def alumni():
    return render_template('public/alumni.html')


@public_bp.route('/contact')
def contact():
    return render_template('public/contact.html')
