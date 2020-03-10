
import json
import re
import marshmallow
import status
from aiohttp import web
from bson.objectid import ObjectId

from db import Product

routes = web.RouteTableDef()


@routes.view("/products/{id}")
class ProductDetailView(web.View):
    async def get(self):
        try:
            product = await Product.find_one({
                '_id': ObjectId(self.request.match_info['id'])
            })
            return web.json_response({
                "data": product.dump()
            })
        except:
            return web.json_response({
                "message": "Product not found."
            }, status=status.HTTP_404_NOT_FOUND)


@routes.view("/products/")
class ProductsView(web.View):
    async def get(self):
        try:
            limit = self.request.query.get("limit", None)
            offset = self.request.query.get("offset", None)

            query = {
                "$and": []
            }

            name = self.request.query.get("name", None)
            if name:
                query["$and"].append({
                    "name": name
                })

            for q, v in self.request.query.items():
                param_search = re.search(r"^parameters\[(.+)\]", q)
                if param_search:
                    parameter = param_search.group(1)
                    query["$and"].append({
                        "parameters": {
                            "$elemMatch": {"key": parameter, "value": v}
                        }
                    })

            products_cursor = Product.find(
                query if query["$and"] else None
            )

            if offset:
                products_cursor.skip(int(offset))
            if limit:
                products_cursor.limit(int(limit))

            product_list = []
            async for product in products_cursor:
                product_list.append({
                    "id": str(product.pk),
                    "name": product.name
                })

            return web.json_response({
                "data": product_list
            })
        except:
            return web.json_response({
                "message": "Unknown error."
            }, status=status.HTTP_400_BAD_REQUEST)

    async def post(self):
        try:
            product = await self.request.json()
            product = Product(**product)

            await product.commit()

            return web.json_response({
                "data": product.dump()
            }, status=status.HTTP_201_CREATED)
        except json.decoder.JSONDecodeError:
            return web.json_response({
                "message": "Syntax error in the request body."
            }, status=status.HTTP_400_BAD_REQUEST)
        except marshmallow.exceptions.ValidationError as e:
            return web.json_response({
                "message": e.messages
            }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return web.json_response({
                "message": "Unknown error."
            }, status=status.HTTP_400_BAD_REQUEST)
