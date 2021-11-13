try:
    from notubot.plugins.sql_helper import BASE, SESSION
except ImportError:
    raise AttributeError

from sqlalchemy import Column, String


class GMute(BASE):
    __tablename__ = "gmute"
    user_id = Column(String(14), primary_key=True)

    def __init__(self, user_id):
        self.user_id = str(user_id)


GMute.__table__.create(checkfirst=True)


def is_gmuted(user_id):
    user = SESSION.query(GMute).get(str(user_id))
    return bool(user)


def gmute(user_id):
    adder = GMute(str(user_id))
    SESSION.add(adder)
    SESSION.commit()


def ungmute(user_id):
    rem = SESSION.query(GMute).get(str(user_id))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()
