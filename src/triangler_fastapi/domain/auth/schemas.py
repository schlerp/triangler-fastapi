from typing import Self

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import computed_field

from triangler_fastapi.domain import schemas
from triangler_fastapi.domain.auth import hashing


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


class UserCreate(schemas.TrianglerBaseInSchema):
    username: str
    email: str
    password: str
    salt: str = Field(default_factory=hashing.generate_salt)
    roles: list[Role] = Field(default_factory=list)

    @computed_field
    @property
    def hashed_password(self: Self) -> str:
        return hashing.hash_password(password=self.password, salt=self.salt)

    @classmethod
    def create(
        cls: type[Self],
        username: str,
        email: str,
        password: str,
        salt: str | None = None,
    ) -> Self:
        user_create_schema = cls(username=username, email=email, password=password)
        if salt is not None:
            user_create_schema.salt = salt
        return user_create_schema


class User(schemas.TrianglerBaseOutSchema):
    id: int
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
        return self.hashed_password == hashing.hash_password(
            password=password, salt=self.salt
        )

    def password_is_set(self: Self) -> bool:
        """Returns True if the password is set."""
        return bool(self.hashed_password)

    def set_password(self: Self, password: str) -> None:
        """Sets the password for the user."""
        self.hashed_password = hashing.hash_password(password=password, salt=self.salt)
