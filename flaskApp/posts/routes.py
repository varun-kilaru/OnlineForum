from flask import (render_template, flash, url_for,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskApp import db
from flaskApp.models import Post, Answer
from flaskApp.posts.forms import PostForm, AnswerForm


posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been posted!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')




@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.is_answered:
        answers = Answer.query.order_by(Answer.date_posted.desc()).filter_by(post_id=post_id).all()
    else:
        answers=None
    return render_template('post.html', title=post.title, post=post, answers=answers)




@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and current_user.is_admin==False:
        abort(403)   
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')




@posts.route("/post/<int:post_id>/update_answer", methods=['GET', 'POST'])
@login_required
def update_answer(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and current_user.is_admin==False:
        abort(403)   
    form = AnswerForm()
    if form.validate_on_submit():
        ans = Answer.query.filter_by(post_id=post_id).all()
        for a in ans:
            if current_user.username == a.author.username:
                a.content = form.content.data
        db.session.commit()
        flash('Answer has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id, answer=True))
    elif request.method == 'GET':
        post_title = post.title
        post_data = post.content
        if post.is_answered == True:
            ans = Answer.query.filter_by(post_id=post_id).all()
            for a in ans:
                if current_user.username == a.author.username:
                    form.content.data = a.content
    return render_template('answer_post.html', title='Update Answer',
                           form=form, post_title=post_title, post_data=post_data)




@posts.route("/post/<int:post_id>/answer", methods=['GET', 'POST'])
@login_required
def answer_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and current_user.is_admin==False:
        abort(403)   
    form = AnswerForm()
    if form.validate_on_submit():
        ans = Answer(content=form.content.data, post_id=post.id, user_id=current_user.id)
        db.session.add(ans)
        db.session.commit()
        post.is_answered = True
        db.session.commit()
        flash('Answer has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id, answer=True))
    elif request.method == 'GET':
        post_title = post.title
        post_data = post.content
    return render_template('answer_post.html', title='Answer Post',
                           form=form, post_title=post_title, post_data=post_data)




@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.is_answered == True:
        answers = Answer.query.filter_by(post_id=post_id).all()
    if post.author != current_user and current_user.is_admin==False:
        abort(403)
    db.session.delete(post)
    if post.is_answered == True:
        for ans in answers:
            db.session.delete(ans)
    db.session.commit()
    flash('Post has been deleted!', 'success')
    return redirect(url_for('main.home'))




@posts.route("/post/<int:post_id>/delete_answer", methods=['POST'])
@login_required
def delete_answer(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and current_user.is_admin==False:
        abort(403)
    if post.is_answered == True:
        answers = Answer.query.filter_by(post_id=post_id).all()
        for ans in answers:
            if current_user.username == ans.author.username:
                db.session.delete(ans)
            db.session.commit()
        answers = Answer.query.filter_by(post_id=post_id).all()
        if answers:
            post.is_answered=True
        else:
            post.is_answered=False
        db.session.commit()
    flash('Answer has been deleted!', 'success')
    return redirect(url_for('posts.post', post_id=post_id, answers=answers))