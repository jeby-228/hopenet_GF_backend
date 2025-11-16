"""
Unit tests for Task model.

This module contains unit tests for the Task model to ensure
proper data validation and model behavior.
"""

import pytest
from datetime import datetime

from app.enums.task_enum import TaskStatus
from app.models.task_model import Task


class TestTaskModel:
    """Test cases for Task model."""

    def test_task_creation_with_minimal_fields(self):
        """Test creating a task with only required fields."""
        task = Task(title='測試任務')

        assert task.title == '測試任務'
        assert task.is_deleted is False
        assert task.weight == 50  # default weight
        assert task.status is None
        assert task.description is None
        assert task.creator_id is None

    def test_task_creation_with_all_fields(self):
        """Test creating a task with all fields populated."""
        start_time = datetime(2025, 1, 1, 10, 0)
        deadline = datetime(2025, 1, 31, 18, 0)

        task = Task(
            title='完整任務',
            status=TaskStatus.working,
            description='這是一個完整的任務描述',
            weight=100,
            start_at=start_time,
            deadline=deadline,
            contact_number='0912-345-678',
            registration_location='報到處',
            work_location='工作地點',
            maximum_number_of_people=20,
            creator_id=1,
        )

        assert task.title == '完整任務'
        assert task.status == TaskStatus.working
        assert task.description == '這是一個完整的任務描述'
        assert task.weight == 100
        assert task.start_at == start_time
        assert task.deadline == deadline
        assert task.contact_number == '0912-345-678'
        assert task.registration_location == '報到處'
        assert task.work_location == '工作地點'
        assert task.maximum_number_of_people == 20
        assert task.creator_id == 1
        assert task.is_deleted is False

    def test_task_default_values(self):
        """Test that default values are correctly set."""
        task = Task(title='預設值測試')

        assert task.title == '預設值測試'
        assert task.weight == 50
        assert task.is_deleted is False
        assert task.deleted_at is None
        assert task.updated_at is None

    def test_task_status_enum(self):
        """Test that task status uses correct enum values."""
        task_working = Task(title='工作中任務', status=TaskStatus.working)
        task_done = Task(title='已完成任務', status=TaskStatus.done)

        assert task_working.status == TaskStatus.working
        assert task_working.status == '工作中'
        assert task_done.status == TaskStatus.done
        assert task_done.status == '已完成'

    def test_task_with_creator(self):
        """Test task with creator_id set."""
        creator_id = 42
        task = Task(title='有建立者的任務', creator_id=creator_id)

        assert task.creator_id == creator_id

    def test_task_optional_fields_are_none(self):
        """Test that optional fields default to None."""
        task = Task(title='最小任務')

        assert task.status is None
        assert task.description is None
        assert task.start_at is None
        assert task.deadline is None
        assert task.contact_number is None
        assert task.registration_location is None
        assert task.work_location is None
        assert task.maximum_number_of_people is None

    def test_task_weight_custom_value(self):
        """Test setting custom weight value."""
        task = Task(title='自訂權重', weight=200)

        assert task.weight == 200

    def test_task_soft_delete_fields(self):
        """Test soft delete related fields."""
        task = Task(title='軟刪除測試')

        assert task.is_deleted is False
        assert task.deleted_at is None

        # Simulate soft delete
        task.is_deleted = True
        task.deleted_at = datetime.now()

        assert task.is_deleted is True
        assert task.deleted_at is not None

    @pytest.mark.parametrize(
        'title,expected_title',
        [
            ('簡單任務', '簡單任務'),
            ('Task with English', 'Task with English'),
            ('任務 123', '任務 123'),
            ('特殊字元 !@#$', '特殊字元 !@#$'),
        ],
    )
    def test_task_title_variations(self, title: str, expected_title: str):
        """Test various title formats."""
        task = Task(title=title)

        assert task.title == expected_title

    def test_task_url_fields(self):
        """Test URL fields for locations."""
        task = Task(
            title='有 URL 的任務',
            registration_location='花蓮縣光復鄉',
            registration_location_url='https://maps.google.com/location1',
            work_location='工作現場',
            work_location_url='https://maps.google.com/location2',
        )

        assert task.registration_location_url == 'https://maps.google.com/location1'
        assert task.work_location_url == 'https://maps.google.com/location2'
