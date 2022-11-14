from typing import TYPE_CHECKING, Optional

from tortoise import fields, models
from tortoise.exceptions import DoesNotExist

if TYPE_CHECKING:
    from apps.accounts.models import User


class ZipCode(models.Model):
    id = fields.IntField(pk=True, index=True)
    code = fields.CharField(max_length=5, unique=True)

    users: fields.ManyToManyRelation['User'] = fields.ManyToManyField(
        'models.User',
        related_name='favourites',
        through='zip_code_favourite',
    )

    @classmethod
    async def get_by_code(cls, code: str) -> Optional['ZipCode']:
        try:
            query = cls.get(code=code)
            zip_code = await query
            return zip_code
        except DoesNotExist:
            return None

    class Meta:
        table = 'zip_codes'
