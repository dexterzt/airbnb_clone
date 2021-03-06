from peewee import *
from base import *
from user import *
from city import *

'''
 Place:
    - owner: foreign key to User
    - city: foreing key to City
    - name: place name, cannot be empty
    - description: text field for description of place
    - number_rooms: integer with default set to 0, num rooms available
    - number_bathrooms: integer with default set to 0, num restrooms available
    - max_guest: integer with default set to 0, num guests staying
    - price_by_night: integer with default set to 0, price per night
    - latitude: float
    - longitude: float
'''
class Place(BaseModel):
    owner = ForeignKeyField(User, related_name="places")
    city = ForeignKeyField(City, related_name="places")
    name = CharField(128, null=False)
    description = TextField()
    number_rooms = IntegerField(default=0)
    number_bathrooms = IntegerField(default=0)
    max_guest = IntegerField(default=0)
    price_by_night = IntegerField(default=0)
    latitude = FloatField()
    longitude = FloatField()

    def to_dict(self):
        return {'id': self.id,
                'created_at': self.created_at.strftime('%d/%m/%Y %H:%M:%S'),
                'updated_at': self.updated_at.strftime('%d/%m/%Y %H:%M:%S'),
                'owner_id': self.owner.id,
                'city_id': self.city.id,
                'name': self.name,
                'description': self.description,
                'number_rooms': self.number_rooms,
                'number_bathrooms': self.number_bathrooms,
                'max_guest': self.max_guest,
                'price_by_night': self.price_by_night,
                'latitude': self.latitude,
                'longitude': self.longitude
                }
