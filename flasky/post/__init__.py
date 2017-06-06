# -*- coding: utf-8 -*-
from flask import Blueprint

post = Blueprint('post', __name__, url_prefix='/post')

import flasky.post.views
