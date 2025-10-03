# 構造主観力学 AIコアエンジン (SSD Core Engine)

[](https://www.python.org/downloads/)
[](https://www.google.com/search?q=./)

このリポジトリは、独自の理論体系\*\*「構造主観力学（Structural Subjectivity Dynamics: SSD）」\*\*を、自律的に思考・行動するAIエージェントとして動作させるためのコアエンジンをPythonで実装したものです。

このエンジンは、単に合理的な判断を下すだけでなく、内部状態（感情や本能に相当）の力学に基づき、安定的（整合的）な振る舞いと、予測困難で創造的（跳躍的）な振る舞いを動的に生み出すことを目的としています。

## 🏛️ 実装されているSSDの主要概念

このエンジンは、SSD理論の以下の核心概念をモジュールとして実装しています。

  * **四層構造モデル (`LayerType`)**: AIの内部状態を、**物理・基層・中核・上層**という動かしにくさの異なる4つの階層で管理します。
  * **意味圧 (`MeaningPressureProcessor`)**: 周囲のオブジェクトを知覚し、それがAIの内部状態に与える影響（意味圧）を計算し、「未処理圧 `E`」として蓄積します。
  * **整合 (`AlignmentProcessor`)**: 過去の経験（整合慣性 `kappa`）に基づき、安定した反応を試みます。
  * **跳躍 (`LeapProcessor`)**: 未処理圧 `E` が閾値を超えた際に、確率的に内部構造を大きく変化させる「跳躍」を実行します。
  * **意思決定 (`DecisionSystem`)**: 現在の内部状態と整合慣性に基づき、最適な行動を選択します。未処理圧が高い場合は、より探索的な行動を取りやすくなります。
  * **未来予測 (`PredictionSystem`)**: 周囲の状況変化を予測し、食料枯渇などの危機を事前に検知します。

## ✨ 主な特徴

  * **基層的色付け (Survival-Driven Behavior)**
    オブジェクトの `survival_relevance`（生存関連度）を自動計算し、意思決定や跳躍のプロセスに強く影響させます。これにより、AIは平時と危機的状況で異なる、より人間らしい振る舞いを見せます。

  * **反応の二段階モデル (Two-Stage Reaction System)**
    刺激に対して、まず本能的な（基層）即時反応が起こり、少し遅れて理性的な（中核・上層）再処理が行われるという、人間らしい反応の時間差をシミュレートします。

  * **動的な学習と適応**
    行動の結果を`ActionEvaluator`が記録・評価し、成功体験を「整合慣性 `kappa`」として蓄積することで、環境に適応し、徐々に賢くなっていきます。

  * **モジュール化された設計**
    理論の各概念が独立したクラスとして実装されており、理解しやすく拡張性に優れた構造になっています。

## 🚀 クイックスタート

このエンジンは、数行のコードで簡単に動作させることができます。

### 1\. 必要なライブラリ

`numpy`が必要です。

```bash
pip install numpy
```

### 2\. 基本的な使用例

以下のコードは、AIエージェントを生成し、10ステップのシミュレーションを実行する基本的な例です。

```python
import random
from ssd_engine import create_ssd_engine, setup_basic_structure
from ssd_utils import create_simple_world_objects

# 1. SSDエンジンの初期化
engine = create_ssd_engine("test_agent_1")
setup_basic_structure(engine)

# 2. シミュレーション用の世界のオブジェクトを作成
world_objects = create_simple_world_objects()

# 3. シミュレーションループを実行
for step_num in range(10):
    print(f"\n--- Step {step_num + 1} ---")
    
    # AIがランダムにオブジェクトを知覚
    perceived_obj = random.choice(world_objects)
    
    # AIが取りうる行動のリスト
    available_actions = ["approach", "avoid", "investigate", "use"]
    
    # エンジンの1ステップを実行し、結果を取得
    result = engine.step([perceived_obj], available_actions)
    
    # 結果の表示
    print(f"Perceived: {perceived_obj.id} (type: {perceived_obj.type})")
    if 'decision' in result:
        print(f"Decision: {result['decision']['chosen_action']}")
    print(f"Energy (E): {result['system_state']['energy']['E']:.2f}")
    
    # もし跳躍が発生したら表示
    if 'leap' in result:
        print(f"🚀 LEAP OCCURRED: {result['leap']['leap_type']}")

# 最終状態の表示
final_state = engine.get_system_state()
print(f"\n=== Final State ===")
print(f"Total decisions: {final_state.cognition['decision_history_length']}")
print(f"Learned patterns: {final_state.cognition['global_kappa_size']}")
```

## 📂 ファイル構成

  * `ssd_engine.py`: 全てのモジュールを統合し、メインの処理サイクルを実行するコアエンジン。
  * `ssd_types.py`: `LayerType`や`ObjectInfo`など、理論の基本となるデータ構造を定義。
  * `ssd_meaning_pressure.py`: 意味圧の計算と未処理圧`E`の管理を担当。
  * `ssd_alignment_leap.py`: 理論の核心である「整合」と「跳躍」の力学を実装。
  * `ssd_decision.py`: 内部状態に基づき、AIの行動選択を行う。
  * `ssd_prediction.py`: 未来の状態を予測し、危機的状況を検知する。
  * `ssd_utils.py`: システムの監視、メンテナンス、テストデータ生成などの補助機能。
  * `test_ssd.py`: 基本的な動作を確認するためのテストスクリプト。
  * `test_enhanced_features.py`: 「二段階反応」など、より高度な機能のテストスクリプト。

## 📖 理論との関係

このコードベースは、別途提供されている構造主観力学の理論ドキュメント群を具現化したものです。理論の理解を深めるため、並行して参照することを推奨します。
