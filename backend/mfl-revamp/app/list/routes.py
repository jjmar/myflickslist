from app.list import list
from app.models.list import FlicksList, FlicksListItem, CustomList, CustomListItem
from app.models.movie import Movie
from app.models.user import User
import request_args
from app.responses import error_response, success_response
from app import db

from webargs.flaskparser import use_args
from flask_jwt_extended import jwt_required, get_jwt_identity


@list.route('/createcustomlist', methods=['POST'])
@use_args(request_args.create_custom_list_args, locations=('json',))
@jwt_required
def create_custom_list(args):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return error_response(400, 'User does not exist')

    custom_list = CustomList(name=args['name'], description=args['description'], private=args['private'],
                             owner_id=user_id)

    db.session.add(custom_list)
    db.session.commit()
    return success_response(list_id=custom_list.id)


@list.route('/editcustomlist', methods=['POST'])
@use_args(request_args.edit_custom_list_args, locations=('json',))
@jwt_required
def edit_custom_list(args):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return error_response(400, 'User does not exist')

    custom_list = CustomList.query.get(args['list_id'])

    if not custom_list:
        return error_response(400, 'List does not exist')
    elif custom_list.owner_id != user_id:
        return error_response(400, 'List does not belong to user')

    custom_list.private = args['private']
    custom_list.description = args['description']

    db.session.add(custom_list)
    db.session.commit()

    return success_response()


@list.route('/addcustomlistitem', methods=['POST'])
@use_args(request_args.add_custom_list_item_args)
@jwt_required
def add_custom_list_item(args):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return error_response(400, 'User does not exist')

    movie = Movie.query.get(args['movie_id'])

    if not movie:
        return error_response(400, 'Movie does not exist')

    custom_list = CustomList.query.get(args['list_id'])

    if not custom_list:
        return error_response(400, 'List does not exist')
    elif custom_list.owner_id != user_id:
        return error_response(400, 'List does not belong to user')
    elif movie.id in [item.movie_id for item in custom_list.items]:
        return error_response(400, 'Movie already exists in custom list')

    list_item = CustomListItem(list_id=custom_list.id, movie_id=movie.id, notes=args['notes'])
    movie.num_custom += 1

    db.session.add(list_item)
    db.session.add(movie)
    db.session.commit()

    return success_response()

