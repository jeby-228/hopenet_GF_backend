# Tests Directory

This directory contains all pytest tests for the backend application.

## Structure

```
tests/
├── conftest.py              # Pytest configuration and shared fixtures
├── unit/                    # Unit tests
│   ├── test_models.py       # Tests for database models
│   └── test_schemas.py      # Tests for Pydantic schemas
└── integration/             # Integration tests
    └── test_task_api.py     # Tests for Task API endpoints
```

## Running Tests

### All tests
```bash
uv run pytest
```

### Unit tests only
```bash
uv run pytest tests/unit/
```

### Integration tests only
```bash
uv run pytest tests/integration/
```

### Specific test file
```bash
uv run pytest tests/unit/test_models.py
```

### With coverage
```bash
uv run pytest --cov=app --cov-report=html
```

### Verbose output
```bash
uv run pytest -v
```

## Writing Tests

### Unit Test Example

```python
def test_task_creation():
    """Test creating a task with minimal fields."""
    task = Task(title='Test Task')
    assert task.title == 'Test Task'
    assert task.is_deleted is False
```

### Integration Test Example

```python
@pytest.mark.asyncio
async def test_get_task(client: AsyncClient, test_task: Task):
    """Test retrieving a task via API."""
    response = await client.get(f'/api/v1/task/{test_task.id}')
    assert response.status_code == 200
    assert response.json()['id'] == test_task.id
```

## Available Fixtures

See `conftest.py` for all available fixtures:

- `test_engine` - Test database engine
- `test_session` - Test database session
- `client` - HTTP test client
- `test_user` - Test user instance
- `test_superuser` - Test superuser instance
- `test_task` - Single test task
- `test_tasks` - Multiple test tasks
- `auth_headers` - Authentication headers

## Test Markers

```python
@pytest.mark.unit          # Mark as unit test
@pytest.mark.integration   # Mark as integration test
@pytest.mark.slow          # Mark as slow test
```

Run specific markers:
```bash
uv run pytest -m unit
uv run pytest -m integration
```

## More Information

For detailed documentation, see:
- [TESTING.md](../../../TESTING.md) - Complete testing guide (Chinese & English)
- [測試說明.md](../../../測試說明.md) - Quick reference (Chinese)
