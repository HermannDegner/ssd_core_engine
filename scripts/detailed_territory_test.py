#!/usr/bin/env python3
"""
SSD Territory System - 詳細動作テスト
四層構造縄張りシステムの詳細分析
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ssd_territory import TerritoryProcessor
from ssd_types import LayerType

def detailed_territory_analysis():
    """詳細な縄張り分析"""
    print("🔍 詳細縄張り分析テスト")
    print("=" * 40)
    
    layer_mobility = {
        LayerType.PHYSICAL: 0.1,
        LayerType.BASE: 0.3,
        LayerType.CORE: 0.6,
        LayerType.UPPER: 0.9
    }
    
    territory_processor = TerritoryProcessor(layer_mobility)
    npc_id = "TestNPC"
    location = (0.0, 0.0)
    
    print(f"🏠 {npc_id} の縄張り形成プロセス詳細分析")
    print(f"📍 位置: {location}")
    print(f"🎯 縄張り閾値: {territory_processor.territory_claim_threshold}")
    
    # 段階的に経験を蓄積し、各ステップでの変化を詳しく見る
    for step in range(10):
        print(f"\n--- ステップ {step+1} ---")
        
        # 経験を処理
        result = territory_processor.process_territorial_experience(
            npc_id=npc_id,
            location=location,
            experience_type='safe_rest',
            experience_valence=0.8,
            tick=step
        )
        
        # 状態詳細を確認
        state = territory_processor.get_territorial_state(npc_id)
        
        print(f"縄張り信頼度: {state['territorial_confidence']:.4f}")
        
        # 各層の詳細
        for layer in LayerType:
            activation = state.get(f'{layer.value}_activation', 0)
            connections = state.get(f'{layer.value}_connections', 0)
            print(f"  {layer.value:8}: {activation:.4f} ({connections}接続)")
        
        # 縄張り形成チェック
        location_id = f"loc_{location[0]:.1f}_{location[1]:.1f}"
        comfort = territory_processor._calculate_alignment_comfort(npc_id, location_id)
        print(f"整合安心感: {comfort:.4f} ({'閾値超過' if comfort > territory_processor.territory_claim_threshold else '閾値未満'})")
        
        if result['territorial_changes']:
            for change in result['territorial_changes']:
                print(f"🏘️ 縄張り形成: {change}")
        
        # 閾値に達した場合は終了
        if state['has_territory']:
            break
    
    # 最終結果
    final_state = territory_processor.get_territorial_state(npc_id)
    print(f"\n🏁 最終結果:")
    print(f"縄張り形成: {'成功' if final_state['has_territory'] else '未形成'}")
    print(f"多層整合: {'達成' if final_state['multi_layer_alignment'] else '未達成'}")
    
    return territory_processor

def test_threshold_adjustment():
    """閾値調整テスト"""
    print(f"\n⚙️ 閾値調整テスト")
    print("=" * 30)
    
    layer_mobility = {
        LayerType.PHYSICAL: 0.1,
        LayerType.BASE: 0.3,
        LayerType.CORE: 0.6,
        LayerType.UPPER: 0.9
    }
    
    # 閾値を0.3に下げてテスト
    territory_processor = TerritoryProcessor(layer_mobility)
    territory_processor.territory_claim_threshold = 0.3  # デフォルトから0.6→0.3に下降
    
    print(f"🎯 調整後閾値: {territory_processor.territory_claim_threshold}")
    
    npc_id = "AdjustedNPC"
    location = (5.0, 5.0)
    
    # 縄張り形成まで経験を蓄積
    for step in range(8):
        result = territory_processor.process_territorial_experience(
            npc_id=npc_id,
            location=location,
            experience_type='safe_rest',
            experience_valence=0.8,
            tick=step
        )
        
        state = territory_processor.get_territorial_state(npc_id)
        confidence = state['territorial_confidence']
        
        print(f"ステップ {step+1}: 信頼度 {confidence:.4f}")
        
        if result['territorial_changes']:
            change = result['territorial_changes'][0]
            print(f"🏘️ 縄張り形成成功! 半径:{change['radius']}, 安心感:{change.get('alignment_comfort', 0):.3f}")
            break
    
    return territory_processor

def test_cross_layer_interaction_details():
    """四層間相互作用の詳細テスト"""
    print(f"\n🔄 四層間相互作用詳細テスト")
    print("=" * 40)
    
    layer_mobility = {
        LayerType.PHYSICAL: 0.1,
        LayerType.BASE: 0.3,
        LayerType.CORE: 0.6,
        LayerType.UPPER: 0.9
    }
    
    territory_processor = TerritoryProcessor(layer_mobility)
    territory_processor.territory_claim_threshold = 0.3
    
    npc_id = "InteractionNPC"
    location = (10.0, 10.0)
    
    # 各層の構造を直接確認
    print("📊 四層構造の詳細確認:")
    
    for step in range(6):
        territory_processor.process_territorial_experience(
            npc_id=npc_id,
            location=location,
            experience_type='safe_rest',
            experience_valence=0.85,
            tick=step
        )
        
        structures = territory_processor.npc_structures[npc_id]
        location_id = f"loc_{location[0]:.1f}_{location[1]:.1f}"
        
        print(f"\nステップ {step+1} 後の構造状態:")
        
        # 物理層
        spatial = structures[LayerType.PHYSICAL]['spatial_constraints']
        terrain_key = f'terrain_{location_id}'
        print(f"  物理層 - 地形把握: {spatial.connections.get(terrain_key, 0.0):.4f}")
        
        # 基層
        instinct = structures[LayerType.BASE]['territorial_instinct']
        print(f"  基層   - 本能安全感: {instinct.connections.get(location_id, 0.0):.4f}")
        
        # 中核層
        attachment = structures[LayerType.CORE]['place_attachment']
        memory = structures[LayerType.CORE]['territorial_memory']
        print(f"  中核層 - 場所愛着: {attachment.connections.get(location_id, 0.0):.4f}")
        print(f"  中核層 - 記憶蓄積: {memory.connections.get(location_id, 0.0):.4f}")
        
        # 上層
        abstract = structures[LayerType.UPPER]['abstract_boundaries']
        ownership_key = f'ownership_{location_id}'
        print(f"  上層   - 所有概念: {abstract.connections.get(ownership_key, 0.0):.4f}")
        
        # 四層間相互作用の処理
        territory_processor._process_cross_layer_territorial_effects(npc_id, location_id)


if __name__ == "__main__":
    print("🔬 SSD Territory System - 詳細動作分析")
    print("=" * 60)
    
    try:
        # 詳細分析
        processor = detailed_territory_analysis()
        
        # 閾値調整テスト
        adjusted_processor = test_threshold_adjustment()
        
        # 四層間相互作用詳細
        test_cross_layer_interaction_details()
        
        print(f"\n🎊 詳細分析完了!")
        print(f"✨ SSD四層構造縄張りシステムの動作メカニズムが確認できました")
        
    except Exception as e:
        print(f"❌ 分析エラー: {e}")
        import traceback
        traceback.print_exc()