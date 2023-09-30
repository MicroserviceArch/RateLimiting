from flaskr.controllers.home import home_bp
from flask import current_app, render_template, request, json, Response
import logging
import os

from flaskr.lib.token_bucket import token_bucket_middleware

rate_limit = 200  # 5 tokens per second
burst_limit = 10  # Burst limit of 10 tokens


@home_bp.before_app_request
def before_request():
    pass


@home_bp.route('/', methods=['GET'])
@token_bucket_middleware(rate_limit, burst_limit)
def index():
    data = {
        "env": os.getenv("FLASK_ENV")
    }
    return render_template('index.html', data=data)
