from pony.orm import Database, Required
from config import config
import json


db = Database()
db.bind(config['database'])

class Favorite_service(db.Entity):
    name = Required(str, unique = True)
    service_name = Required(str)

db.generate_mapping(create_tables=True)