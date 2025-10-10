import pytest

from app.enums import task_enum


@pytest.mark.parametrize(
    ('status', 'expected'),
    [
        (task_enum.TaskStatus.working, '工作中'),
        (task_enum.TaskStatus.done, '已完成'),
    ],
)
def test_task_enum(*, status: task_enum.TaskStatus, expected: str) -> None:
    assert status == expected
