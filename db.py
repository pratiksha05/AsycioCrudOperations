"""Database defined here."""
import datetime
import uuid
from peewee import *


sq_db = SqliteDatabase("my_db")


class BaseModel(Model):
    """Base model"""

    class Meta:
        database = sq_db

    @staticmethod
    def create_id():
        return str(uuid.uuid4()).replace("-", "")


class Agent(BaseModel):
    """
    Agent table Model
    """

    uuid = CharField(primary_key=True, default=lambda: BaseModel.create_id())
    ip_address = CharField(null=True)
    register_date = DateTimeField(default=datetime.datetime.now)


class System(BaseModel):
    """
    System table Model
    """

    uuid = CharField(primary_key=True, default=lambda: BaseModel.create_id())
    agent_uuid = ForeignKeyField(Agent, null=True)


