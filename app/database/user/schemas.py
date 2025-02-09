from app.database.schema import Schema, fields, validate, EnumField
from app.database.user.models import Permision

from app.exceptions import InvalidParameter


class UserSchema(Schema):

    username = fields.String(
        allow_none = False,
        validate   = validate.Length(min=5, max=32)
    )

    permission = EnumField(
        Permision,
        allow_none = False,
        dump_only  = True
    )

    college = fields.String(
        attribute  = 'college_initials',
        allow_none = False,
        validate   = validate.Length(max=10),
        load_only  = True
    )

    password = fields.String(
        allow_none = False,
        load_only  = True
    )
