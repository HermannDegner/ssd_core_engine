"""
SSD Test and Example Usage
構造主観力学 - テスト・使用例
"""

import random
import sys
import os

# モジュールパスを追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ssd_engine import create_ssd_engine, setup_basic_structure
from ssd_utils import create_simple_world_objects, create_survival_scenario_objects


def run_basic_test():
    """基本テストの実行"""
    print("=== SSD Core Engine Basic Test ===")
    
    # エンジン初期化
    engine = create_ssd_engine("test_agent_1")
    setup_basic_structure(engine)
    
    # シンプルな世界のオブジェクト
    world_objects = create_simple_world_objects()
    
    # シミュレーション実行
    for step_num in range(10):
        print(f"\n--- Step {step_num + 1} ---")
        
        # ランダムにオブジェクトを知覚
        perceived = [random.choice(world_objects)]
        actions = ["approach", "avoid", "investigate", "use"]
        
        result = engine.step(perceived, actions)
        
        print(f"Perceived: {perceived[0].id} (type: {perceived[0].type})")
        if 'decision' in result:
            print(f"Decision: {result['decision']['chosen_action']}")
        print(f"Energy (E): {result['system_state']['energy']['E']:.2f}")
        print(f"Temperature (T): {result['system_state']['energy']['T']:.2f}")
        
        if 'leap' in result:
            print(f"🚀 LEAP OCCURRED: {result['leap']['leap_type']}")
            print(f"   Affected layers: {result['leap']['affected_layers']}")
            print(f"   Survival driven: {result['leap']['survival_driven']}")
    
    # 最終状態
    print(f"\n=== Final State ===")
    final_state = engine.get_system_state()
    print(f"Total decisions: {final_state.cognition['decision_history_length']}")
    print(f"Learned patterns: {final_state.cognition['global_kappa_size']}")
    
    # パフォーマンス指標の表示
    performance = engine.get_performance_metrics()
    print(f"Cognitive Load: {performance.get('cognitive_metrics', {}).get('cognitive_load', 0):.3f}")
    
    # ヘルスチェック
    health = engine.get_health_status()
    print(f"System Health: {health['status']}")
    if health['warnings']:
        print(f"Warnings: {len(health['warnings'])}")


def run_survival_scenario_test():
    """生存シナリオテストの実行"""
    print("\n\n=== SSD Survival Scenario Test ===")
    
    # エンジン初期化
    engine = create_ssd_engine("survival_agent")
    setup_basic_structure(engine)
    
    # 生存シナリオのオブジェクト
    crisis_objects = create_survival_scenario_objects()
    
    # 危機検出テスト
    for obj in crisis_objects:
        engine.perceive_object(obj)
    
    crisis_report = engine.detect_crisis_conditions()
    print(f"Crisis detected: {crisis_report['crisis_detected']}")
    print(f"Crisis level: {crisis_report['crisis_level']}")
    print(f"Objects in crisis: {crisis_report['objects_in_crisis']}")
    print(f"Cooperation urgency: {crisis_report['cooperation_urgency']:.2f}")
    
    # 生存行動のテスト
    survival_actions = ["drink", "seek_shelter", "craft", "gather", "rest"]
    
    for step_num in range(5):
        print(f"\n--- Survival Step {step_num + 1} ---")
        
        result = engine.step([], survival_actions)
        
        if 'decision' in result:
            action = result['decision']['chosen_action']
            scores = result['decision']['info']['scores']
            print(f"Survival Decision: {action}")
            print(f"Action scores: {[(k, f'{v:.2f}') for k, v in scores.items()]}")
        
        # 未来予測テスト
        if crisis_objects:
            prediction = engine.predict_future_state(crisis_objects[0].id)
            print(f"Future prediction for {prediction.object_id}:")
            print(f"  Crisis level: {prediction.crisis_level}")
            print(f"  Confidence: {prediction.confidence:.2f}")


def run_learning_adaptation_test():
    """学習・適応テストの実行"""
    print("\n\n=== SSD Learning & Adaptation Test ===")
    
    engine = create_ssd_engine("learning_agent")
    setup_basic_structure(engine)
    
    # 学習用オブジェクト
    learning_objects = create_simple_world_objects()
    
    print("Testing learning and adaptation over multiple episodes...")
    
    # 複数エピソードでの学習
    episode_results = []
    
    for episode in range(3):
        print(f"\n--- Episode {episode + 1} ---")
        episode_decisions = []
        
        # エピソード内でのステップ実行
        for step in range(8):
            perceived = [random.choice(learning_objects)]
            actions = ["approach", "avoid", "investigate", "use", "gather"]
            
            result = engine.step(perceived, actions)
            
            if 'decision' in result:
                decision = result['decision']['chosen_action']
                episode_decisions.append(decision)
                
                # 行動結果をシミュレート（成功/失敗）
                success = random.random() > 0.4  # 60%成功率
                engine.action_evaluator.record_action_result(decision, success)
        
        episode_results.append(episode_decisions)
        
        # エピソード終了時の統計
        decision_stats = engine.decision_system.get_decision_statistics()
        print(f"Episode {episode + 1} decisions: {episode_decisions}")
        print(f"Exploration ratio: {decision_stats['exploration_ratio']:.2f}")
    
    # 学習結果の分析
    print("\n=== Learning Analysis ===")
    for action in ["approach", "avoid", "investigate", "use", "gather"]:
        success_rate = engine.action_evaluator.get_action_success_rate(action)
        print(f"{action}: {success_rate:.2f} success rate")
    
    # 最終パフォーマンス
    final_performance = engine.get_performance_metrics()
    learning_metrics = final_performance.get('learning_metrics', {})
    print(f"Final learning diversity: {learning_metrics.get('kappa_diversity', 0):.3f}")
    print(f"Learned patterns: {learning_metrics.get('learned_patterns', 0)}")


if __name__ == "__main__":
    # すべてのテストを実行
    try:
        run_basic_test()
        run_survival_scenario_test()
        run_learning_adaptation_test()
        
        print("\n\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()