try:
    from flask import _app_ctx_stack as ctx_stack
except ImportError:  # pragma: no cover
    from flask import _request_ctx_stack as ctx_stack

from functools import wraps

from flask_jwt_extended.utils import _decode_jwt_from_request, WrongTokenError, check_if_token_revoked, \
                                     get_blacklist_enabled, NoAuthorizationError
from flask_sqlalchemy import Pagination


def jwt_optional(fn):
    """
        Modified jwt_required. Wrap around a view that optionally takes a JWT header.

        :param fn: The view function to decorate
        """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Attempt to decode the token
        try:
            jwt_data = _decode_jwt_from_request(type='access')
        except NoAuthorizationError:
            return fn(*args, **kwargs)

        # Verify this is an access token
        if jwt_data['type'] != 'access':
            raise WrongTokenError('Only access tokens can access this endpoint')

        # If blacklisting is enabled, see if this token has been revoked
        blacklist_enabled = get_blacklist_enabled()
        if blacklist_enabled:
            check_if_token_revoked(jwt_data)

        # Save the jwt in the context so that it can be accessed later by
        # the various endpoints that is using this decorator
        ctx_stack.top.jwt = jwt_data
        return fn(*args, **kwargs)

    return wrapper


def paginate(query, page, per_page):
    """
        Pretty much flask-sqlalchemy's paginate function but can be used with any Query object (instead of just
         BaseQuery)
    """
    items = query.limit(per_page).offset((page - 1) * per_page).all()

    if page == 1 and len(items) < per_page:
        total = len(items)
    else:
        total = query.order_by(None).count()

    return Pagination(query, page, per_page, total, items)

