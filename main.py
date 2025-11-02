from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from database import engine, create_db_and_tables
from models import User, OTPUser, Message, Group, GroupMember, GroupMessage
from schemas import SignupModel, LoginModel, MessageModel, ProfileUpdateModel
from auth import get_current_user, create_access_token
from utils import hash_password

app = FastAPI()
create_db_and_tables()

from health import router as health_router
app.include_router(health_router)
@app.post("/signup")
def signup(user: SignupModel):
    with Session(engine) as session:
        if session.exec(select(User).where(User.username == user.username)).first():
            raise HTTPException(status_code=400, detail="❌ نام کاربری قبلاً ثبت شده")
        new_user = User(username=user.username, hashed_password=hash_password(user.password), role=user.role)
        session.add(new_user)
        session.commit()
        return {"message": f"✅ ثبت‌نام کاربر {user.username} با نقش {user.role} انجام شد"}
@app.get("/healthz")
def health_check():
    return {"status": "ok ✅"}

@app.post("/login")
def login(user: LoginModel):
    with Session(engine) as session:
        db_user = session.exec(select(User).where(User.username == user.username)).first()
        if not db_user or db_user.hashed_password != hash_password(user.password):
            raise HTTPException(status_code=401, detail="❌ اطلاعات ورود اشتباه است")
        token = create_access_token({"sub": db_user.username, "role": db_user.role})
        return {"access_token": token, "token_type": "bearer", "message": f"🎉 خوش آمدی {db_user.username} با نقش {db_user.role}"}

@app.get("/me")
def me(user=Depends(get_current_user)):
    return {"username": user["username"], "role": user["role"], "message": "📌 این اطلاعات توکن فعلی شماست"}

@app.put("/update_profile")
def update_profile(update: ProfileUpdateModel, user=Depends(get_current_user)):
    with Session(engine) as session:
        db_user = session.exec(select(User).where(User.username == user["username"])).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="کاربر پیدا نشد")
        if update.bio: db_user.bio = update.bio
        if update.theme: db_user.theme = update.theme
        if update.language: db_user.language = update.language
        session.add(db_user)
        session.commit()
        return {"message": "✅ پروفایل با موفقیت به‌روزرسانی شد"}
@app.get("/inbox")
def inbox(user=Depends(get_current_user)):
    with Session(engine) as session:
        messages = session.exec(
            select(Message).where(Message.receiver == user["username"])
        ).all()
        return {
            "inbox": [
                {
                    "from": msg.sender,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat()
                } for msg in messages
            ],
            "count": len(messages)
        }
@app.post("/send_message")
def send_message(msg: MessageModel, user=Depends(get_current_user)):
    with Session(engine) as session:
        receiver_user = session.exec(select(User).where(User.username == msg.receiver)).first()
        if not receiver_user:
            raise HTTPException(status_code=404, detail="❌ گیرنده پیدا نشد")
        new_msg = Message(sender=user["username"], receiver=msg.receiver, content=msg.content)
        session.add(new_msg)
        session.commit()
        return {"message": "✅ پیام با موفقیت ارسال شد"}
from schemas import GroupCreateModel

@app.post("/create_group")
def create_group(data: GroupCreateModel, user=Depends(get_current_user)):
    with Session(engine) as session:
        existing = session.exec(select(Group).where(Group.name == data.name)).first()
        if existing:
            raise HTTPException(status_code=400, detail="❌ نام گروه قبلاً ثبت شده")
        new_group = Group(name=data.name, creator=user["username"])
        session.add(new_group)
        session.commit()
        return {"message": f"✅ گروه {data.name} ساخته شد", "group_id": new_group.id}
from schemas import AddMemberModel

@app.post("/add_member")
def add_member(data: AddMemberModel, user=Depends(get_current_user)):
    with Session(engine) as session:
        group = session.exec(select(Group).where(Group.id == data.group_id)).first()
        if not group:
            raise HTTPException(status_code=404, detail="❌ گروه پیدا نشد")
        if group.creator != user["username"]:
            raise HTTPException(status_code=403, detail="⛔ فقط سازنده گروه می‌تونه عضو اضافه کنه")
        target_user = session.exec(select(User).where(User.username == data.username)).first()
        if not target_user:
            raise HTTPException(status_code=404, detail="❌ کاربر مورد نظر پیدا نشد")
        existing = session.exec(
            select(GroupMember).where(
                (GroupMember.group_id == data.group_id) &
                (GroupMember.username == data.username)
            )
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="⚠️ این کاربر قبلاً عضو گروه شده")
        new_member = GroupMember(group_id=data.group_id, username=data.username)
        session.add(new_member)
        session.commit()
        return {"message": f"✅ کاربر {data.username} به گروه {group.name} اضافه شد"}

@app.post("/create_group")
def create_group(data: GroupCreateModel, user=Depends(get_current_user)):
    with Session(engine) as session:
        existing = session.exec(select(Group).where(Group.name == data.name)).first()
        if existing:
            raise HTTPException(status_code=400, detail="❌ نام گروه قبلاً ثبت شده")
        new_group = Group(name=data.name, creator=user["username"])
        session.add(new_group)
        session.commit()
        return {"message": f"✅ گروه {data.name} ساخته شد", "group_id": new_group.id}
@app.post("/add_member")
def add_member(data: AddMemberModel, user=Depends(get_current_user)):
    with Session(engine) as session:
        group = session.exec(select(Group).where(Group.id == data.group_id)).first()
        if not group:
            raise HTTPException(status_code=404, detail="❌ گروه پیدا نشد")
        if group.creator != user["username"]:
            raise HTTPException(status_code=403, detail="⛔ فقط سازنده گروه می‌تونه عضو اضافه کنه")
        target_user = session.exec(select(User).where(User.username == data.username)).first()
        if not target_user:
            raise HTTPException(status_code=404, detail="❌ کاربر مورد نظر پیدا نشد")
        existing = session.exec(
            select(GroupMember).where(
                (GroupMember.group_id == data.group_id) &
                (GroupMember.username == data.username)
            )
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="⚠️ این کاربر قبلاً عضو گروه شده")
        new_member = GroupMember(group_id=data.group_id, username=data.username)
        session.add(new_member)
        session.commit()
        return {"message": f"✅ کاربر {data.username} به گروه {group.name} اضافه شد"}
@app.post("/send_group_message")
def send_group_message(data: GroupMessage, user=Depends(get_current_user)):
    with Session(engine) as session:
        member = session.exec(
            select(GroupMember).where(
                (GroupMember.group_id == data.group_id) &
                (GroupMember.username == user["username"])
            )
        ).first()
        if not member:
            raise HTTPException(status_code=403, detail="⛔ شما عضو این گروه نیستید")
        msg = GroupMessage(group_id=data.group_id, sender=user["username"], content=data.content)
        session.add(msg)
        session.commit()
        return {"message": "✅ پیام ارسال شد"}
@app.get("/group_inbox/{group_id}")
def group_inbox(group_id: int, user=Depends(get_current_user)):
    with Session(engine) as session:
        member = session.exec(
            select(GroupMember).where(
                (GroupMember.group_id == group_id) &
                (GroupMember.username == user["username"])
            )
        ).first()
        if not member:
            raise HTTPException(status_code=403, detail="⛔ شما عضو این گروه نیستید")
        messages = session.exec(
            select(GroupMessage).where(GroupMessage.group_id == group_id)
        ).all()
        return {
            "group_id": group_id,
            "messages": [
                {
                    "from": msg.sender,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat()
                } for msg in messages
            ],
            "count": len(messages)
        }

@app.get("/test")
def test():
    return {"status": "🧪 تست موفق"}

@app.get("/")
def home():
    return {"message": "✅ سرور Cryptora با موفقیت اجرا شد!"}
