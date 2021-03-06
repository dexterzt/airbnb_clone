from peewee import *
from base import *
from datetime import datetime

'''
Inherits from BaseModel and update configuration

 Amenity:
    - name: not unique but cannot be blank
'''


class Amenity(BaseModel):
    name = CharField(128, null=False)

    def to_dict(self):
        return {
                'id': self.id,
                'created_at': self.created_at.strftime('%d/%m/%Y %H:%M:%S'),
                'updated_at': self.updated_at.strftime('%d/%m/%Y %H:%M:%S'),
                'name': self.name
                }
