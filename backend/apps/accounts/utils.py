from typing import Optional

from apps.accounts.models import User
from fastapi import HTTPException


async def get_current_user() -> Optional[User]:
    user = await User.get_by_username(username='admin')
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user
