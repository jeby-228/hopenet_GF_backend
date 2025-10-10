from enum import StrEnum
from enum import unique


@unique
class TaskStatus(StrEnum):
    working = '工作中'
    done = '已完成'
