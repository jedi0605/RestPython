import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items
from schemas import ItemSchemas, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on Item")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchemas)
    def get(self, item_id):
        try:
            return items[item_id]
        except:
            abort(404, message="Item id not found")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except:
            abort(404, message="Item id not found")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchemas)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message="Item id not found")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchemas(many=True))
    def get(self):
        return items.values()

    ### blp.arg will check requst's json body is valied. and pass in as item_data
    @blp.arguments(ItemSchemas)
    @blp.response(201, ItemSchemas())
    def post(self, item_data):
        for item in items.values():
            if (
                item["name"] == item_data["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                abort(400, message="Item already exist.")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item, 201
