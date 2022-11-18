from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator


class Users(Model):
    """
    The User model
    """

    id = fields.IntField(pk=True)
    login = fields.CharField(max_length=50, null=True)
    password = fields.CharField(max_length=128, null=True)


User_Pydantic = pydantic_model_creator(Users, name="User")
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)


