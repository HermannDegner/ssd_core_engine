# SSD Core Engine - Scripts

[![Python Package](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](https://github.com/HermannDegner/ssd_core_engine)

**ssd-core-engine** パッケージの開発・デバッグ・デモンストレーション用ユーティリティ集

## 🎯 パッケージ利用者向けスクリプト

### パッケージデモの実行

```bash
# パッケージインストール後
pip install ssd-core-engine

# デモスクリプトの実行
python scripts/demo_enhanced.py
```

## 📜 スクリプト一覧

### `demo_enhanced.py`
パッケージ化された拡張機能のデモ
- パッケージAPIの実用的使用例
- 高度な機能の紹介
- パフォーマンス測定とベンチマーク
- 実世界シナリオのシミュレーション

```python
# 使用例
from ssd_core_engine import SSDCoreEngine
# デモが自動実行されます
```

### `detailed_territory_test.py`
縄張りシステムの詳細分析（パッケージ版）
- パッケージ化された `TerritoryProcessor` のテスト
- 四層構造の動作詳細分析
- 最適化された処理の効果測定
- レイヤーモビリティの調整テスト

```bash
# 実行方法
python scripts/detailed_territory_test.py
```

### `distribution_options.py`
パッケージ配布オプションの分析
- PyPI公開の準備
- 配布形式の比較
- インストール方法の検証
- バージョン管理の確認

### `code_check_fix.py`
パッケージ品質チェックツール
- パッケージ構造の検証
- インポートエラーの自動検出・修正
- コード品質の測定
- 依存関係の確認

### `final_check.py`
パッケージ全体の最終確認
- 全モジュールの正常動作確認
- パッケージビルドの検証
- 統合テストの実行
- 品質スコア計算

## 🛠️ スクリプト使用方法

```bash
# デモ実行
python scripts/demo_enhanced.py

# 縄張り詳細分析
python scripts/detailed_territory_test.py

# コードチェック
python scripts/code_check_fix.py

# 最終確認
python scripts/final_check.py
```

## 🎯 用途

- **開発**: コード品質管理、バグ検出
- **テスト**: 動作確認、性能測定  
- **デモ**: 機能紹介、使用例提示
- **保守**: システムヘルスチェック

スクリプトは独立して実行可能で、メインシステムに影響しません。