from app.list import list
from app.models.list import FlicksList, FlicksListItem, CustomList, CustomListItem, Favourite
from app.models.movie import Movie
from app.models.user import User
import request_args
from app.responses import error_response, success_response
from app import db

from webargs.flaskparser import use_args
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func


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

    return success_response(list_item_id=list_item.id)


@list.route('/deletecustomlistitem', methods=['POST'])
@use_args(request_args.delete_custom_list_item_args, locations=('json',))
@jwt_required
def delete_custom_list_item(args):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return error_response(400, 'User does not exist')

    list_item = CustomListItem.query.get(args['list_item_id'])

    if not list_item:
        return error_response(400, 'List item does not exist')
    elif list_item.list.owner_id != user_id:
        return error_response(400, 'Item does not belong to user')

    movie = Movie.query.get(list_item.movie_id)
    movie.num_custom -= 1

    db.session.delete(list_item)
    db.session.add(movie)
    db.session.commit()

    return success_response()


@list.route('/deletecustomlist', methods=['POST'])
@use_args(request_args.delete_custom_list_args, locations=('json',))
@jwt_required
def delete_custom_list(args):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return error_response(400, 'User does not exist')

    custom_list = CustomList.query.get(args['list_id'])

    if not custom_list:
        return error_response(400, 'List does not exist')
    elif custom_list.owner_id != user_id:
        return error_response(400, 'List does not belong to user')

    # Decrement num_custom for each movie in the list
    for item in custom_list.items:
        item.movie.num_custom -= 1

    db.session.delete(custom_list)
    db.session.commit()
    return success_response()


@list.route('/getusercustomlists', methods=['POST'])
@use_args(request_args.get_user_lists_args, locations=('json',))
def get_user_lists(args):
    user = User.query.get(args['user_id'])
    if not user:
        return error_response(400, 'User does not exist')

    custom_lists = db.session.query(CustomList.name, func.count(CustomList.items).label('num_items'))\
                             .filter_by(owner_id=user.id)\
                             .group_by(CustomList.name).all()

    response = [{'name': l.name, 'num_items': l.num_items} for l in custom_lists]

    return success_response(results=response)


@list.route('/getlistdetails', methods=['POST'])
@use_args(request_args.get_list_details_args, locations=('json',))
def get_list_details(args):

    # return all info
    pass


@list.route('/getfavourites', methods=['POST'])
@use_args(request_args.get_favourites_args, locations=('json',))
def get_favourites(args):
    user = User.query.get(args['user_id'])

    if not user:
        return error_response(400, 'User does not exist')

    favourites = db.session.query(Favourite).filter_by()
    response = [{'movie_title': i.title, 'movie_id': i.id, 'ordering': i.ordering} for i in favourites]
    return success_response(results=response)


