from peewee import *
from base import *
from flask import Flask
from flask_json import jsonify

class State(BaseModel):
    name = CharField(128, null = False, unique = True)

    def to_hash(self):
        return jsonify({'id': self.id,
                        'create_at': self.create_at,
                        'updated_at': self.updated_at,
                        'name': self.name
                        })
