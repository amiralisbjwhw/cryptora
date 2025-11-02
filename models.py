from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

# 🧍‍♂️ مدل کاربر
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    hashed_password: str
    role: str = "user"
    bio: Optional[str] = None
    theme: Optional[str] = "light"
    language: Optional[str] = "fa"
    created_at: datetime = Field(default_factory=datetime.utcnow)

# 📲 مدل OTP برای ثبت‌نام با شماره
class OTPUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    phone_number: str
    otp_code: str
    verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

# 💌 پیام خصوصی بین کاربران
class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sender: str
    receiver: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# 👥 گروه‌ها
class Group(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    creator: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# 👤 اعضای گروه
class GroupMember(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    group_id: int
    username: str

# 💬 پیام‌های گروهی
class GroupMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    group_id: int
    sender: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
