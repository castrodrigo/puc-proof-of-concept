from flask import Blueprint
from flask import request
from flask import jsonify

from jsonschema import exceptions as jsonschema_exceptions
from jsonschema import validate

from src.common.util import Util
from src.models.subject.subject import Subject
from src.models.subject.exceptions import SubjectNotFoundException

subject_blueprint = Blueprint('subjects', __name__)


@subject_blueprint.route('/<string:id>', methods=['GET'])
def get_subject(id):
    try:
        document = Subject.get_subject_by_id(id)
        return jsonify(document), 200
    except SubjectNotFoundException as e:
        return jsonify(Util.setup_response_body(e.message)), 404


@subject_blueprint.route('/<string:id>', methods=['PUT'])
def put_subject(id):
    try:
        payload = request.get_json()
        validate(payload, Subject.schema)

        subject = Subject(
            name=payload['name'],
            summary=payload['description'],
            script=None if 'script' not in payload else payload['script'],
            total_hours=None if 'total_hours' not in payload else payload['total_hours'],
            id=id
        )
        subject.save()

        return jsonify(), 204
    except jsonschema_exceptions.ValidationError as e:
        return jsonify(Util.setup_response_body(e.message)), 422


@subject_blueprint.route('/', methods=['GET'])
def get_subjects():
    try:
        response = Subject.get_subjects()
        return jsonify(response), 200
    except Exception:
        return jsonify(Util.setup_response_body('Operation not completed')), 500


@subject_blueprint.route('/', methods=['POST'])
def post_subject():
    try:
        payload = request.get_json()
        validate(payload, Subject.schema)

        subject = Subject(
            name=payload['name'],
            summary=payload['description'],
            script=None if 'script' not in payload else payload['script'],
            total_hours=None if 'total_hours' not in payload else payload['total_hours']
        )
        subject.save()

        return jsonify(), 204
    except jsonschema_exceptions.ValidationError as e:
        return jsonify(Util.setup_response_body(e.message)), 422
