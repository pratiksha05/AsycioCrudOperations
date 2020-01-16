"""Used to define test cases by creating new """
import unittest
from peewee import *
from models.db import Agent, System
MODELS = [Agent, System]
test_db = SqliteDatabase('test_db')

class TestCases(unittest.TestCase):
    """Test case writing"""

    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

        self.agent = Agent()
        self.system = System()

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()


    async def test_get_by_id(self):
        data = dict(agent_uuid='dff123', register_date='10-01-2020')
        instance = await self.agent.create(**data)

        retrieved = await self.agent.get_by_id(instance.id)

        self.assertEqual(instance, retrieved)
    async def test_create(self):
        data = dict(agent_uuid='dff123', register_date='10-01-2020')

        instance = await self.agent.create(**data)

        self.assertEqual(data, dict(title=instance.agent_uuid, text=instance.register_date))
