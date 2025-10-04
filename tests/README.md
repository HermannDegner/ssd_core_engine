# SSD Core Engine - Test Suite

[![Python Package](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![Test Status](https://img.shields.io/badge/tests-passing-green)](https://github.com/HermannDegner/ssd_core_engine)

**ssd-core-engine** パッケージの品質を保証するためのテストスイート

## 📦 パッケージテストの実行

### インストール後のテスト

```bash
# パッケージのインストール確認
pip install ssd-core-engine

# 基本動作テスト
python -c "
from ssd_core_engine import SSDCoreEngine
engine = SSDCoreEngine(agent_id='test')
print('✅ パッケージ正常動作')
"
```

### 開発者向けテスト実行

```bash
# 開発環境でのテスト実行
python -m pytest tests/ -v

# カバレッジ付きテスト
python -m pytest tests/ --cov=ssd_core_engine

# 特定テストの実行
python -m pytest tests/test_ssd.py::test_engine_initialization
```

## 🧪 テストファイル一覧

### `test_ssd.py`
パッケージ化されたメインエンジンのテスト
- `SSDCoreEngine` クラスの初期化
- パッケージインポートの動作確認
- 基本的なステップ実行
- エラーハンドリング

### `test_enhanced_features.py`
拡張機能のテスト
- 高度なAPI機能の検証
- パフォーマンス測定
- カスタム設定のテスト
- 並列処理の確認

### `test_territory_system.py`
縄張りシステムの専門テスト
- `TerritoryProcessor` の動作確認
- パッケージモジュール間の連携
- 最適化された処理の検証
- レイヤーモビリティの効果測定

## 🚀 テスト実行方法

### 基本的なテスト実行

```bash
# 全テストの実行（推奨）
python -m pytest tests/
python tests/test_enhanced_features.py
python tests/test_territory_system.py

# 全テスト一括実行
python -m pytest tests/
```

## 📊 テスト品質基準

- **基本機能**: 100%動作必須
- **縄張りシステム**: 理論的整合性確認
- **統合テスト**: エラーゼロ

新機能追加時は必ず対応するテストも作成してください。