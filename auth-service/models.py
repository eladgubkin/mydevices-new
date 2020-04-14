from pony.orm import Database, Required, Optional, PrimaryKey
import uuid
from datetime import datetime

db = Database()


class User(db.Entity):
    _table_ = "users"
    id = PrimaryKey(uuid.UUID)
    email = Required(str, unique=True)
    first_name = Required(str)
    last_name = Required(str)
    created_at = Required(datetime)
    google_userid = Optional(str)
