from pony.orm import Required, Optional, PrimaryKey, Database
import uuid
from datetime import datetime

db = Database()


class User(db.Entity):
    _table_ = "users"
    id = PrimaryKey(uuid.UUID)
    email = Required(str, unique=True)
    first_name = Optional(str, nullable=True)
    last_name = Optional(str, nullable=True)
    created_at = Required(datetime)
    google_userid = Optional(str)
