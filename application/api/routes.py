from flask import Blueprint

mod = Blueprint('api', __name__)


@mod.route('/version')
def version():
    return('{"version": "API 1.0"}')
