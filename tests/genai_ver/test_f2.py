"""演習F2 解答コードのメモ関数テスト"""

import sys
from pathlib import Path

# srcをインポートパスに追加
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

import pytest
from genai_ver.f2 import save_memo, read_memo, list_memos, MEMO_DIR


@pytest.fixture(autouse=True)
def cleanup_memos():
    """各テスト後にテスト用メモを削除"""
    yield
    for f in MEMO_DIR.glob("test_*.txt"):
        f.unlink(missing_ok=True)


class TestSaveMemo:
    def test_save_success(self):
        result = save_memo("test_save", "テスト内容")
        assert result["status"] == "success"
        assert result["title"] == "test_save"

    def test_saved_file_exists(self):
        save_memo("test_exists", "内容")
        file_path = MEMO_DIR / "test_exists.txt"
        assert file_path.exists()

    def test_saved_content_matches(self):
        save_memo("test_content", "保存テスト内容")
        file_path = MEMO_DIR / "test_content.txt"
        assert file_path.read_text(encoding="utf-8") == "保存テスト内容"


class TestReadMemo:
    def test_read_existing(self):
        save_memo("test_read", "読み取りテスト")
        result = read_memo("test_read")
        assert result["content"] == "読み取りテスト"
        assert result["title"] == "test_read"

    def test_read_nonexistent(self):
        result = read_memo("test_nonexistent_memo_xyz")
        assert result["error"] is not None
        assert result["content"] is None


class TestListMemos:
    def test_list_returns_dict(self):
        result = list_memos()
        assert "titles" in result
        assert "count" in result

    def test_list_includes_saved(self):
        save_memo("test_list_item", "一覧テスト")
        result = list_memos()
        assert "test_list_item" in result["titles"]
        assert result["count"] >= 1
