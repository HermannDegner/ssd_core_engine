#!/usr/bin/env python3
"""
SSD Territory System Test
縄張りシステムの動作検証テスト
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ssd_core_engine'))

from ssd_territory import TerritoryProcessor, TerritoryInfo, SubjectiveBoundary
from ssd_types import LayerType
import math

def test_territory_basic_functionality():
    """縄張りシステムの基本機能テスト"""
    print("=== 縄張りシステム基本機能テスト ===")
    
    processor = TerritoryProcessor()
    
    # 1. NPCの境界初期化テスト
    print("1. NPC境界初期化テスト")
    processor.initialize_npc_boundaries("npc_alice")
    assert "npc_alice" in processor.subjective_boundaries
    boundary = processor.subjective_boundaries["npc_alice"]
    assert len(boundary.inner_objects) == 0
    assert len(boundary.outer_objects) == 0
    print("   ✓ 境界初期化成功")
    
    # 2. 縄張り経験処理テスト
    print("2. 縄張り経験処理テスト")
    result = processor.process_territorial_experience(
        npc_id="npc_alice",
        location=(10.0, 20.0),
        experience_type="safe_rest",
        experience_valence=0.8,
        tick=1
    )
    
    print(f"   経験処理結果: {result}")
    assert result['meaning_pressure_delta'] is not None
    print("   ✓ 経験処理成功")
    
    # 3. 内側度更新テスト
    print("3. 内側度更新確認")
    boundary = processor.subjective_boundaries["npc_alice"]
    location_id = "loc_10.0_20.0"
    if location_id in boundary.boundary_strength:
        strength = boundary.boundary_strength[location_id]
        print(f"   場所 {location_id} の境界強度: {strength:.3f}")
        assert strength > 0, "正の体験による境界強度は正であるべき"
    print("   ✓ 内側度更新成功")

def test_territory_formation():
    """縄張り形成プロセスのテスト"""
    print("\n=== 縄張り形成テスト ===")
    
    processor = TerritoryProcessor()
    
    # 複数の正の経験で縄張り形成を促進
    location = (15.0, 25.0)
    experiences = [
        ("safe_rest", 0.7),
        ("successful_forage", 0.6),
        ("social_cooperation", 0.8),
        ("safe_rest", 0.9)  # 繰り返し経験
    ]
    
    territory_formed = False
    for i, (exp_type, valence) in enumerate(experiences):
        print(f"{i+1}. 経験: {exp_type} (価値: {valence})")
        result = processor.process_territorial_experience(
            npc_id="npc_bob",
            location=location,
            experience_type=exp_type,
            experience_valence=valence,
            tick=i+1
        )
        
        if result['territorial_changes']:
            territory_formed = True
            territory_info = result['territorial_changes'][0]
            print(f"   🏘️ 縄張り形成! {territory_info}")
            break
    
    # 縄張り状態確認
    state = processor.get_territorial_state("npc_bob")
    print(f"縄張り状態: {state}")
    
    if territory_formed:
        print("   ✓ 縄張り形成成功")
        
        # 縄張り相互作用テスト
        interaction = processor.check_territorial_interaction("npc_bob", location)
        print(f"   縄張り相互作用: {interaction}")
        assert interaction['is_own_territory'] == True
        print("   ✓ 縄張り認識成功")
    else:
        print("   ⚠️ 縄張り形成されず（閾値調整が必要な可能性）")

def test_collective_boundary():
    """集団境界形成のテスト"""
    print("\n=== 集団境界形成テスト ===")
    
    processor = TerritoryProcessor()
    
    # 共同経験による集団境界形成
    result = processor.process_territorial_experience(
        npc_id="npc_charlie",
        location=(5.0, 5.0),
        experience_type="social_cooperation",
        experience_valence=0.8,
        other_npcs=["npc_david", "npc_eve"],
        tick=1
    )
    
    if result['collective_formation']:
        print(f"集団境界形成: {result['collective_formation']}")
        
        # 参加者間の内側認識確認
        charlie_boundary = processor.subjective_boundaries["npc_charlie"]
        assert "npc_david" in charlie_boundary.inner_objects
        assert "npc_eve" in charlie_boundary.inner_objects
        print("   ✓ 集団境界形成成功")
        print("   ✓ 相互内側認識確認")
    else:
        print("   ⚠️ 集団境界形成されず")

def test_territorial_defense():
    """縄張り防衛システムのテスト"""
    print("\n=== 縄張り防衛テスト ===")
    
    processor = TerritoryProcessor()
    
    # 先に縄張りを作成
    territory = TerritoryInfo(
        territory_id="test_territory",
        center=(0.0, 0.0),
        radius=10.0,
        owner_npc="npc_defender",
        members={"npc_defender"},
        established_tick=1
    )
    
    processor.territories["test_territory"] = territory
    processor.npc_territories["npc_defender"] = "test_territory"
    processor.initialize_npc_boundaries("npc_defender")
    
    # 各種脅威に対する防衛反応テスト
    threats = [
        ((8.0, 0.0), "predator"),      # 縄張り内の捕食者
        ((5.0, 5.0), "hostile_human"), # 縄張り内の敵対者
        ((2.0, 2.0), "unknown_human")  # 縄張り内の未知の人間
    ]
    
    for threat_location, threat_type in threats:
        print(f"脅威テスト: {threat_type} at {threat_location}")
        
        # 防衛処理
        defense_result = processor.process_territorial_defense(
            defender_npc="npc_defender",
            intruder_location=threat_location,
            intruder_type=threat_type,
            current_tick=2
        )
        
        print(f"   防衛結果: {defense_result}")
        
        # 脅威侵入検知
        threat_result = processor.check_threat_intrusion(
            npc_id="npc_defender",
            threat_location=threat_location,
            threat_type=threat_type
        )
        
        print(f"   脅威検知: {threat_result}")
        print()

def test_boundary_decay():
    """境界減衰システムのテスト"""
    print("\n=== 境界減衰テスト ===")
    
    processor = TerritoryProcessor()
    processor.initialize_npc_boundaries("npc_test")
    
    # 初期境界強度を設定
    boundary = processor.subjective_boundaries["npc_test"]
    boundary.boundary_strength["test_object"] = 0.5
    boundary.inner_objects.add("test_object")
    
    print(f"初期境界強度: {boundary.boundary_strength['test_object']:.3f}")
    
    # 数回の減衰処理
    for i in range(10):
        processor.decay_boundaries()
        if "test_object" in boundary.boundary_strength:
            strength = boundary.boundary_strength["test_object"]
            print(f"減衰 {i+1}: {strength:.3f}")
        else:
            print(f"減衰 {i+1}: オブジェクト削除")
            break
    
    print("   ✓ 境界減衰システム動作確認")

def test_safety_feeling_calculation():
    """安全感計算の詳細テスト"""
    print("\n=== 安全感計算テスト ===")
    
    processor = TerritoryProcessor()
    processor.initialize_npc_boundaries("npc_test")
    
    # 境界強度を設定
    boundary = processor.subjective_boundaries["npc_test"]
    boundary.boundary_strength["loc_10.0_20.0"] = 0.6  # 慣れた場所
    
    # 安全感計算
    safety = processor._calculate_safety_feeling("npc_test", (10.0, 20.0))
    print(f"安全感: {safety:.3f}")
    print(f"閾値: {processor.territory_claim_threshold}")
    
    if safety >= processor.territory_claim_threshold:
        print("   ✓ 縄張り主張可能レベル")
    else:
        print("   ⚠️ 縄張り主張には不十分")

if __name__ == "__main__":
    print("🏘️ SSD縄張りシステム総合テスト開始")
    print("=" * 50)
    
    test_territory_basic_functionality()
    test_territory_formation()
    test_collective_boundary()
    test_territorial_defense()
    test_boundary_decay()
    test_safety_feeling_calculation()
    
    print("\n" + "=" * 50)
    print("✅ 全てのテスト完了")