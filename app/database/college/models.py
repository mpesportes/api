from app.database import SurrogatePK, Model, Column, relationship
from app.database.fields import String, LargeBinary
from app.exceptions import protect_params


class College(Model, SurrogatePK):
    __tablename__ = 'colleges'

    name = Column(String(64), unique=True, nullable=False)
    initials = Column(String(5), unique=True, nullable=False, index=True)
    logo = Column(LargeBinary)

    users = relationship('User', backref='users')

    # noqa: E303
    def __init__(self, name, initials, logo=None):
        Model.__init__(self, name=name, initials=initials, logo=logo)
        SurrogatePK.__init__(self)

        self.save()

    def update(self, **kwargs):
        kwargs = {key: val for key, val in kwargs.items() if val}
        super().update(**kwargs)

    def __repr__(self):
        return f'<College {self.name}>'
