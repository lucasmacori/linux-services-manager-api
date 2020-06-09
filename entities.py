from pony.orm import Database, Required, Optional
from config import config
import json


db = Database()
db.bind(config['database'])

class Favorite_service(db.Entity):
    name = Required(str, unique = True)
    service_name = Required(str, unique = True)

class User(db.Entity):
    name = Required(str, unique = True)
    hash = Required(str)
    token = Optional('Token')

class Token(db.Entity):
    user = Required(User)
    token = Required(str)

db.generate_mapping(create_tables=True)