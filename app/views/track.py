from flask import Blueprint, request, jsonify
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, jwt_optional, current_user
from sqlalchemy.exc import IntegrityError

from app.exceptions import require_args, ForbiddenAccess
from app.exceptions.models import ResourceNotFound, AlreadyRegistered, RegistrationLimit
from app.database.models import Athlete, College, Track, Registration
from app.database.schemas import TrackSchema, RegistrationSchema
from .__helpers__ import Permision, permission_required

blueprint = Blueprint('track', __name__)


@blueprint.route('/create', methods=['PUT'])
@permission_required(Permision.admin)
@use_kwargs(TrackSchema)
@marshal_with(TrackSchema)
@require_args
def create_track(track_type, sex):
    try:
        track = Track(track_type, sex)
    except IntegrityError:
        raise AlreadyRegistered('track')

    return track


@blueprint.route('/read', methods=['GET'])
@use_kwargs(TrackSchema)
@marshal_with(TrackSchema)
def get_track(track_type, sex):
    return Track.get(track_type=track_type, sex=sex)


@blueprint.route('/register', methods=['PUT'])
@permission_required(Permision.admin, Permision.dm)
@use_kwargs(RegistrationSchema)
@marshal_with(RegistrationSchema)
def register_athlete(athlete_rg, track):
    athlete = Athlete.get(rg=athlete_rg)
    if len(athlete.tracks) == 3:
        raise RegistrationLimit

    user = current_user
    if not user.is_admin() and user.college != athlete.college:
        raise ForbiddenAccess

    track = Track.get(track_type=track, sex=athlete.sex)

    try:
        reg = Registration(athlete, track)
    except IntegrityError:
        raise AlreadyRegistered('athlete on track')

    return reg


@blueprint.route('/all', methods=['GET'])
@marshal_with(TrackSchema(many=True))
def all_tracks(**_):
    return Track.query.all()
