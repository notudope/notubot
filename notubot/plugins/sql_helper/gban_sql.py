try:
    from notubot.plugins.sql_helper import BASE, SESSION
except ImportError:
    raise AttributeError

from sqlalchemy import Column, String, UnicodeText


class GBan(BASE):
    __tablename__ = "gban"
    user_id = Column(String(14), primary_key=True)
    reason = Column(UnicodeText)

    def __init__(self, user_id, reason=""):
        self.user_id = user_id
        self.reason = reason


GBan.__table__.create(checkfirst=True)


def is_gbanned(user_id):
    try:
        return SESSION.query(GBan).filter(GBan.user_id == str(user_id)).one()
    except BaseException:
        return None
    finally:
        SESSION.close()


def gbaner(user_id, reason):
    adder = GBan(str(user_id), reason)
    SESSION.add(adder)
    SESSION.commit()


def ungbaner(user_id):
    rem = SESSION.query(GBan).get(str(user_id))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def all_gbanned():
    rem = SESSION.query(GBan).all()
    SESSION.close()
    return rem
