from marshmallow import Schema, pre_load, post_dump
from marshmallow.fields import String, Email, DateTime, Nested
from marshmallow.validate import Length

from app.exceptions import InvalidParameter


class UserSchema(Schema):
    username = String(allow_none=False, validate=Length(min=5, max=32))
    email = Email(required=True, allow_none=False, validate=Length(max=48))

    password = String(allow_none=False, load_only=True)
    old_password = String(allow_none=False, load_only=True)

    # noqa: E303
    @post_dump
    def dump_user(self, data):
        return {'user': data}

    def handle_error(self, error, data):
        field = error.field_name
        message = error.message

        raise InvalidParameter(parameter=field, value=data, error=message)

    class Meta:
        strict = True
