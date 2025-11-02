from pydantic import BaseModel

class SignupModel(BaseModel):
    username: str
    password: str
    role: str = "user"

class LoginModel(BaseModel):
    username: str
    password: str

class MessageModel(BaseModel):
    receiver: str
    content: str

class ProfileUpdateModel(BaseModel):
    bio: str | None = None
    theme: str | None = None
    language: str | None = None
class GroupCreateModel(BaseModel):
    name: str
class AddMemberModel(BaseModel):
    group_id: int
    username: str
class GroupCreateModel(BaseModel):
    name: str

class AddMemberModel(BaseModel):
    group_id: int
    username: str

class GroupMessageModel(BaseModel):
    group_id: int
    content: str
