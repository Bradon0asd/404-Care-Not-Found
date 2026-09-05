# Flask Hackathon Backend

一個適合 Hackathon 快速擴充的 Flask REST API 骨架，採用 App Factory、Service Layer、SQLAlchemy、Marshmallow、webargs 與 LINE Messaging API SDK。

## 快速開始

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
flask --app main db init
flask --app main db migrate -m "create users"
flask --app main db upgrade
flask --app main run --debug
```

若只想快速試跑 SQLite，也可以先略過 migration，在 Flask shell 執行：

```powershell
flask --app main shell
```

```python
from app.extensions import db
db.create_all()
```

## API

完整端點清單、欄位與錯誤碼見 [後端 API 功能清單](backend/docs/api.md)。

- Swagger UI: `GET /api/docs/swagger`
- OpenAPI JSON: `GET /api/docs/openapi.json`

## 測試

```powershell
pytest
```

正式部署前請設定 `DATABASE_URL`、`LINE_CHANNEL_ACCESS_TOKEN`、`LINE_CHANNEL_SECRET`，並關閉 debug mode。
