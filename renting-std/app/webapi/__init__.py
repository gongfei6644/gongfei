# -*- coding: utf-8 -*-
# @Desc    :

from flask import Blueprint

api = Blueprint('api', __name__)

from . import std_case_api

from . import statis_case_email_api
