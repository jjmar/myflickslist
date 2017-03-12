from app.list import list
from app.models.list import FlicksList, FlicksListItem, CustomList, CustomListItem, Favourite
from app.models.movie import Movie
from app.models.user import User
import request_args
from app.responses import error_response, success_response
from app import db
from app.util import jwt_optional

from webargs.flaskparser import use_args
from flask_jwt_extended import jwt_required, get_jwt_identity, get_raw_jwt
from sqlalchemy import func
from sqlalchemy.orm import joinedload


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

    movies = db.session.query(Movie).join(CustomListItem).filter_by(list_id=custom_list.id).all()

    # Decrement num_custom for each movie in the list
    for movie in movies:
        movie.num_custom -= 1

    db.session.delete(custom_list)
    db.session.commit()
    return success_response()


@list.route('/getcustomlists', methods=['POST'])
@use_args(request_args.get_custom_lists_args, locations=('json',))
def get_custom_lists(args):
    user = User.query.get(args['user_id'])
    if not user:
        return error_response(400, 'User does not exist')

    custom_lists = db.session.query(CustomList.name, func.count(CustomListItem.id).label('num_items'))\
                             .outerjoin(CustomListItem)\
                             .filter(CustomList.owner_id == user.id)\
                             .group_by(CustomList.name).all()

    response = {
        'items': [{'name': l.name, 'num_items': l.num_items} for l in custom_lists]
    }

    return success_response(**response)


@list.route('/addfavourite', methods=['POST'])
@use_args(request_args.add_favourite_item_args, locations=('json',))
@jwt_required
def add_favourite_item(args):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return error_response(400, 'User does not exist')

    movie = Movie.query.get(args['movie_id'])

    if not movie:
        return error_response(400, 'Movie does not exist')
    elif args['movie_id'] in [fav.movie_id for fav in user.favourites]:
        return error_response(400, 'Movie already exists in favourites')
    elif len(user.favourites) >= 4:
        return error_response(400, 'Maximum allowable number of favourites reached (4)')

    movie.num_favourites += 1
    fav = Favourite(movie_id=args['movie_id'], user_id=user_id)

    db.session.add(fav)
    db.session.commit()
    return success_response()


@list.route('/getfavourites', methods=['POST'])
@use_args(request_args.get_favourites_args, locations=('json',))
def get_favourites(args):
    user = User.query.get(args['user_id'])

    if not user:
        return error_response(400, 'User does not exist')

    favourites = db.session.query(Movie.title, Movie.id, Favourite.ordering)\
                           .join(Favourite)\
                           .filter_by(user_id=user.id).all()

    response = {
        'num_items': len(favourites),
        'items': [{'movie_title': i.title, 'movie_id': i.id, 'ordering': i.ordering} for i in favourites]
    }

    return success_response(**response)


@list.route('/removefavourite', methods=['POST'])
@use_args(request_args.remove_favourite_item_args)
@jwt_required
def remove_favourites_item(args):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return error_response(400, 'User does not exist')

    fav_movie = db.session.query(Favourite, Movie).join(Movie)\
                          .filter(Favourite.user_id == user_id)\
                          .filter(Favourite.movie_id == args['movie_id']).first()

    if not fav_movie:
        return error_response(400, 'Favourite does not exist')

    favourite, movie = fav_movie

    movie.num_favourites -= 1

    db.session.delete(favourite)
    db.session.commit()
    return success_response()


@list.route('/addflickslistitem', methods=['POST'])
@use_args(request_args.add_flicks_list_item_args, locations=('json',))
@jwt_required
def add_flicks_list_item(args):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return error_response(400, 'User does not exist')

    movie = Movie.query.get(args['movie_id'])

    if not movie:
        return error_response(400, 'Movie does not exist')

    flicks_list = FlicksList.query.filter_by(owner_id=user_id).options(joinedload('items')).first()

    if movie.id in [i.movie_id for i in flicks_list.items]:
        return error_response(400, 'Item already present in user list')

    if args['completed']:
        list_item = FlicksListItem(list_id=flicks_list.id, movie_id=movie.id, rating=args['rating'],
                                   completed=True, notes=args['notes'], completion_date=args['completion_date'])
        movie.add_completed_member(rating=args['rating'])

    else:
        list_item = FlicksListItem(list_id=flicks_list.id, movie_id=movie.id, notes=args['notes'])
        movie.add_ptw_member()

    db.session.add(list_item)
    db.session.commit()
    return success_response(list_item_id=list_item.id)


@list.route('/removeflickslistitem', methods=['POST'])
@use_args(request_args.remove_flicks_list_item_args, locations=('json',))
@jwt_required
def remove_flicks_list_item(args):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return error_response(400, 'User does not exist')

    list_item_movie = db.session.query(FlicksList, FlicksListItem, Movie)\
                                .join(FlicksListItem)\
                                .join(Movie)\
                                .filter(FlicksList.owner_id == user_id)\
                                .filter(FlicksListItem.id == args['list_item_id']).first()

    if not list_item_movie:
        return error_response(400, 'Item does not exist')

    flickslist, list_item, movie = list_item_movie

    if list_item.completed:
        movie.remove_completed_member(rating=list_item.rating)
    else:
        movie.remove_ptw_member()

    db.session.delete(list_item)
    db.session.commit()
    return success_response()


@list.route('/getflickslistdetails', methods=['POST'])
@use_args(request_args.get_flicks_list_details_args, locations=('json',))
def get_flicks_list_details(args):
    user = User.query.get(args['user_id'])

    if not user:
        return error_response(400, 'User does not exist')

    flickslist = db.session.query(FlicksList)\
                           .options(joinedload('items').joinedload('movie'))\
                           .filter(FlicksList.owner_id == user.id).first()

    response = {}

    for k, v in flickslist.get_list_details().iteritems():
        response[k] = v

    return success_response(results=response)


@list.route('/getcustomlistdetails', methods=['POST'])
@use_args(request_args.get_custom_list_details_args, locations=('json',))
@jwt_optional
def get_custom_list_details(args):

    custom_list = db.session.query(CustomList)\
                            .options(joinedload('items').joinedload('movie'))\
                            .filter(CustomList.id == args['list_id']).first()

    if not custom_list:
        return error_response(400, 'List does not exist')
    elif custom_list.private and custom_list.owner_id != get_jwt_identity():
        return error_response(400, 'List does not exist')

    response = custom_list.get_list_details()

    return success_response(**response)

# TODO Stubs

def edit_custom_list_item():
    pass

def edit_flicks_list_item():
    pass