# SSD Core Engine - Tests

システムの品質を保証するためのテストスイート

## 🧪 テストファイル一覧

### `test_ssd.py`
メインエンジンの基本機能テスト
- エンジンの初期化
- 構造要素の追加
- 整合・跳躍処理
- 決定システム

### `test_enhanced_features.py`
拡張機能のテスト
- 高度なアルゴリズムの検証
- パフォーマンステスト
- エラーハンドリング

### `test_territory_system.py`
縄張りシステムの専門テスト
- 縄張り形成メカニズム
- 四層構造統合
- 整合慣性の動作確認

## 🚀 テスト実行方法

```bash
# 個別テスト実行
python tests/test_ssd.py
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