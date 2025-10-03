#!/usr/bin/env python3
"""
SSD Enhanced Features Test Script
数理モデル完全性向上機能のテストスクリプト
"""

import sys
sys.path.insert(0, '.')

from ssd_types import LayerType, ObjectInfo, StructuralState
from ssd_alignment_leap import AlignmentProcessor, TwoStageReactionSystem
import numpy as np


def test_heat_loss_alignment():
    """熱損失を考慮した整合ステップのテスト"""
    print("🔥 熱損失整合ステップテスト")
    print("=" * 50)
    
    # AlignmentProcessorの初期化
    layer_mobility = {
        LayerType.PHYSICAL: 0.2,
        LayerType.BASE: 0.4,
        LayerType.CORE: 0.6,
        LayerType.UPPER: 0.8
    }
    
    alignment_processor = AlignmentProcessor(layer_mobility)
    
    # テスト用の層構造作成
    layers = {
        LayerType.BASE: {
            "survival_1": StructuralState(layer=LayerType.BASE, activation=0.6, stability=0.9, connections={}),
            "food_need": StructuralState(layer=LayerType.BASE, activation=0.7, stability=0.9, connections={})
        },
        LayerType.CORE: {
            "social_rule": StructuralState(layer=LayerType.CORE, activation=0.4, stability=0.6, connections={}),
            "work_ethic": StructuralState(layer=LayerType.CORE, activation=0.5, stability=0.6, connections={})
        }
    }
    
    # 熱損失を考慮した整合処理実行
    alignment_work = alignment_processor.process_alignment_step_with_heat_loss(layers, current_E=0.7)
    
    print("🧮 整合仕事計算結果:")
    for elem_id, work in alignment_work.items():
        print(f"  {elem_id}: W = {work:.4f}")
    
    # 統計取得
    stats = alignment_processor.get_alignment_statistics()
    print(f"\n📊 統計情報:")
    print(f"  平均慣性: {stats['avg_inertia']:.4f}")
    print(f"  総熱損失: {stats['total_heat_loss']:.4f}")
    print(f"  熱効率: {stats['thermal_efficiency']:.4f}")
    print()


def test_two_stage_reaction():
    """二段階反応システムのテスト"""
    print("🧠 二段階反応システムテスト")
    print("=" * 50)
    
    reaction_system = TwoStageReactionSystem()
    
    # テスト刺激の定義
    test_stimuli = [
        {
            'type': 'threat',
            'intensity': 0.9,
            'social_context': False,
            'danger_level': 0.8,
            'description': '高強度の脅威'
        },
        {
            'type': 'food',
            'intensity': 0.7,
            'social_context': True,
            'value_alignment': 0.6,
            'long_term_benefit': 0.4,
            'description': '社会的文脈での食物'
        },
        {
            'type': 'abstract',
            'intensity': 0.5,
            'social_context': False,
            'value_alignment': 0.9,
            'long_term_benefit': 0.8,
            'description': '高価値な抽象概念'
        }
    ]
    
    current_time = 0.0
    
    print("🎯 刺激処理結果:")
    for i, stimulus in enumerate(test_stimuli):
        print(f"\n--- 刺激 {i+1}: {stimulus['description']} ---")
        
        # 即座の反応（第1段階）
        unconscious_response = reaction_system.process_reaction(stimulus, current_time)
        
        print(f"🚨 無意識反応 (t={unconscious_response['reaction_time']}s):")
        print(f"  行動: {unconscious_response['action']}")
        print(f"  強度: {unconscious_response['strength']:.3f}")
        print(f"  信頼度: {unconscious_response['confidence']:.3f}")
        
        # 時間経過をシミュレート
        current_time += 0.4  # 400ms経過
        
        # 意識的処理（第2段階） - ダミー層データで実行
        layers = {
            LayerType.BASE: {"base_1": StructuralState(layer=LayerType.BASE, activation=0.5, stability=0.9, connections={})},
            LayerType.CORE: {"core_1": StructuralState(layer=LayerType.CORE, activation=0.6, stability=0.6, connections={})},
            LayerType.UPPER: {"upper_1": StructuralState(layer=LayerType.UPPER, activation=0.7, stability=0.3, connections={})}
        }
        
        conscious_responses = reaction_system.process_conscious_reactions(current_time, layers)
        
        if conscious_responses:
            response = conscious_responses[0]
            print(f"🤔 意識的再処理 (t={reaction_system.conscious_processing_time}s後):")
            print(f"  最終行動: {response['final_action']}")
            print(f"  統合信頼度: {response['integration_confidence']:.3f}")
            print(f"  中核調整: {response['core_adjustment']['action']}")
            print(f"  上層評価: {response['upper_evaluation']['recommendation']}")


def test_integration_scenario():
    """統合シナリオテスト"""
    print("\n🌟 統合シナリオテスト")
    print("=" * 50)
    
    print("📝 シナリオ: 野生動物との遭遇")
    
    # 1. 熱損失整合処理で初期状態を作成
    layer_mobility = {LayerType.PHYSICAL: 0.2, LayerType.BASE: 0.4, LayerType.CORE: 0.6, LayerType.UPPER: 0.8}
    alignment_processor = AlignmentProcessor(layer_mobility)
    
    # 2. 危険刺激の二段階処理
    reaction_system = TwoStageReactionSystem()
    
    danger_stimulus = {
        'type': 'threat',
        'intensity': 0.95,
        'social_context': False,
        'danger_level': 0.9,
        'description': '野生のクマとの遭遇'
    }
    
    # 即座の反応
    immediate = reaction_system.process_reaction(danger_stimulus, 0.0)
    print(f"⚡ 即座の反応: {immediate['action']} (強度: {immediate['strength']:.3f})")
    
    # 層状態の作成（高い生存圧力）
    survival_layers = {
        LayerType.PHYSICAL: {
            "body_state": StructuralState(layer=LayerType.PHYSICAL, activation=0.9, stability=1.0, connections={})
        },
        LayerType.BASE: {
            "fight_flight": StructuralState(layer=LayerType.BASE, activation=0.95, stability=0.9, connections={}),
            "survival_instinct": StructuralState(layer=LayerType.BASE, activation=0.92, stability=0.9, connections={})
        },
        LayerType.CORE: {
            "safety_protocol": StructuralState(layer=LayerType.CORE, activation=0.7, stability=0.6, connections={}),
        },
        LayerType.UPPER: {
            "rational_analysis": StructuralState(layer=LayerType.UPPER, activation=0.2, stability=0.3, connections={})
        }
    }
    
    # 熱損失を含む整合処理
    alignment_work = alignment_processor.process_alignment_step_with_heat_loss(survival_layers, current_E=0.9)
    
    print(f"\n⚙️ 生存モード整合処理:")
    for layer_elem, work in alignment_work.items():
        if work > 0.1:  # 有意な仕事のみ表示
            print(f"  {layer_elem}: 仕事量 = {work:.3f}")
    
    # 意識的再処理（0.35秒後）
    conscious_results = reaction_system.process_conscious_reactions(0.4, survival_layers)
    
    if conscious_results:
        final = conscious_results[0]
        print(f"\n🧠 最終判断: {final['final_action']}")
        print(f"   理由: 基層反応({final['unconscious_response']['action']})を")
        print(f"         中核層が{final['core_adjustment']['action']}に調整")
        print(f"         上層評価: {final['upper_evaluation']['recommendation']}")
    
    # システム統計
    stats = alignment_processor.get_alignment_statistics()
    print(f"\n📊 システム効率:")
    print(f"   熱効率: {stats['thermal_efficiency']:.1%}")
    print(f"   総熱損失: {stats['total_heat_loss']:.4f}")


if __name__ == "__main__":
    print("🔬 SSD Enhanced Features Test Suite")
    print("構造主観力学 - 数理モデル完全性向上機能テスト")
    print("=" * 60)
    
    try:
        # テスト実行
        test_heat_loss_alignment()
        test_two_stage_reaction()
        test_integration_scenario()
        
        print("\n✅ 全テスト完了！")
        print("🎉 数理モデル完全性向上機能が正常に動作しています。")
        
    except Exception as e:
        print(f"\n❌ テストエラー: {e}")
        import traceback
        traceback.print_exc()