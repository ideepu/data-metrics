from flask import Blueprint, jsonify

# Override pydantic validation error to customize the error to model exception for the consistent error reporting.
from pydantic import ValidationError

from src.exceptions import AppBaseException

error_handlers_blueprint = Blueprint('error_handlers', __name__, url_prefix='/')


@error_handlers_blueprint.app_errorhandler(ValidationError)
def pydantic_validation_exception_handler(error: ValidationError):
    return jsonify({'error': error.errors(include_url=False, include_context=False)}), 400


@error_handlers_blueprint.app_errorhandler(AppBaseException)
def app_exception_handler(error: AppBaseException):
    return jsonify(error.dump()), error.STATUS_CODE


@error_handlers_blueprint.app_errorhandler(Exception)
def global_exception_handler(_error: Exception):
    return jsonify({'error': 'Internal server error'}), 500
