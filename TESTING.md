# 測試文檔 (Testing Documentation)

## 概述 (Overview)

本專案使用多種測試方法來確保程式碼品質與可靠性：

- **集成測試 (Integration Tests)**: 使用 Hurl 進行 API 端點測試
- **單元測試 (Unit Tests)**: 使用 pytest 進行單元測試（即將實作）
- **測試資料庫 (Test Database)**: 使用獨立的測試資料庫環境

This project uses multiple testing approaches to ensure code quality and reliability:

- **Integration Tests**: API endpoint testing using Hurl
- **Unit Tests**: Unit testing using pytest (to be implemented)
- **Test Database**: Separate test database environment

---

## 目錄結構 (Directory Structure)

```
hopenet_GF_backend/
├── src/
│   └── backend/
│       ├── app/               # 應用程式碼
│       │   ├── models/        # 資料模型
│       │   ├── routers/       # API 路由
│       │   ├── schemas/       # Pydantic schemas
│       │   └── ...
│       └── tests/             # 測試目錄（待建立）
│           ├── __init__.py
│           ├── conftest.py    # pytest 配置與 fixtures
│           ├── unit/          # 單元測試
│           │   ├── test_models.py
│           │   ├── test_schemas.py
│           │   └── ...
│           └── integration/   # 集成測試
│               ├── test_task_api.py
│               ├── test_user_api.py
│               └── ...
├── test.hurl                  # Hurl 集成測試
└── TESTING.md                 # 本文檔
```

---

## 1. Hurl 集成測試 (Hurl Integration Tests)

### 簡介 (Introduction)

Hurl 是一個用於測試 HTTP API 的命令列工具。本專案使用 `test.hurl` 檔案來測試主要的 API 端點。

Hurl is a command-line tool for testing HTTP APIs. This project uses the `test.hurl` file to test main API endpoints.

### 執行測試 (Running Tests)

```bash
# 確保後端服務正在運行
docker-compose up -d

# 運行 Hurl 測試
hurl --test test.hurl

# 或使用自訂變數
hurl --test --variable backend_host=http://localhost:8000 test.hurl
```

### 測試內容 (Test Coverage)

`test.hurl` 涵蓋以下場景：

1. **使用者認證 (User Authentication)**
   - 使用者註冊
   - 登入並取得 JWT token
   - 驗證使用者資訊

2. **任務管理 (Task Management)**
   - 建立任務
   - 查詢單一任務
   - 列表任務（分頁）
   - 更新任務
   - 刪除任務

### 測試範例解析 (Test Example Explanation)

```hurl
# 建立任務
POST {{backend_host}}/api/v1/task
authorization: Bearer {{access_token}}
{"title": "string"}
HTTP 200
[Asserts]
jsonpath "$.id" exists
jsonpath "$.title" == "string"
jsonpath "$.is_deleted" == false
```

此測試：
1. 發送 POST 請求到任務建立端點
2. 使用 Bearer token 認證
3. 傳送包含標題的 JSON body
4. 驗證回應狀態為 200
5. 檢查回應中的特定欄位

---

## 2. Pytest 單元測試 (Pytest Unit Tests)

### 簡介 (Introduction)

Pytest 是 Python 最流行的測試框架，用於撰寫單元測試與集成測試。

Pytest is Python's most popular testing framework for writing unit and integration tests.

### 安裝 (Installation)

```bash
# 使用 uv 安裝開發依賴
cd src/backend
uv sync --dev
```

### 配置 (Configuration)

在 `src/backend/pyproject.toml` 中配置 pytest：

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-v",                    # verbose output
    "--strict-markers",      # 嚴格標記模式
    "--tb=short",           # 短格式追蹤回報
    "--cov=app",            # 程式碼覆蓋率
    "--cov-report=term-missing",
]
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "slow: Slow running tests",
]
```

### 執行測試 (Running Tests)

```bash
# 執行所有測試
uv run pytest

# 執行特定測試檔案
uv run pytest tests/unit/test_models.py

# 執行特定測試函數
uv run pytest tests/unit/test_models.py::test_task_creation

# 執行帶標記的測試
uv run pytest -m unit
uv run pytest -m integration

# 顯示程式碼覆蓋率
uv run pytest --cov=app --cov-report=html
```

---

## 3. 測試最佳實踐 (Testing Best Practices)

### 3.1 單元測試範例 (Unit Test Examples)

#### 測試模型 (Testing Models)

```python
# tests/unit/test_models.py
import pytest
from datetime import datetime
from app.models.task_model import Task
from app.enums.task_enum import TaskStatus


class TestTaskModel:
    """測試 Task 模型"""
    
    def test_task_creation(self):
        """測試任務建立"""
        task = Task(
            title="測試任務",
            status=TaskStatus.working,
            description="這是一個測試任務",
            creator_id=1
        )
        
        assert task.title == "測試任務"
        assert task.status == TaskStatus.working
        assert task.description == "這是一個測試任務"
        assert task.creator_id == 1
        assert task.is_deleted is False
    
    def test_task_default_values(self):
        """測試任務預設值"""
        task = Task(title="簡單任務")
        
        assert task.title == "簡單任務"
        assert task.weight == 50  # 預設權重
        assert task.is_deleted is False
        assert task.status is None
        assert task.description is None
```

#### 測試 Schemas (Testing Schemas)

```python
# tests/unit/test_schemas.py
import pytest
from datetime import datetime
from pydantic import ValidationError
from app.schemas.task_schema import CreateTaskSchema, UpdateTaskSchema
from app.enums.task_enum import TaskStatus


class TestCreateTaskSchema:
    """測試 CreateTaskSchema"""
    
    def test_valid_task_schema(self):
        """測試有效的任務 schema"""
        data = {
            "title": "新任務",
            "status": TaskStatus.working,
            "description": "任務描述",
            "maximum_number_of_people": 10
        }
        
        schema = CreateTaskSchema(**data)
        
        assert schema.title == "新任務"
        assert schema.status == TaskStatus.working
        assert schema.description == "任務描述"
        assert schema.maximum_number_of_people == 10
    
    def test_missing_required_field(self):
        """測試缺少必要欄位"""
        data = {
            "description": "缺少標題"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            CreateTaskSchema(**data)
        
        assert "title" in str(exc_info.value)
    
    def test_invalid_status(self):
        """測試無效的狀態"""
        data = {
            "title": "任務",
            "status": "無效狀態"
        }
        
        with pytest.raises(ValidationError):
            CreateTaskSchema(**data)


class TestUpdateTaskSchema:
    """測試 UpdateTaskSchema"""
    
    def test_partial_update(self):
        """測試部分更新"""
        data = {
            "title": "更新標題"
        }
        
        schema = UpdateTaskSchema(**data)
        
        assert schema.title == "更新標題"
        assert schema.status is None
        assert schema.description is None
```

### 3.2 集成測試範例 (Integration Test Examples)

#### 測試 API 端點 (Testing API Endpoints)

```python
# tests/integration/test_task_api.py
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.models.task_model import Task
from app.models.user_model import User


@pytest.mark.asyncio
class TestTaskAPI:
    """測試任務 API"""
    
    async def test_create_task(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_user: User
    ):
        """測試建立任務"""
        data = {
            "title": "新任務",
            "description": "任務描述",
            "maximum_number_of_people": 5
        }
        
        response = await client.post(
            "/api/v1/task",
            json=data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        json_data = response.json()
        assert json_data["title"] == "新任務"
        assert json_data["description"] == "任務描述"
        assert json_data["creator_id"] == test_user.id
    
    async def test_get_task(
        self,
        client: AsyncClient,
        test_task: Task
    ):
        """測試取得任務"""
        response = await client.get(f"/api/v1/task/{test_task.id}")
        
        assert response.status_code == 200
        json_data = response.json()
        assert json_data["id"] == test_task.id
        assert json_data["title"] == test_task.title
    
    async def test_list_tasks(
        self,
        client: AsyncClient,
        test_tasks: list[Task]
    ):
        """測試列表任務"""
        response = await client.get(
            "/api/v1/task",
            params={"page": 1, "itemsPerPage": 10}
        )
        
        assert response.status_code == 200
        json_data = response.json()
        assert "data" in json_data
        assert "total_count" in json_data
        assert len(json_data["data"]) > 0
    
    async def test_update_task(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_task: Task
    ):
        """測試更新任務"""
        update_data = {
            "title": "更新的標題",
            "status": "已完成"
        }
        
        response = await client.patch(
            f"/api/v1/task/{test_task.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        json_data = response.json()
        assert json_data["title"] == "更新的標題"
        assert json_data["status"] == "已完成"
    
    async def test_delete_task(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_task: Task
    ):
        """測試刪除任務"""
        response = await client.delete(
            f"/api/v1/task/{test_task.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
    
    async def test_unauthorized_access(self, client: AsyncClient):
        """測試未授權存取"""
        data = {"title": "新任務"}
        
        response = await client.post("/api/v1/task", json=data)
        
        # 根據實際的未授權回應調整
        assert response.status_code in [401, 403]
```

### 3.3 測試 Fixtures (Test Fixtures)

```python
# tests/conftest.py
import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel

from app.main import app
from app.dependencies.database_dependency import get_async_session
from app.models.user_model import User
from app.models.task_model import Task


# 測試資料庫 URL
TEST_DATABASE_URL = "postgresql+asyncpg://test_user:test_password@localhost/test_db"


@pytest.fixture(scope="session")
def event_loop():
    """建立事件迴圈"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_engine():
    """建立測試資料庫引擎"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture(scope="function")
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """建立測試資料庫 session"""
    async_session_maker = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="function")
async def client(test_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """建立測試客戶端"""
    async def override_get_async_session():
        yield test_session
    
    app.dependency_overrides[get_async_session] = override_get_async_session
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(test_session: AsyncSession) -> User:
    """建立測試使用者"""
    user = User(
        email="test@example.com",
        hashed_password="hashed_password_here",
        is_active=True,
        is_superuser=False,
        is_verified=False
    )
    
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)
    
    return user


@pytest.fixture
async def auth_headers(test_user: User) -> dict:
    """建立認證標頭"""
    # 這裡需要實作實際的 token 生成邏輯
    # 可能需要從 fastapi-users 取得 token
    token = "test_jwt_token"
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
async def test_task(test_session: AsyncSession, test_user: User) -> Task:
    """建立測試任務"""
    task = Task(
        title="測試任務",
        description="這是一個測試任務",
        creator_id=test_user.id
    )
    
    test_session.add(task)
    await test_session.commit()
    await test_session.refresh(task)
    
    return task


@pytest.fixture
async def test_tasks(test_session: AsyncSession, test_user: User) -> list[Task]:
    """建立多個測試任務"""
    tasks = [
        Task(title=f"任務 {i}", creator_id=test_user.id)
        for i in range(5)
    ]
    
    for task in tasks:
        test_session.add(task)
    
    await test_session.commit()
    
    for task in tasks:
        await test_session.refresh(task)
    
    return tasks
```

---

## 4. 程式碼覆蓋率 (Code Coverage)

### 檢查覆蓋率 (Checking Coverage)

```bash
# 執行測試並生成覆蓋率報告
uv run pytest --cov=app --cov-report=html --cov-report=term

# 開啟 HTML 報告
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### 覆蓋率目標 (Coverage Goals)

- **總體覆蓋率**: 目標 > 80%
- **關鍵模組**: 目標 > 90%
  - Models
  - Schemas
  - Core business logic

---

## 5. 持續集成 (Continuous Integration)

### GitHub Actions

建議在 `.github/workflows/test.yml` 中加入測試流程：

```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:17.6
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      working-directory: src/backend
      run: |
        pip install uv
        uv sync --dev
    
    - name: Run tests
      working-directory: src/backend
      run: |
        uv run pytest --cov=app --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

---

## 6. 測試資料管理 (Test Data Management)

### Factories (使用 Factory Boy)

```python
# tests/factories.py
import factory
from factory import Faker
from app.models.task_model import Task
from app.models.user_model import User
from app.enums.task_enum import TaskStatus


class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    email = Faker('email')
    is_active = True
    is_superuser = False
    is_verified = False


class TaskFactory(factory.Factory):
    class Meta:
        model = Task
    
    title = Faker('sentence', nb_words=4)
    description = Faker('paragraph')
    status = factory.Iterator([TaskStatus.working, TaskStatus.done])
    creator_id = 1
```

使用方式：

```python
def test_with_factory(test_session):
    # 建立單一任務
    task = TaskFactory()
    
    # 建立多個任務
    tasks = TaskFactory.create_batch(5)
```

---

## 7. 常見問題 (FAQ)

### Q: 如何執行特定的測試？
A: 使用 pytest 的過濾功能：
```bash
# 執行特定檔案
uv run pytest tests/unit/test_models.py

# 執行特定類別
uv run pytest tests/unit/test_models.py::TestTaskModel

# 執行特定函數
uv run pytest tests/unit/test_models.py::TestTaskModel::test_task_creation

# 使用關鍵字過濾
uv run pytest -k "task"
```

### Q: 如何跳過慢速測試？
A: 使用標記功能：
```python
@pytest.mark.slow
def test_slow_operation():
    pass

# 跳過慢速測試
uv run pytest -m "not slow"
```

### Q: 如何除錯失敗的測試？
A: 使用以下方式：
```bash
# 詳細輸出
uv run pytest -vv

# 進入 pdb 除錯器
uv run pytest --pdb

# 在第一個失敗時停止
uv run pytest -x

# 顯示本地變數
uv run pytest -l
```

---

## 8. 參考資源 (References)

- [Pytest 官方文檔](https://docs.pytest.org/)
- [FastAPI 測試指南](https://fastapi.tiangolo.com/tutorial/testing/)
- [Hurl 文檔](https://hurl.dev/)
- [SQLModel 測試](https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)

---

## 總結 (Summary)

本專案採用多層次的測試策略：

1. **Hurl 集成測試**：快速驗證 API 端點的基本功能
2. **Pytest 單元測試**：詳細測試個別元件的邏輯
3. **Pytest 集成測試**：測試元件間的互動
4. **持續集成**：自動化測試流程

遵循這些測試實踐可以確保程式碼品質，減少 bug，並提供更好的開發體驗。

This project adopts a multi-layered testing strategy:

1. **Hurl Integration Tests**: Quickly verify basic functionality of API endpoints
2. **Pytest Unit Tests**: Detailed testing of individual component logic
3. **Pytest Integration Tests**: Test interactions between components
4. **Continuous Integration**: Automated testing workflow

Following these testing practices ensures code quality, reduces bugs, and provides a better development experience.
