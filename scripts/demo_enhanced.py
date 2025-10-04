#!/usr/bin/env python3
"""
SSD Integration Test - Enhanced Features
構造主観力学 - 数理完全性向上機能の統合テスト
"""

import sys
sys.path.insert(0, '.')

from ssd_engine import create_ssd_engine, setup_basic_structure
from ssd_utils import create_survival_scenario_objects
import numpy as np


def test_enhanced_integration():
    """強化機能の統合テスト"""
    print("🚀 SSD Enhanced Integration Test")
    print("=" * 50)
    
    # SSDエンジンの作成と初期化
    engine = create_ssd_engine("enhanced_test_agent")
    setup_basic_structure(engine)
    
    # 生存シナリオオブジェクトの作成
    survival_objects = create_survival_scenario_objects()
    
    print(f"📦 オブジェクト数: {len(survival_objects)}")
    for obj in survival_objects[:3]:  # 最初の3つを表示
        print(f"   - {obj.id} ({obj.type}): 値={obj.current_value:.1f}")
    
    print("\n🔄 システム実行 (5ステップ)...")
    
    # 利用可能な行動
    actions = ['approach', 'avoid', 'investigate', 'seek_shelter', 'gather', 'rest']
    
    for step in range(5):
        print(f"\n--- ステップ {step + 1} ---")
        
        # 一部のオブジェクトを知覚対象として選択
        perceived = survival_objects[step:step+2] if step < len(survival_objects) else survival_objects[:2]
        
        # ステップ実行
        result = engine.step(perceived_objects=perceived, available_actions=actions)
        
        # 基本情報
        if 'decision' in result:
            chosen_action = result['decision']['chosen_action']
            print(f"🎯 選択行動: {chosen_action}")
        
        # 新機能の結果表示
        if 'thermal_dynamics' in result:
            thermal = result['thermal_dynamics']
            if 'thermal_stats' in thermal:
                stats = thermal['thermal_stats']
                print(f"🔥 熱力学:")
                print(f"   - 熱効率: {stats.get('thermal_efficiency', 0):.1%}")
                print(f"   - 総熱損失: {stats.get('total_heat_loss', 0):.4f}")
                
            if 'alignment_work' in thermal:
                work_items = list(thermal['alignment_work'].items())[:2]  # 最初の2つ
                if work_items:
                    print(f"   - 整合仕事例: {work_items}")
        
        # 即座反応の表示
        immediate_reactions = [k for k in result.keys() if k.startswith('immediate_reaction_')]
        if immediate_reactions:
            reaction_key = immediate_reactions[0]
            reaction = result[reaction_key]
            print(f"⚡ 即座反応: {reaction['action']} (強度: {reaction['strength']:.3f})")
        
        # 意識的反応の表示
        if 'conscious_reactions' in result:
            conscious = result['conscious_reactions'][0] if result['conscious_reactions'] else None
            if conscious:
                print(f"🧠 意識的判断: {conscious['final_action']}")
        
        # システム状態
        if 'system_state' in result:
            sys_state = result['system_state']
            print(f"📊 システム: E={sys_state.get('total_E', 0):.3f}")
    
    print("\n✅ 統合テスト完了!")
    return engine


def test_crisis_reaction():
    """危機反応の専用テスト"""
    print("\n🚨 Crisis Reaction Test")
    print("=" * 50)
    
    engine = create_ssd_engine("crisis_agent")
    setup_basic_structure(engine)
    
    # 危機シナリオの作成
    from ssd_types import ObjectInfo, LayerType
    
    crisis_threat = ObjectInfo(
        id="bear_encounter",
        type="threat",
        properties={"danger_level": 0.95, "distance": 5, "size": "large"},
        current_value=95.0,
        decline_rate=0.0,  # 脅威は持続
        volatility=0.1,
        meaning_values={
            LayerType.PHYSICAL: 0.9,
            LayerType.BASE: 0.95,
            LayerType.CORE: 0.4,
            LayerType.UPPER: 0.1
        }
    )
    
    print("🐻 危機シナリオ: クマとの遭遇")
    print(f"   危険レベル: {crisis_threat.properties['danger_level']}")
    print(f"   生存関連度: {crisis_threat.survival_relevance:.3f}")
    
    # 危機対応の実行
    result = engine.step(
        perceived_objects=[crisis_threat],
        available_actions=['flee', 'freeze', 'fight', 'seek_shelter']
    )
    
    print("\n📋 危機対応結果:")
    
    # 決定
    if 'decision' in result:
        decision = result['decision']
        print(f"🏃 最終決定: {decision['chosen_action']}")
    
    # 熱力学的分析
    if 'thermal_dynamics' in result and 'thermal_stats' in result['thermal_dynamics']:
        stats = result['thermal_dynamics']['thermal_stats']
        print(f"🔥 エネルギー分析:")
        print(f"   - システム効率: {stats.get('thermal_efficiency', 0):.1%}")
        print(f"   - 熱損失: {stats.get('total_heat_loss', 0):.4f}")
    
    # 反応時間分析
    immediate_key = next((k for k in result.keys() if k.startswith('immediate_reaction_')), None)
    if immediate_key:
        reaction = result[immediate_key]
        print(f"⚡ 基層反応:")
        print(f"   - 反応時間: {reaction['reaction_time']}s")
        print(f"   - 行動: {reaction['action']}")
        print(f"   - 強度: {reaction['strength']:.3f}")
    
    if 'conscious_reactions' in result and result['conscious_reactions']:
        conscious = result['conscious_reactions'][0]
        print(f"🧠 意識的統合:")
        print(f"   - 処理時間: +{conscious['processing_time']}s")
        print(f"   - 最終行動: {conscious['final_action']}")
    
    print("✅ 危機反応テスト完了!")


def demonstration():
    """デモンストレーション実行"""
    print("🎭 SSD Enhanced Features Demonstration")
    print("構造主観力学 - 数理完全性向上機能デモ")
    print("=" * 60)
    
    try:
        # 統合テスト
        engine = test_enhanced_integration()
        
        # 危機反応テスト
        test_crisis_reaction()
        
        print(f"\n🎉 全デモンストレーション完了!")
        print(f"🔬 数理モデル完全性が向上し、以下が実装されました:")
        print(f"   ✅ 熱損失を考慮した整合ステップ (W = p·j - ρj²)")
        print(f"   ✅ 二段階反応システム (50ms無意識 + 350ms意識的)")
        print(f"   ✅ 層別エネルギー効率計算")
        print(f"   ✅ 生存駆動型反応優先度")
        print(f"   ✅ 統合システムでの実時間処理")
        
    except Exception as e:
        print(f"❌ デモエラー: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    demonstration()