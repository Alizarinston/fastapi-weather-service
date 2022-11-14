from typing import Optional

from apps.zip_weather.models import ZipCode
from tortoise import fields
from tortoise import models
from tortoise.exceptions import DoesNotExist


class User(models.Model):
    id = fields.IntField(pk=True, index=True)
    username = fields.CharField(max_length=20, unique=True)
    password_hash = fields.CharField(max_length=128, null=True)

    favourites: fields.ManyToManyRelation[ZipCode]

    @classmethod
    async def get_by_username(cls, username: str) -> Optional['User']:
        try:
            query = cls.get(username=username)
            user = await query
            return user
        except DoesNotExist:
            return None

    class Meta:
        table = 'users'
