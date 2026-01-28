"""演習F3 解答コードのタスク管理関数テスト"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

import pytest
from genai_ver import f3


@pytest.fixture(autouse=True)
def clear_tasks():
    """各テスト前にタスクリストをクリア"""
    f3.TASKS.clear()
    yield


class TestAddTask:
    def test_add_returns_success(self):
        result = f3.add_task("テストタスク")
        assert result["status"] == "success"
        assert result["task"] == "テストタスク"
        assert result["index"] == 0

    def test_add_multiple(self):
        f3.add_task("タスク1")
        result = f3.add_task("タスク2")
        assert result["index"] == 1
        assert len(f3.TASKS) == 2


class TestCompleteTask:
    def test_complete_valid(self):
        f3.add_task("完了テスト")
        result = f3.complete_task(0)
        assert result["status"] == "success"
        assert f3.TASKS[0]["done"] is True

    def test_complete_invalid_index(self):
        result = f3.complete_task(99)
        assert "error" in result


class TestListTasks:
    def test_empty_list(self):
        result = f3.list_tasks()
        assert result["total"] == 0
        assert result["completed"] == 0
        assert result["tasks"] == []

    def test_list_with_tasks(self):
        f3.add_task("タスクA")
        f3.add_task("タスクB")
        f3.complete_task(0)
        result = f3.list_tasks()
        assert result["total"] == 2
        assert result["completed"] == 1
        assert result["tasks"][0]["done"] is True
        assert result["tasks"][1]["done"] is False
