from app.search import search
from app.models.movie import Movie, Actor
from app.models.user import User
from app.models.list import CustomList
from app.responses import success_response

from flask import request

SEARCH_PAGE_SIZE = 10


@search.route('/searchmovies', methods=['GET'])
def movie_search():
    q = request.args.get('q', '')

    try:
        page = int(max(0, request.args.get('page', 1)))
    except:
        page = 1

    pagination = Movie.query.search(q).paginate(page=page, per_page=SEARCH_PAGE_SIZE, error_out=False)

    response = {
        'items': [{'title': movie.title, 'poster_path': movie.poster_path} for movie in pagination.items],
        'page_size': SEARCH_PAGE_SIZE,
        'current_page': pagination.page,
        'total_pages': pagination.pages,
        'total_results': pagination.total
    }

    return success_response(**response)


@search.route('/searchactors', methods=['GET'])
def actor_search():
    q = request.args.get('q', '')

    try:
        page = int(max(0, request.args.get('page', 1)))
    except:
        page = 1

    pagination = Actor.query.search(q).paginate(page=page, per_page=SEARCH_PAGE_SIZE, error_out=False)

    response = {
        'items': [{'name': actor.name, 'poster_path': actor.profile_path} for actor in pagination.items],
        'page_size': SEARCH_PAGE_SIZE,
        'current_page': pagination.page,
        'total_pages': pagination.pages,
        'total_results': pagination.total
    }

    return success_response(**response)


@search.route('/searchlists', methods=['GET'])
def list_search():
    q = request.args.get('q', '')

    try:
        page = int(max(0, request.args.get('page', 1)))
    except:
        page = 1

    pagination = CustomList.query.search(q).paginate(page=page, per_page=SEARCH_PAGE_SIZE, error_out=False)

    response = {
        'items': [{'name': l.name, 'owner': l.owner} for l in pagination.items],
        'page_size': SEARCH_PAGE_SIZE,
        'current_page': pagination.page,
        'total_pages': pagination.pages,
        'total_results': pagination.total
    }

    return success_response(**response)


@search.route('/searchusers', methods=['GET'])
def user_search():
    q = request.args.get('q', '')

    try:
        page = int(max(0, request.args.get('page', 1)))
    except:
        page = 1

    pagination = User.query.search(q).paginate(page=page, per_page=SEARCH_PAGE_SIZE, error_out=False)

    response = {
        'items': [{'username': user.username} for user in pagination.items],
        'page_size': SEARCH_PAGE_SIZE,
        'current_page': pagination.page,
        'total_pages': pagination.pages,
        'total_results': pagination.total
    }

    return success_response(**response)


