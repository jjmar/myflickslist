from app import db
from app.config import DefaultConfig
from app.tmdb.logger import log_message

from time import sleep
import requests

API_KEY = DefaultConfig.TMDB_API_KEY
API_URL = DefaultConfig.TMDB_API_URL
API_ENDPOINTS = {"latest_movie": "movie/latest?api_key={0}",
                 "movie_info": "movie/{1}?api_key={0}&append_to_response=credits,videos",
                 "genre": "genre/movie/list?api_key={0}",
                 "person": "person/{1}?api_key={0}"}


def perform_request(endpoint, resource_id=None):
    request_url = API_URL + API_ENDPOINTS[endpoint].format(API_KEY, resource_id)

    while True:
        log_message('ATTEMPT {} : {}'.format(endpoint, resource_id))
        r = requests.get(request_url)

        if r.status_code == 404:
            log_message('404 {} : {}'.format(endpoint, resource_id))
            return None
        elif r.status_code == 429:
            retry_after = r.headers['Retry-After']
            log_message('429 ({} sec) {} : {}'.format(retry_after, endpoint, resource_id), msg_type='warning')
            sleep(int(retry_after))
            db.session.commit()
        else:
            log_message('200 {} : {}'.format(endpoint, resource_id))
            return r.json()
