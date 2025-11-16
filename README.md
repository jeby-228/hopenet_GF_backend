# 光復 e 互助平台

一個專為花蓮光復鄉災害應變設計的數位互助平台，透過高效、可靠的數位平台優化災害應變流程。

## 專案概述

我們的願景是透過高效、可靠的數位平台，徹底優化花蓮光復鄉的災害應變流程。我們相信準確的數據是救災成功的基石。團隊目標是將複雜的物資需求與緊急通報系統整合簡化，讓工程師的技術專長與在地聯繫窗口的溝通能力發揮最大效用，確保在極端條件下，救援資訊的傳遞零延誤、高效率。

## 主要功能

- **任務管理系統**：支援清理、救援、物資配送、醫療支援、收容所支援等任務類型
- **志工協調**：志工報名、任務分配、進度追蹤
- **權限管理**：基於角色的存取控制
- **即時通知**：任務狀態更新與緊急通知
- **響應式設計**：支援桌面與行動裝置

## 技術棧

- **資料庫**: postgres:17.6
- **後端框架**: fastapi v0.118.0 + fastcrud v0.17.0
- **Server Gateway Interface**: uvicorn v0.37.0
- **Object–relational mapping**: sqlmodel v0.0.25 + alembic v1.16.5
- **資料驗證**: pydantic v2.11.9
- **設定管理**: pydantic-settings v2.11.0
- **使用者認證**：fastapi-users v14.0.1

## 快速開始

### 環境需求

- Docker Compose (參考版本 v2.36.2)

### 開發環境

- 將 `.env.common` + `.env.dev` + `.env.dev-secrets` 內容複製依序合併至 `.env` ，給。Docker Compose `本身 (非服務的 env file)` 使用

- 啟動服務:

```sh
docker-compose up -d
```

- migrate database

```sh
docker-compose run --rm backend uv run alembic upgrade head
```

- 開啟 [http://localhost:8000/docs](http://localhost:8000/docs) 查看 API 文檔

## 專案結構

```sh
├── data                            # 臨時資料
├── src
│   └── backend
│       ├── alembic
│       │   ├── versions
│       │   ├── env.py
│       │   └── script.py.mako
│       ├── app
│       │   ├── dependencies
│       │   ├── enums
│       │   ├── models
│       │   ├── routers
│       │   ├── schemas
│       │   ├── settings
│       │   ├── __init__.py
│       │   ├── logger.py
│       │   └── main.py
│       ├── tests                   # 測試目錄
│       │   ├── unit               # 單元測試
│       │   ├── integration        # 集成測試
│       │   └── conftest.py        # pytest 配置
│       ├── alembic.ini
│       ├── dev.py
│       ├── Dockerfile
│       ├── pyproject.toml
│       └── uv.lock
├── compose.override.dev.yml
├── compose.override.prod.yml
├── compose.yml
├── test.hurl                       # Hurl 集成測試
└── TESTING.md                      # 測試文檔
```

## 測試

本專案使用多種測試方法來確保程式碼品質：

### Hurl 集成測試

快速測試 API 端點：

```sh
# 確保後端服務正在運行
docker-compose up -d

# 執行 Hurl 測試
hurl --test test.hurl
```

### Pytest 單元測試與集成測試

```sh
cd src/backend

# 安裝測試依賴
uv sync --dev

# 執行所有測試
uv run pytest

# 執行特定測試
uv run pytest tests/unit/          # 只執行單元測試
uv run pytest tests/integration/   # 只執行集成測試

# 執行帶覆蓋率報告
uv run pytest --cov=app --cov-report=html
```

詳細測試文檔請參閱 [TESTING.md](TESTING.md)。
