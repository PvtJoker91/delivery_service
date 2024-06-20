import datetime

import pytest

from src.apps.tasks.entities import TaskEntity


@pytest.fixture()
def new_task():
    return TaskEntity(
        id=1,
        title="New test task",
        description="Test description",
        author_id=1,
        assignee_ids=[1],
        created_at="10-01-2022"

    )
