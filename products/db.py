from asyncio import get_event_loop
from motor import motor_asyncio
from pymongo import ASCENDING
from umongo import Instance, Document, EmbeddedDocument, fields

from settings import config

HOST = config['mongo']['host']
PORT = config['mongo']['port']
DATABASE = config['mongo']['database']

db = motor_asyncio.AsyncIOMotorClient(HOST, PORT)[DATABASE]
instance = Instance(db)

@instance.register
class Parameter(EmbeddedDocument):
    key = fields.StrField(required=True)
    value = fields.StrField(required=True)


@instance.register
class Product(Document):
    name = fields.StrField(
        required=True
    )
    description = fields.StrField(
        required=True,
        default=""
    )
    parameters = fields.ListField(
        fields.EmbeddedField(Parameter),
        required=True,
        default=[]
    )

async def init_indexes():
    await Product.collection.create_index([("parameters.key", ASCENDING),
                    ("parameters.value", ASCENDING)])
    await Product.collection.create_index([("name", ASCENDING)])

loop = get_event_loop()
loop.run_until_complete(init_indexes())