#!/usr/bin/env python3
"""
SSD Territory System - 動作テスト
四層構造縄張りシステムの動作確認
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ssd_territory import TerritoryProcessor
from ssd_types import LayerType

def test_basic_territory_system():
    """基本的な縄張りシステムのテスト"""
    print("🧪 SSD Territory System - Basic Test")
    print("=" * 50)
    
    # 層の動かしにくさ設定
    layer_mobility = {
        LayerType.PHYSICAL: 0.1,
        LayerType.BASE: 0.3,
        LayerType.CORE: 0.6,
        LayerType.UPPER: 0.9
    }
    
    # 縄張りプロセッサーを作成
    territory_processor = TerritoryProcessor(layer_mobility)
    
    print("✅ TerritoryProcessor 作成成功")
    
    # NPC「Alice」の縄張り経験をテスト
    npc_id = "Alice"
    location = (10.0, 20.0)
    
    print(f"\n🏠 NPC {npc_id} の縄張り経験テスト")
    print(f"📍 位置: {location}")
    
    # 初期状態確認
    initial_state = territory_processor.get_territorial_state(npc_id)
    print(f"\n📊 初期状態:")
    for key, value in initial_state.items():
        if isinstance(value, bool):
            print(f"   {key}: {value}")
        elif isinstance(value, (int, float)):
            print(f"   {key}: {value:.3f}")
        elif isinstance(value, list):
            print(f"   {key}: {len(value)} items")
    
    # 複数回の安全な休息経験
    print(f"\n🔄 安全な休息経験を繰り返し...")
    for i in range(5):
        result = territory_processor.process_territorial_experience(
            npc_id=npc_id,
            location=location,
            experience_type='safe_rest',
            experience_valence=0.8,
            tick=i
        )
        
        print(f"   ステップ {i+1}: 意味圧変化 = {result['meaning_pressure_delta']:.4f}")
        
        if result['territorial_changes']:
            for change in result['territorial_changes']:
                print(f"   🏘️ 縄張り変化: {change['action']}")
                print(f"      半径: {change['radius']}, 安心感: {change.get('alignment_comfort', 0):.3f}")
    
    # 経験後の状態確認
    print(f"\n📊 経験後の状態:")
    final_state = territory_processor.get_territorial_state(npc_id)
    
    print("🏗️ 各層の活性化状況:")
    for layer in LayerType:
        activation_key = f'{layer.value}_activation'
        connections_key = f'{layer.value}_connections'
        if activation_key in final_state:
            print(f"   {layer.value:8}: 活性化 {final_state[activation_key]:.3f}, 接続数 {final_state[connections_key]}")
    
    print(f"\n🎯 縄張り信頼度: {final_state.get('territorial_confidence', 0):.3f}")
    print(f"🔗 多層整合: {final_state.get('multi_layer_alignment', False)}")
    
    return territory_processor, final_state


def test_social_territory_formation():
    """社会的縄張り形成のテスト"""
    print(f"\n👥 社会的縄張り形成テスト")
    print("=" * 30)
    
    layer_mobility = {
        LayerType.PHYSICAL: 0.1,
        LayerType.BASE: 0.3,
        LayerType.CORE: 0.6,
        LayerType.UPPER: 0.9
    }
    
    territory_processor = TerritoryProcessor(layer_mobility)
    
    # 複数NPCでの共同経験
    location = (15.0, 25.0)
    leader = "Bob"
    participants = ["Charlie", "Diana"]
    
    print(f"👑 リーダー: {leader}")
    print(f"👫 参加者: {participants}")
    print(f"📍 共同経験位置: {location}")
    
    # 共同作業経験
    result = territory_processor.process_territorial_experience(
        npc_id=leader,
        location=location,
        experience_type='social_cooperation',
        experience_valence=0.9,
        other_npcs=participants,
        tick=10
    )
    
    if result['collective_formation']:
        formation = result['collective_formation']
        print(f"🤝 {formation['action']} 成功!")
        print(f"   グループID: {formation['group_id']}")
        print(f"   参加者: {formation['participants']}")
        print(f"   整合タイプ: {formation['alignment_type']}")
    
    # 各NPCの社会的結束状況を確認
    for npc in [leader] + participants:
        state = territory_processor.get_territorial_state(npc)
        upper_activation = state.get('upper_activation', 0)
        print(f"   {npc}: 上層活性化 = {upper_activation:.3f}")


def test_cross_layer_effects():
    """四層間相互作用のテスト"""
    print(f"\n🔄 四層間相互作用テスト")
    print("=" * 30)
    
    layer_mobility = {
        LayerType.PHYSICAL: 0.1,
        LayerType.BASE: 0.3,
        LayerType.CORE: 0.6,
        LayerType.UPPER: 0.9
    }
    
    territory_processor = TerritoryProcessor(layer_mobility)
    npc_id = "Eva"
    location = (5.0, 5.0)
    
    # 段階的に強い経験を積む
    experiences = [
        ('safe_rest', 0.6),
        ('successful_forage', 0.7),
        ('territory_defense', 0.9),
        ('safe_rest', 0.8),
        ('social_cooperation', 0.8)
    ]
    
    print("📈 段階的経験蓄積:")
    for i, (exp_type, valence) in enumerate(experiences):
        territory_processor.process_territorial_experience(
            npc_id=npc_id,
            location=location,
            experience_type=exp_type,
            experience_valence=valence,
            tick=i
        )
        
        state = territory_processor.get_territorial_state(npc_id)
        confidence = state.get('territorial_confidence', 0)
        print(f"   {i+1}. {exp_type}: 信頼度 {confidence:.3f}")
    
    # 最終状態の詳細確認
    final_state = territory_processor.get_territorial_state(npc_id)
    print(f"\n🔍 最終分析:")
    print(f"   縄張り保有: {final_state['has_territory']}")
    print(f"   多層整合達成: {final_state['multi_layer_alignment']}")
    print(f"   総合信頼度: {final_state['territorial_confidence']:.3f}")


def test_territorial_interaction():
    """縄張り間相互作用のテスト"""
    print(f"\n⚔️ 縄張り間相互作用テスト")
    print("=" * 30)
    
    layer_mobility = {
        LayerType.PHYSICAL: 0.1,
        LayerType.BASE: 0.3,
        LayerType.CORE: 0.6,
        LayerType.UPPER: 0.9
    }
    
    territory_processor = TerritoryProcessor(layer_mobility)
    
    # 縄張り主を設定
    owner = "Frank"
    owner_location = (0.0, 0.0)
    
    # 縄張り形成まで経験を積む
    for i in range(6):
        territory_processor.process_territorial_experience(
            npc_id=owner,
            location=owner_location,
            experience_type='safe_rest',
            experience_valence=0.85,
            tick=i
        )
    
    owner_state = territory_processor.get_territorial_state(owner)
    print(f"🏠 {owner} の縄張り: {owner_state['has_territory']}")
    
    if owner_state['has_territory']:
        # 侵入者のテスト
        intruder = "Grace"
        intrusion_location = (3.0, 3.0)  # 縄張り内
        
        interaction = territory_processor.check_territorial_interaction(intruder, intrusion_location)
        
        print(f"🚶 {intruder} が位置 {intrusion_location} に接近:")
        print(f"   他者縄張り: {interaction['is_others_territory']}")
        print(f"   縄張り主: {interaction['territory_owner']}")
        print(f"   侵入レベル: {interaction['intrusion_level']:.3f}")
        print(f"   推奨行動: {interaction['recommended_action']}")


if __name__ == "__main__":
    print("🧪 SSD Territory System - 統合動作テスト")
    print("=" * 60)
    
    try:
        # 基本テスト
        processor, state = test_basic_territory_system()
        
        # 社会的縄張りテスト  
        test_social_territory_formation()
        
        # 四層相互作用テスト
        test_cross_layer_effects()
        
        # 縄張り間相互作用テスト
        test_territorial_interaction()
        
        print(f"\n🎉 全テスト完了!")
        print(f"✅ SSD四層構造縄張りシステムが正常に動作しています")
        
    except Exception as e:
        print(f"❌ テストエラー: {e}")
        import traceback
        traceback.print_exc()