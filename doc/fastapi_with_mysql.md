FastAPI と MySQL を使って **データの取得・更新**を行うには、以下のようなステップで構成するのが一般的です。

---

## ✅ 構成の概要

1. **FastAPI**：Web API フレームワーク
2. **SQLAlchemy**：ORM（または `aiomysql` などの直接接続も可）
3. **MySQL（または MariaDB）**：データベース本体
4. **pymysql または mysqlclient**：DBドライバ

---

## ✅ 例：FastAPI + SQLAlchemy + MySQL で「取得」と「更新」

### 1. 必要なパッケージをインストール

```bash
pip install fastapi uvicorn sqlalchemy pymysql
```

---

### 2. データベース接続設定（`database.py`）

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/test_db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
```

---

### 3. モデル定義（`models.py`）

```python
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=50))
    email = Column(String(length=100))
```

---

### 4. CRUD 操作（例：取得・更新）（`main.py`）

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User

app = FastAPI()

# DB初期化
Base.metadata.create_all(bind=engine)

# DBセッション依存性
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ユーザ取得
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ユーザ更新
@app.put("/users/{user_id}")
def update_user(user_id: int, name: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = name
    db.commit()
    db.refresh(user)
    return user
```

---

### 5. 起動

```bash
uvicorn main:app --reload
```

---

## ✅ 動作確認

- GET `/users/1` → ユーザー取得
- PUT `/users/1?name=NewName` → 名前の更新

---

## ✅ 代替案（補足）

- 非同期で処理したいなら → `databases` パッケージ + `async SQLAlchemy` か `aiomysql`
- ORM不要でSQLだけ使いたい → `pymysql` を直接使う

---

もし「非同期でやりたい」「async/awaitを使った例が見たい」などあれば、そのスタイルでもサンプル出せます！どんな用途で使いたいですか？