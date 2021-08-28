from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user, login_user, logout_user
from . import db
from .models import User
from .forms import LoginForm, SignUpForm
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.hello'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                flash('Вход выполнен!', category='success')
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('views.hello')
                return redirect(next_page)
            else:
                flash('Неверный пароль!', category='error')
        else:
            flash('Неверная почта!', category='error')

    return render_template('login.html', user=current_user, form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.hello'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('views.hello'))
    form = SignUpForm()
    if form.validate_on_submit():
        password = form.password.data
        if len(password) < 5:
            flash('Пароль слишком короткий, должен быть длиннее 5 символов!', category='error')
        else:
            new_user = User(email=form.email.data,
                            username=form.username.data,
                            password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('Пользователь создан!')
            return redirect(url_for('views.home'))

    return render_template('signup.html', user=current_user, form=form)
