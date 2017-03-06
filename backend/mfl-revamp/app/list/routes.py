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
