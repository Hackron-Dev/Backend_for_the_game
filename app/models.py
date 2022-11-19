from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator


class Users(Model):
    """
    The User model
    """

    id = fields.IntField(pk=True, unique=True)
    login = fields.CharField(max_length=50, null=False)
    password = fields.CharField(max_length=128, null=False)
    mcoin = fields.IntField(null=False)
    rcoin = fields.IntField(null=False)


# Pydantic schemas creating automatically by Tortoise
User_Pydantic = pydantic_model_creator(Users, name="User")
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)


# Class for the shop (9:36)
class Shop(Model):
    id = fields.IntField(pk=True, unique=True)
    name = fields.CharField(max_length=50, null=False)
    description = fields.CharField(max_length=200, null=True)
    price = fields.IntField(null=False)
    image = fields.CharField(max_length=200, null=True)  # image | CharField?
    quantity = fields.IntField(null=True)  # quantity of product


# Pydantic schemas created automatically by [Copilot]
Shop_Pydantic = pydantic_model_creator(Shop, name="Shop")
ShopIn_Pydantic = pydantic_model_creator(Shop, name="ShopIn", exclude_readonly=True)
