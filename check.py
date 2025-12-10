#!/usr/bin/env python3
"""研修環境チェックスクリプト

このスクリプトを実行して、研修環境が正しくセットアップされているか確認してください。

使い方:
    uv run python check.py
"""

import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def print_header():
    print("=" * 44)
    print("🔍 研修環境チェック")
    print("=" * 44)


def print_footer(success: bool):
    print("=" * 44)
    if success:
        print("🎉 環境構築完了！研修を始めましょう！")
    else:
        print("❌ 問題があります。上記のエラーを確認してください。")
    print("=" * 44)


def check_python_version() -> bool:
    """Pythonバージョンをチェック"""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version.major == 3 and version.minor >= 11:
        print(f"✅ Python バージョン: {version_str}")
        return True
    else:
        print(f"❌ Python バージョン: {version_str}")
        print("   → Python 3.11以上が必要です")
        return False


def check_uv_version() -> bool:
    """uvのバージョンをチェック"""
    try:
        result = subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        version = result.stdout.strip()
        print(f"✅ uv バージョン: {version}")
        return True
    except FileNotFoundError:
        print("❌ uv: インストールされていません")
        print("   → curl -LsSf https://astral.sh/uv/install.sh | sh")
        return False
    except subprocess.CalledProcessError:
        print("❌ uv: バージョン取得に失敗")
        return False


def check_venv() -> bool:
    """仮想環境の存在をチェック"""
    venv_path = Path(".venv")
    if venv_path.exists() and venv_path.is_dir():
        print("✅ 仮想環境: .venv")
        return True
    else:
        print("❌ 仮想環境: 見つかりません")
        print("   → uv sync を実行してください")
        return False


def check_dependencies() -> bool:
    """主要な依存パッケージをチェック"""
    packages = [
        ("google.genai", "google-genai"),
        ("langchain", "langchain"),
        ("pydantic", "pydantic"),
        ("dotenv", "python-dotenv"),
    ]

    all_ok = True
    missing = []

    for module_name, package_name in packages:
        try:
            __import__(module_name)
        except ImportError:
            missing.append(package_name)
            all_ok = False

    if all_ok:
        print("✅ 依存パッケージ: インストール済み")
    else:
        print("❌ 依存パッケージ: 不足しています")
        for pkg in missing:
            print(f"   → {pkg}")
        print("   → uv sync を実行してください")

    return all_ok


def check_env_file() -> bool:
    """環境変数ファイルの存在をチェック"""
    env_path = Path(".env")
    if env_path.exists():
        print("✅ 環境変数ファイル: .env")
        return True
    else:
        print("⚠️  環境変数ファイル: .env が見つかりません")
        print("   → cp .env.example .env を実行してください")
        return True  # Warningなので失敗扱いにしない


def check_api_key() -> bool:
    """Google AI APIキーをチェック"""
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key and api_key != "your_api_key_here":
        print("✅ GOOGLE_API_KEY: 設定済み")
        return True
    else:
        print("❌ GOOGLE_API_KEY: 未設定")
        print("   → .env ファイルに GOOGLE_API_KEY を設定してください")
        print("   → https://aistudio.google.com/apikey で取得できます")
        return False


def main():
    print_header()

    results = [
        check_python_version(),
        check_uv_version(),
        check_venv(),
        check_dependencies(),
        check_env_file(),
        check_api_key(),
    ]

    success = all(results)
    print_footer(success)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
