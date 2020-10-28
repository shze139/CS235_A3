from flask import Blueprint,request,render_template,session,flash,redirect,url_for,abort
from app.utilities.forms import ReviewForm
from app.utilities.decorators import login_required
from app.adapters.repository import repo_instance as repo
import app.movie.services as services

bp = Blueprint('movie', __name__, url_prefix='/movie')

@bp.route('/<int:id>', methods=('GET',))
def detail(id):
    reviewForm = ReviewForm(request.form)
    movie = None
    hasWatch = False
    status_code = 200
    try:
        movie = services.get_movie(id, repo)
        username = session.get('username')
        hasWatch = services.has_watch(movie, username, repo)
    except services.MovieNotFoundException:
        status_code = 404
    return render_template('movie.html', movie=movie, reviewForm=reviewForm, hasWatch=hasWatch), status_code

@bp.route('/add_review/<int:movieId>', methods=('POST',))
@login_required
def add_review(movieId):
    form = ReviewForm(request.form)
    if form.validate():
        content = form.content.data
        username = session.get('username')
        try:
            services.add_review(content, username, movieId, repo)
            flash('add review successful', 'is-success')
        except services.MovieNotFoundException:
            return abort(404)
        except services.UserNotFoundException:
            return abort(404)
    else:
        flash('review content cannot be empty', 'is-error')
    return redirect(url_for('movie.detail', id=movieId))

@bp.route('/add_to_watchlist/<int:movieId>', methods=('GET',))
@login_required
def add_to_watchlist(movieId):
    try:
        username = session['username']
        services.add_to_watchlist(username, movieId, repo)
        return redirect(url_for('movie.detail', id=movieId))
    except services.MovieNotFoundException:
        return abort(404)
    except services.UserNotFoundException:
        return abort(404)

@bp.route('/remove_from_watchlist/<int:movieId>', methods=('GET',))
@login_required
def remove_from_watchlist(movieId):
    try:
        username = session['username']
        services.remove_from_watchlist(username, movieId, repo)
        return redirect(url_for('movie.detail', id=movieId))
    except services.MovieNotFoundException:
        return abort(404)
    except services.UserNotFoundException:
        return abort(404)


@bp.route('/watchlist', methods=('GET',))
@login_required
def watchlist():
    username = session['username']
    user = repo.get_user(username)
    return render_template('watchlist.html', watchList=user.watchList)


