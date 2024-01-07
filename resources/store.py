from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db

from models import StoreModel
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on Stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}

    def put(self, store_id):
        store_data = request.get_json()
        if "name" not in store_data:
            abort(404, message="'name' should be in the json payload.")
        try:
            store = stores[store_id]
            store |= store_data
            return store
        except KeyError:
            abort(404, message="Item id not found")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        stoer = StoreModel(**store_data)

        try:
            db.session.add(stoer)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exist.")
        except SQLAlchemyError:
            abort(
                500, message="An error occurred while inserting the item to database."
            )

        return stoer
