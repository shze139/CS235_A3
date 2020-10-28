from flask import Blueprint,request,render_template
from app.utilities.forms import SearchForm
from app.adapters.repository import repo_instance as repo

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/', methods=('GET',))
def index():
    form = SearchForm(request.args, meta={'csrf': False})
    data = None
    if form.validate():
        page = form.page.data
        size = form.size.data
        key = form.key.data
        by = form.by.data
        data = repo.search_movies(key, by, page, size)

    return render_template('index.html', data=data, form=form)