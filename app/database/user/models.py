from app.database import SurrogatePK, Model, Column
from app.database.fields import String, Binary
from app.extensions import bcrypt
from app.exceptions import ParameterNotModifiable

from .exceptions import InvalidPassword


class User(Model, SurrogatePK):
    __tablename__ = 'users'

    username = Column(String(32), unique=True, nullable=False)
    email = Column(String(48), unique=True, nullable=False, index=True)
    password_hash = Column(Binary(60), unique=True, nullable=False)

    access_token: str = None
    refresh_token: str = None

    # noqa: E303
    def __init__(self, username, email, password):
        Model.__init__(self, username=username, email=email, password=password)
        SurrogatePK.__init__(self)

        self.save()

    @property
    def password(self):
        raise AttributeError('cannot access password directly')

    @password.setter
    def password(self, new_password: str):
        hashed = bcrypt.generate_password_hash(new_password)
        self.password_hash = hashed

    def valid_password(self, password) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    def update(self, old_password, **kwargs):
        if not self.valid_password(old_password):
            raise InvalidPassword

        elif 'username' in kwargs:
            raise ParameterNotModifiable('username')

        super().update(**kwargs)

    def delete(self, password):
        if not self.valid_password(password):
            raise InvalidPassword

        super().delete()

    def __repr__(self):
        return f'<User {self.username}>'
