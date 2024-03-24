from datetime import datetime
from typing import Self

from pydantic import BaseModel
from pydantic import ConfigDict

from triangler_fastapi.auth.hashing import hash_password


class LoginPayload(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


class TokenPayload(BaseModel):
    sub: str
    scopes: list[str] = []


class Role(BaseModel):
    name: str
    scopes: list[str]

    model_config = ConfigDict(from_attributes=True)

    def has_scope(self: Self, scope: str) -> bool:
        return scope in self.scopes


class User(BaseModel):
    id: int
    created_at: datetime
    username: str
    email: str
    hashed_password: str
    salt: str
    disabled: bool
    roles: list[Role]

    model_config = ConfigDict(from_attributes=True)

    @property
    def scopes(self: Self) -> list[str]:
        return [x for role in self.roles for x in role.scopes]

    def validate_password(self: Self, password: str) -> bool:
        """Validates the supplied password."""
        return self.hashed_password == hash_password(password=password, salt=self.salt)
