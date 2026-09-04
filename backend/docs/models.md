# Models 與資料庫 Migration

本專案使用 Flask-SQLAlchemy 定義資料模型，並透過 Flask-Migrate（Alembic）管理 MySQL schema 版本。

## 環境設定

先複製環境變數範例並填入 MySQL 連線資訊：

```powershell
Copy-Item .env.example .env
```

```env
DB_SERVER=127.0.0.1
DB_USER=root
DB_NAME=hackathon
DB_PASSWORD=your_password
```

`DB_SERVER` 也可以包含 port，例如 `127.0.0.1:3307`。`.env` 含有密碼，請勿提交到 Git。

所有指令都使用專案內的 `.venv`：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Model 放置方式

Model 放在 `app/models/`。例如目前的 `User`：

```python
from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    line_user_id = db.Column(
        db.String(64),
        unique=True,
        nullable=False,
        index=True,
    )
    name = db.Column(db.String(100), nullable=True)
```

新增 model 後，記得在 `app/models/__init__.py` 匯入，Flask-Migrate 才能從 SQLAlchemy metadata 偵測它：

```python
from app.models.user import User

__all__ = ["User"]
```

## Migration 基本流程

### 1. 初始化 migration 環境

一個 repository 只需執行一次。本專案已經完成初始化，通常不需要再執行：

```powershell
.\.venv\Scripts\python.exe -m flask --app main db init
```

這會建立 `migrations/`。該目錄必須提交到 Git。

### 2. 產生 migration

每次新增或修改 model 後執行：

```powershell
.\.venv\Scripts\python.exe -m flask --app main db migrate -m "add user email"
```

`migrate` 只會產生 `migrations/versions/` 內的版本檔案，不會直接修改資料庫。

產生後務必人工檢查 `upgrade()` 與 `downgrade()`，尤其是：

- 欄位或 table rename 是否被誤判為刪除後重建
- 新增 `nullable=False` 欄位時，既有資料是否有可用的預設值
- index、unique constraint 和 foreign key 是否正確
- `downgrade()` 是否能安全還原

若 Alembic 顯示 `No changes in schema detected`，請確認新 model 已經由 `app/models/__init__.py` 匯入。

### 3. 套用 migration

將尚未套用的版本更新到最新：

```powershell
.\.venv\Scripts\python.exe -m flask --app main db upgrade
```

此指令會修改 `.env` 指向的 MySQL。執行前請確認目前使用的是正確環境與資料庫。

### 4. 查看 migration 狀態

```powershell
.\.venv\Scripts\python.exe -m flask --app main db current
.\.venv\Scripts\python.exe -m flask --app main db history
.\.venv\Scripts\python.exe -m flask --app main db heads
```

### 5. 回退 migration

回退一個版本：

```powershell
.\.venv\Scripts\python.exe -m flask --app main db downgrade -1
```

回退可能刪除欄位或資料。共享、測試及正式資料庫操作前應先備份並確認 migration 的 `downgrade()`。

## 團隊協作流程

建議每次 model 變更與其 migration 放在同一個 feature／PR 中：

```powershell
git add app/models migrations/versions
git commit -m "feat: add user email field"
```

拉取其他人的 migration 後，不要重新執行 `db init`；直接執行：

```powershell
.\.venv\Scripts\python.exe -m flask --app main db upgrade
```

若多人同時產生 migration 而出現多個 heads，先確認兩邊變更都正確，再建立 merge revision：

```powershell
.\.venv\Scripts\python.exe -m flask --app main db merge heads -m "merge migration heads"
```

## 常見錯誤

### MySQL `Access denied`（1045）

確認 `.env` 的 `DB_USER`、`DB_PASSWORD` 正確，且該帳號允許從目前主機連線。

### `Unknown database`

Flask-Migrate 不會建立 MySQL database 本身。請先建立 `DB_NAME` 指定的 database，再執行 `db upgrade`。

### `Target database is not up to date`

先套用既有 migration，再產生新的版本：

```powershell
.\.venv\Scripts\python.exe -m flask --app main db upgrade
.\.venv\Scripts\python.exe -m flask --app main db migrate -m "describe model change"
```
