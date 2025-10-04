# SSD Core Engine - Documentation

[![Python Package](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](https://github.com/HermannDegner/ssd_core_engine)

Hermann DegnerのStructural Subjectivity Dynamics（構造主観力学）理論に関するドキュメント集

**ssd-core-engine** パッケージの開発者・利用者向けドキュメント

## � パッケージ利用者向け

### クイックスタート
```bash
# パッケージのインストール
pip install ssd-core-engine

# 基本的な使用方法
python -c "from ssd_core_engine import SSDCoreEngine; print('インストール成功！')"
```

### APIリファレンス
```python
from ssd_core_engine import SSDCoreEngine
from ssd_core_engine.ssd_types import LayerType, MeaningPressure
from ssd_core_engine.ssd_territory import TerritoryProcessor
```

## �📚 ドキュメント一覧

### `ARCHITECTURE_GUIDELINES.md`
システムアーキテクチャのガイドライン
- パッケージ設計原則
- モジュール依存関係の管理
- 拡張性とメンテナンス性
- パフォーマンス最適化

### `ENHANCED_FEATURES.md`
拡張機能の詳細説明
- 高度なAPI機能の使用方法
- カスタマイズとプラグイン開発
- 実世界での応用事例
- パフォーマンスチューニング

## 🔗 関連リンク

- [メインREADME](../README.md) - パッケージ概要
- [SSD理論リポジトリ](https://github.com/HermannDegner/Structural-Subjectivity-Dynamics) - 理論背景
- [テストスイート](../tests/) - 品質保証
- [デモスクリプト](../scripts/) - 実装例
- [PyPI（将来）](https://pypi.org/project/ssd-core-engine/) - パッケージ配布

## 👥 開発者向け

### パッケージ開発環境
```bash
# 開発用インストール
git clone https://github.com/HermannDegner/ssd_core_engine.git
cd ssd_core_engine
pip install -e .

# テスト実行
python -m pytest tests/

# パッケージビルド
python -m build
```

### 貢献ガイドライン
- プルリクエスト歓迎
- 新機能はテスト付きで
- ドキュメント更新も忘れずに

## 📝 ドキュメント更新

ドキュメントの更新や追加は、このフォルダーで行ってください。
- 理論的背景の詳細な説明
- 実装の技術的詳細
- パッケージAPI仕様
- ユースケース集