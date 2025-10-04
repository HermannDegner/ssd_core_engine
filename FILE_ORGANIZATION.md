# SSD Core Engine - ファイル整理計画

## 📁 フォルダー構成

### 🎯 メインディレクトリ (ルート)
**保持するファイル** - コアエンジンの必須ファイル
- `ssd_*.py` - 全てのコアモジュール
- `__init__.py` - パッケージ初期化
- `README.md` - メインドキュメント

### 📚 docs/ - ドキュメント
**移動するファイル**
- `ARCHITECTURE_GUIDELINES.md` - アーキテクチャガイドライン
- `ENHANCED_FEATURES.md` - 拡張機能ドキュメント

### 🧪 tests/ - テスト関連
**移動するファイル**
- `test_ssd.py` - メインテスト
- `test_enhanced_features.py` - 拡張機能テスト
- `test_territory_system.py` - 縄張りシステムテスト

### 📜 scripts/ - ユーティリティスクリプト
**移動するファイル**
- `demo_enhanced.py` - デモスクリプト
- `detailed_territory_test.py` - 縄張り詳細テスト
- `code_check_fix.py` - コードチェックツール
- `final_check.py` - 最終チェックツール

### 🗄️ archive/ - アーカイブ/非推奨
**移動するファイル**
- `README_SPLIT.py` - 分割テスト用（非推奨）

## 🎯 整理後の効果
- メインディレクトリがスッキリ
- 目的別にファイルが分類
- 開発・保守が効率化
- 新規ユーザーが迷わない