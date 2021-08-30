from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Post, User, Comment, Like
from sqlalchemy import desc, func
from .forms import EditProfileForm, PostForm, CommentForm
from datetime import datetime
from os import path, rename
from PIL import Image


views = Blueprint('views', __name__)


@views.route('/')
@views.route('/hello')
def hello():
    return render_template('hello.html', user=current_user)


@views.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(desc('id')).paginate(
        page, 5, False)
    next_url = url_for('views.home', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('views.home', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('home.html', user=current_user, posts=posts, next_url=next_url, prev_url=prev_url)


@views.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        text = form.text.data

        post = Post(text=text, author=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Пост создан!', category='success')
        return redirect(url_for('views.home'))

    return render_template('create_post.html', user=current_user, form=form)


@views.route('<post_id>/edit_post', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    form = PostForm()
    if form.validate_on_submit():
        post.text = form.text.data
        db.session.add(post)
        db.session.commit()
        flash('Данные сохранены.')
        return redirect(url_for('views.post', post_id=post_id))
    elif request.method == 'GET':
        form.text.data = post.text
    return render_template('edit_post.html', user=current_user, form=form)


@views.route('/delete_post/<id>')
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash('Пост не может быть найден!', category='error')
    elif current_user.id != post.author:
        flash('Вы не можете удалить этот пост!', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Пост удалён!', category='success')
    return redirect(url_for('views.home'))


@views.route('/create_comment/<post_id>', methods=['GET', 'POST'])
@login_required
def create_comment(post_id):

    form = CommentForm()
    post = Post.query.filter_by(id=post_id)
    if post:
        if form.validate_on_submit():
            text = form.text.data
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
    else:
        flash('Пост не существует!', category='error')
    return redirect(url_for('views.post', post_id=post_id, form=form))


@views.route('/post/<post_id>/delete_comment/<comment_id>')
@login_required
def delete_comment(post_id, comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        flash('Комментарий не существует!', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('У Вас нет разрешения удалять этот комментарий!', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.post', post_id=post_id))


@views.route('/like_post/<post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error': 'Пост не существует!'}, 400)

    elif like:
        db.session.delete(like)
        db.session.commit()

    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({
        'likes': len(post.likes),
        'liked': current_user.id in map(lambda x: x.author, post.likes)
    })


@views.route('/<username>/profile')
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('Пользователя не существует!', category='error')
    return render_template('profile.html', user=user)


@views.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()


@views.route('<username>/load_photo', methods=['GET', 'POST'])
@login_required
def load_photo(username):
    if request.method == 'POST':
        photo = request.files['photo']
        user = User.query.filter_by(username=username).first()
        if not photo:
            flash('Выберите аватар для загрузки!', category='error')
        elif not user:
            flash('Пользователь не существует!', category='error')
        else:
            user.avatar = photo.filename
            db.session.add(user)
            db.session.commit()
            photo_path = path.join('app/static/avatars', f'{current_user.username}_{photo.filename}')
            img = Image.open(photo)
            img.save(photo_path)
            return redirect(url_for('views.user_profile', username=current_user.username))

    return render_template('photo_loader.html', user=current_user)


@views.route('<username>/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    user = User.query.filter_by(username=username).first()
    form = EditProfileForm(user.username, user.email)
    if form.validate_on_submit():
        photo_path = path.join('app/static/avatars', f'{user.username}_{user.avatar}')
        user.username = form.username.data
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        if user.avatar:
            new_photo_path = path.join('app/static/avatars', f'{user.username}_{user.avatar}')
            rename(photo_path, new_photo_path)
        flash('Данные сохранены.')
        return redirect(url_for('views.user_profile', username=user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_profile.html', user=current_user, form=form)


@views.route('/post/<post_id>')
@login_required
def post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    form = CommentForm()
    if not post:
        flash('Пост не найден!', category='error')
    else:
        return render_template('post.html', post=post, user=current_user, form=form)