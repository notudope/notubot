from telethon.tl.types import MessageEntityPre
from telethon.utils import add_surrogate


def parse_pre(text):
    text = text.strip()
    return (
        text,
        [MessageEntityPre(offset=0, length=len(add_surrogate(text)), language="")],
    )
