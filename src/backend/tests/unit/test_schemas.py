"""
Unit tests for Task schemas.

This module contains unit tests for task-related Pydantic schemas
to ensure proper data validation and serialization.
"""

import pytest
from datetime import datetime

from pydantic import HttpUrl
from pydantic import ValidationError

from app.enums.task_enum import TaskStatus
from app.schemas.task_schema import CreateTaskSchema
from app.schemas.task_schema import UpdateTaskSchema


class TestCreateTaskSchema:
    """Test cases for CreateTaskSchema."""

    def test_create_task_with_minimal_fields(self):
        """Test creating schema with only required fields."""
        data = {'title': '新任務'}

        schema = CreateTaskSchema(**data)

        assert schema.title == '新任務'
        assert schema.status is None
        assert schema.description is None
        assert schema.weight is None

    def test_create_task_with_all_fields(self):
        """Test creating schema with all fields populated."""
        data = {
            'title': '完整任務',
            'status': TaskStatus.working,
            'description': '詳細描述',
            'weight': 100,
            'start_at': datetime(2025, 1, 1, 10, 0),
            'deadline': datetime(2025, 1, 31, 18, 0),
            'contact_number': '0912-345-678',
            'registration_location': '報到地點',
            'registration_location_url': 'https://maps.google.com/reg',
            'work_location': '工作地點',
            'work_location_url': 'https://maps.google.com/work',
            'maximum_number_of_people': 20,
        }

        schema = CreateTaskSchema(**data)

        assert schema.title == '完整任務'
        assert schema.status == TaskStatus.working
        assert schema.description == '詳細描述'
        assert schema.weight == 100
        assert schema.start_at == datetime(2025, 1, 1, 10, 0)
        assert schema.deadline == datetime(2025, 1, 31, 18, 0)
        assert schema.contact_number == '0912-345-678'
        assert schema.registration_location == '報到地點'
        assert str(schema.registration_location_url) == 'https://maps.google.com/reg'
        assert schema.work_location == '工作地點'
        assert str(schema.work_location_url) == 'https://maps.google.com/work'
        assert schema.maximum_number_of_people == 20

    def test_create_task_missing_required_field(self):
        """Test that missing required field raises ValidationError."""
        data = {'description': '缺少標題'}

        with pytest.raises(ValidationError) as exc_info:
            CreateTaskSchema(**data)

        errors = exc_info.value.errors()
        assert any(error['loc'] == ('title',) for error in errors)

    def test_create_task_invalid_status(self):
        """Test that invalid status raises ValidationError."""
        data = {'title': '任務', 'status': '無效的狀態'}

        with pytest.raises(ValidationError) as exc_info:
            CreateTaskSchema(**data)

        errors = exc_info.value.errors()
        assert any(error['loc'] == ('status',) for error in errors)

    def test_create_task_valid_status_values(self):
        """Test all valid status enum values."""
        for status in [TaskStatus.working, TaskStatus.done]:
            data = {'title': '測試任務', 'status': status}

            schema = CreateTaskSchema(**data)

            assert schema.status == status

    def test_create_task_invalid_url(self):
        """Test that invalid URL raises ValidationError."""
        data = {'title': '任務', 'registration_location_url': 'not-a-valid-url'}

        with pytest.raises(ValidationError) as exc_info:
            CreateTaskSchema(**data)

        errors = exc_info.value.errors()
        assert any(error['loc'] == ('registration_location_url',) for error in errors)

    def test_create_task_valid_urls(self):
        """Test valid URL formats."""
        valid_urls = [
            'http://example.com',
            'https://example.com',
            'https://maps.google.com/location',
            'https://www.openstreetmap.org/search?query=location',
        ]

        for url in valid_urls:
            data = {'title': '任務', 'registration_location_url': url}

            schema = CreateTaskSchema(**data)

            assert str(schema.registration_location_url) == url

    @pytest.mark.parametrize(
        'weight',
        [0, 1, 50, 100, 1000],
    )
    def test_create_task_weight_values(self, weight: int):
        """Test various weight values."""
        data = {'title': '任務', 'weight': weight}

        schema = CreateTaskSchema(**data)

        assert schema.weight == weight

    def test_create_task_datetime_fields(self):
        """Test datetime field validation."""
        start = datetime(2025, 1, 1, 9, 0)
        end = datetime(2025, 1, 1, 17, 0)

        data = {'title': '任務', 'start_at': start, 'deadline': end}

        schema = CreateTaskSchema(**data)

        assert schema.start_at == start
        assert schema.deadline == end


class TestUpdateTaskSchema:
    """Test cases for UpdateTaskSchema."""

    def test_update_task_empty(self):
        """Test creating empty update schema (all fields optional)."""
        data = {}

        schema = UpdateTaskSchema(**data)

        assert schema.title is None
        assert schema.status is None
        assert schema.description is None

    def test_update_task_partial_fields(self):
        """Test updating only specific fields."""
        data = {'title': '更新的標題', 'status': TaskStatus.done}

        schema = UpdateTaskSchema(**data)

        assert schema.title == '更新的標題'
        assert schema.status == TaskStatus.done
        assert schema.description is None
        assert schema.weight is None

    def test_update_task_all_fields(self):
        """Test updating all fields."""
        data = {
            'title': '更新任務',
            'status': TaskStatus.done,
            'description': '更新的描述',
            'weight': 75,
            'start_at': datetime(2025, 2, 1, 10, 0),
            'deadline': datetime(2025, 2, 28, 18, 0),
            'contact_number': '0923-456-789',
            'registration_location': '新報到地點',
            'registration_location_url': 'https://maps.google.com/new-reg',
            'work_location': '新工作地點',
            'work_location_url': 'https://maps.google.com/new-work',
            'maximusm_number_of_people': 30,  # Note: typo in original schema
        }

        schema = UpdateTaskSchema(**data)

        assert schema.title == '更新任務'
        assert schema.status == TaskStatus.done
        assert schema.description == '更新的描述'
        assert schema.weight == 75
        assert schema.maximusm_number_of_people == 30

    def test_update_task_status_change(self):
        """Test changing task status."""
        # From working to done
        data = {'status': TaskStatus.done}

        schema = UpdateTaskSchema(**data)

        assert schema.status == TaskStatus.done

    def test_update_task_clear_optional_field(self):
        """Test setting optional field to None."""
        data = {'description': None, 'contact_number': None}

        schema = UpdateTaskSchema(**data)

        assert schema.description is None
        assert schema.contact_number is None

    def test_update_task_invalid_status(self):
        """Test that invalid status raises ValidationError."""
        data = {'status': '錯誤狀態'}

        with pytest.raises(ValidationError) as exc_info:
            UpdateTaskSchema(**data)

        errors = exc_info.value.errors()
        assert any(error['loc'] == ('status',) for error in errors)

    def test_update_task_invalid_url(self):
        """Test that invalid URL raises ValidationError."""
        data = {'work_location_url': 'invalid-url'}

        with pytest.raises(ValidationError) as exc_info:
            UpdateTaskSchema(**data)

        errors = exc_info.value.errors()
        assert any(error['loc'] == ('work_location_url',) for error in errors)

    @pytest.mark.parametrize(
        'field,value',
        [
            ('title', '新標題'),
            ('description', '新描述'),
            ('contact_number', '0912-111-222'),
            ('registration_location', '新地點'),
            ('work_location', '新工作地點'),
            ('weight', 150),
        ],
    )
    def test_update_task_individual_fields(self, field: str, value):
        """Test updating individual fields."""
        data = {field: value}

        schema = UpdateTaskSchema(**data)

        assert getattr(schema, field) == value
