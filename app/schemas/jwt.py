from pydantic import BaseModel


class JWTPayloadSchema(BaseModel):
    id: str


class JWTOutSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
