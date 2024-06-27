from .ponding import ponding_api
from .summary import summary_api 
from .task import task_api
from .channel import channel_api
from .get_location import get_location
from .format_time import format_datetime
from .task_function import format_value, task_function_result
from flask import Blueprint

function_api = Blueprint("function", __name__, url_prefix='/function')

function_api.register_blueprint(ponding_api)
function_api.register_blueprint(summary_api)
function_api.register_blueprint(task_api)
function_api.register_blueprint(channel_api)