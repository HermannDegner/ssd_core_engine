# SSD Core Engine - パッケージ利用ガイド

## 📦 インストール

### PyPI からのインストール（推奨）

```bash
pip install ssd-core-engine
```

### ローカルファイルからのインストール

```bash
# ホイールファイルから
pip install dist/ssd_core_engine-1.0.0-py3-none-any.whl

# ソース配布から
pip install dist/ssd_core_engine-1.0.0.tar.gz

# 開発者モード（編集可能インストール）
pip install -e .
```

## 🚀 基本的な使用方法

### エンジンの初期化

```python
from ssd_core_engine import SSDCoreEngine

# 基本的な初期化
engine = SSDCoreEngine(agent_id="my_agent")

# カスタマイズされた初期化
engine = SSDCoreEngine(
    agent_id="advanced_agent",
    layer_mobility=0.5,  # 縄張り流動性の調整
    initial_energy=100.0
)
```

### 基本的なシミュレーション

```python
# 環境設定
perceived_objects = {
    "food_item_1": 0.8,
    "threat_signal": 0.2,
    "resource_area": 0.6
}

available_actions = [
    "approach",
    "retreat", 
    "investigate",
    "rest"
]

# ステップ実行
result = engine.step(perceived_objects, available_actions)

# 結果の確認
print(f"選択された行動: {result['decision']['chosen_action']}")
print(f"システムエネルギー: {result['system_state']['energy']['E']:.2f}")
print(f"危機レベル: {result['system_state']['crisis_level']:.2f}")
```

## 🧩 モジュール別使用方法

### 縄張りシステム（最適化版）

```python
from ssd_core_engine.ssd_territory import TerritoryProcessor

# 縄張りプロセッサーの作成
territory = TerritoryProcessor(layer_mobility=0.3)

# 縄張り状態の処理
current_state = engine.get_current_state()
territory_result = territory.process(current_state)

print(f"縄張り安定性: {territory_result.stability}")
print(f"領域優先度: {territory_result.priority}")
```

### 意味圧システム

```python
from ssd_core_engine.ssd_meaning_pressure import MeaningPressureSystem

# 意味圧の計算
pressure_system = MeaningPressureSystem()
pressure_value = pressure_system.calculate_pressure(
    current_meaning=0.7,
    target_meaning=0.9,
    context_strength=0.8
)

print(f"意味圧レベル: {pressure_value}")
```

### 予測システム

```python
# 未来状態の予測
prediction = engine.predict_future_state("food_item_1", steps=5)

print(f"予測信頼度: {prediction.confidence}")
print(f"危機発生確率: {prediction.crisis_probability}")
print(f"推奨行動: {prediction.recommended_actions}")
```

## 🔧 高度な設定

### カスタム設定での初期化

```python
from ssd_core_engine import SSDCoreEngine
from ssd_core_engine.ssd_types import LayerType, SystemConfig

# システム設定のカスタマイズ
config = SystemConfig(
    physical_constraints={"max_energy": 150.0},
    biological_drives={"hunger_threshold": 0.3},
    psychological_patterns={"risk_tolerance": 0.7},
    social_context={"cooperation_tendency": 0.6}
)

engine = SSDCoreEngine(
    agent_id="custom_agent",
    config=config,
    layer_mobility=0.4
)
```

### バッチ処理

```python
# 複数エージェントの同時処理
agents = [
    SSDCoreEngine(agent_id=f"agent_{i}")
    for i in range(5)
]

# 並列シミュレーション実行
results = []
for agent in agents:
    result = agent.step(perceived_objects, available_actions)
    results.append(result)

# 統計分析
average_energy = sum(r['system_state']['energy']['E'] for r in results) / len(results)
print(f"平均エネルギー: {average_energy:.2f}")
```

## 📊 モニタリングと診断

### システム健康状態の監視

```python
# ヘルスチェック
health = engine.get_health_status()
print(f"システム状態: {health['status']}")
print(f"CPU使用率: {health['performance']['cpu_usage']:.1f}%")
print(f"メモリ使用量: {health['performance']['memory_mb']:.1f}MB")

# 詳細診断
if health['status'] != 'healthy':
    diagnostics = engine.run_diagnostics()
    print(f"問題箇所: {diagnostics['issues']}")
    print(f"推奨対策: {diagnostics['recommendations']}")
```

### パフォーマンス測定

```python
import time

# ベンチマークテスト
start_time = time.time()

for i in range(1000):
    result = engine.step(perceived_objects, available_actions)

elapsed_time = time.time() - start_time
print(f"1000ステップ実行時間: {elapsed_time:.2f}秒")
print(f"ステップあたり: {elapsed_time/1000*1000:.2f}ms")
```

## 🛠️ トラブルシューティング

### よくある問題と解決方法

#### インポートエラー
```python
try:
    from ssd_core_engine import SSDCoreEngine
    print("パッケージ正常にインストール済み")
except ImportError as e:
    print(f"インストールエラー: {e}")
    print("解決方法: pip install ssd-core-engine")
```

#### メモリ不足
```python
# メモリ使用量の最適化
engine = SSDCoreEngine(
    agent_id="memory_optimized",
    config=SystemConfig(
        memory_management={
            "max_history_size": 100,  # 履歴サイズ制限
            "cleanup_interval": 10,   # 定期クリーンアップ
            "cache_enabled": False    # キャッシュ無効化
        }
    )
)
```

#### パフォーマンス問題
```python
# 高速モード設定
engine = SSDCoreEngine(
    agent_id="performance_mode",
    config=SystemConfig(
        performance_mode={
            "fast_computation": True,
            "reduced_precision": True,
            "parallel_processing": True
        }
    )
)
```

## 🔗 サポートとコミュニティ

- **GitHub Issues**: https://github.com/HermannDegner/ssd_core_engine/issues
- **ドキュメント**: [docs/](../docs/)
- **サンプルコード**: [scripts/](../scripts/)
- **テスト例**: [tests/](../tests/)

## 📈 バージョン情報

現在のパッケージバージョン: **1.0.0**

```python
import ssd_core_engine
print(f"SSD Core Engine バージョン: {ssd_core_engine.__version__}")
```