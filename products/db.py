from motor import motor_asyncio
from pymongo import ASCENDING
from umongo import ( 
    Instance,
    MotorAsyncIOInstance,
    Document,
    EmbeddedDocument,
    fields
)

from settings import config


instance = MotorAsyncIOInstance()


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

    class Meta:
        indexes = ("name", ("parameters.key", "parameters.value"))
        collection_name = "products"


async def init_mongo(app):
    host = config['mongo']['host']
    port = config['mongo']['port']
    database = config['mongo']['database']

    con = motor_asyncio.AsyncIOMotorClient(host, port)
    instance.init(con[database])

    app['db_con'] = con

    await Product.ensure_indexes()


async def close_mongo(app):
    app['db_con'].close()
