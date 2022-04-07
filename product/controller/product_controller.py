import bdb
import json

from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from product.models.product_model import Product
from user import db
from user.decorators import token_validate, permission_validate


class ProductControl(MethodView):
    # decorators = [jwt_required()]

    @jwt_required()
    @token_validate
    @permission_validate(role=["supplier"])
    def post(self,current_user):
        current_user = self
        data = json.loads(request.data)
        product = Product(name=data.get('name'),
                          category=data.get('category'),
                          brand=data.get('brand'),
                          price=data.get('price'),
                          user_id=self.id,
                          )
        product.save(current_user)
        db.session.add(product)
        db.session.commit()
        # serialized = json.dumps(product.json_dump())
        return {"message": "product has been created successfully."}

    @jwt_required()
    @token_validate
    @permission_validate(role=["supplier"])
    def get(self,current_user):
        products = Product.query.all()
        res = []
        for product in products:
            product_info = {}
            product_info['id'] = product.id
            product_info['name'] = product.name
            res.append(product_info)
        return jsonify({'list_of_product':res})

    @jwt_required()
    @token_validate
    @permission_validate(role=["supplier"])
    def put(self,current_user,id):
        data = json.loads(request.data)
        price = data.get('price')
        product = Product.query.filter_by(id=id,user_id=self.id).first()
        product.price = price
        db.session.commit()
        return {'message':'updated'}
