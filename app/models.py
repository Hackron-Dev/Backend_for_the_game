from passlib.hash import bcrypt
from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator

from app.utils import jwt_utils


class Users(Model):
    """ The User model"""

    id = fields.IntField(pk=True, unique=True)
    login = fields.CharField(max_length=50, null=False, unique=True)
    password = fields.CharField(max_length=128, null=False)
    balance = fields.IntField(null=False, default=0)
    created_at = fields.DateField(auto_now=True)
    is_admin = fields.BooleanField(null=False, default=False)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)


# Pydantic schemas creating automatically by Tortoise
User_Pydantic = pydantic_model_creator(Users, name="User")
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)


# Class for the shop (9:36)
class Shop(Model):
    """Shops Model"""

    id = fields.IntField(pk=True, unique=True)
    user = fields.ForeignKeyField('models.Users', related_name='shop')  # user_id in db, relate to User
    name = fields.CharField(max_length=50, null=False)
    description = fields.CharField(max_length=200, null=True)
    price = fields.IntField(null=False)
    image = fields.CharField(max_length=200, null=True)
    quantity = fields.IntField(null=True)  # quantity of product


# Pydantic schemas created automatically by [Copilot]
Shop_Pydantic = pydantic_model_creator(Shop, name="Shop")
ShopIn_Pydantic = pydantic_model_creator(Shop, name="ShopIn", exclude_readonly=True)
# TODO Foreign Key for raw user doens work do this