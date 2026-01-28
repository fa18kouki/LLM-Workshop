"""演習F1 解答コードのツール関数テスト"""

import sys
from pathlib import Path

# srcをインポートパスに追加
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from genai_ver.f1 import calculate, get_current_datetime


class TestCalculate:
    """calculate関数のテスト（安全な数式のみ許可する簡易計算ツール）"""

    def test_basic_addition(self):
        result = calculate("2 + 3")
        assert result["result"] == "5"
        assert result["expression"] == "2 + 3"

    def test_multiplication(self):
        result = calculate("3 * 4")
        assert result["result"] == "12"

    def test_complex_expression(self):
        result = calculate("3 + 5 * 2")
        assert result["result"] == "13"

    def test_division(self):
        result = calculate("10 / 4")
        assert result["result"] == "2.5"

    def test_parentheses(self):
        result = calculate("(2 + 3) * 4")
        assert result["result"] == "20"

    def test_invalid_chars_rejected(self):
        result = calculate("import os")
        assert result["error"] is not None
        assert result["result"] is None

    def test_empty_expression(self):
        result = calculate("")
        assert result["error"] is not None


class TestGetCurrentDatetime:
    def test_returns_all_fields(self):
        result = get_current_datetime()
        assert "date" in result
        assert "time" in result
        assert "datetime" in result
        assert "weekday" in result

    def test_date_format(self):
        result = get_current_datetime()
        parts = result["date"].split("-")
        assert len(parts) == 3
        assert len(parts[0]) == 4

    def test_weekday_is_japanese(self):
        result = get_current_datetime()
        assert result["weekday"] in ["月", "火", "水", "木", "金", "土", "日"]
