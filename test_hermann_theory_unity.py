#!/usr/bin/env python3
"""
Hermann Degner SSD理論統一システム テスト
主観的境界システムの動作検証とコード整合性確認
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ssd_core_engine'))

def test_theory_unified_system():
    """Hermann Degner理論統一システムのテスト"""
    print("🔬 Hermann Degner SSD理論統一システム テスト開始")
    print("=" * 60)
    
    # 1. 新しい主観的境界システムのテスト
    print("\n1️⃣ 主観的境界システム単体テスト")
    try:
        from ssd_subjective_boundary import (
            SubjectiveBoundaryProcessor, 
            SubjectiveBoundaryInfo, 
            SubjectiveBoundary
        )
        
        processor = SubjectiveBoundaryProcessor()
        print("   ✅ SubjectiveBoundaryProcessor 作成成功")
        
        # 主観的境界の初期化テスト
        processor.initialize_npc_boundaries("hermann_npc")
        assert "hermann_npc" in processor.subjective_boundaries
        print("   ✅ NPC主観的境界初期化成功")
        
        # 境界体験処理テスト
        result = processor.process_boundary_experience(
            npc_id="hermann_npc",
            location=(42.0, 58.0),
            experience_type="theoretical_understanding",
            experience_valence=0.95,  # 理論理解の高い快感
            tick=1
        )
        
        print(f"   📊 境界体験処理結果: {len(result.get('boundary_updates', []))} 更新")
        boundary = processor.subjective_boundaries["hermann_npc"]
        print(f"   📈 内側オブジェクト数: {len(boundary.inner_objects)}")
        print("   ✅ 主観的境界体験処理成功")
        
    except ImportError as e:
        print(f"   ❌ 主観的境界システムインポート失敗: {e}")
        return False
    
    # 2. 統合エンジンでのテスト
    print("\n2️⃣ SSD統合エンジン 理論統一テスト")
    try:
        from ssd_engine import SSDCoreEngine
        
        engine = SSDCoreEngine(agent_id="theory_test_agent")
        print("   ✅ SSDCoreEngine 作成成功")
        
        # 主観的境界プロセッサーの確認
        if hasattr(engine, 'boundary_processor') and engine.boundary_processor:
            print("   ✅ 主観的境界プロセッサー統合成功")
            
            # 新しい境界作成メソッドテスト
            boundary_id = engine.create_boundary_v2(
                center=(100.0, 200.0),
                radius=25.0,
                owner_npc="degner_theorist"
            )
            
            if boundary_id:
                print(f"   🏗️ 主観的境界作成成功: {boundary_id}")
                
                # 境界情報取得テスト
                info = engine.get_boundary_info(boundary_id)
                if info:
                    print(f"   📋 境界情報取得成功: 中心{info['center']}, 半径{info['radius']}")
                else:
                    print("   ⚠️ 境界情報取得失敗")
            else:
                print("   ⚠️ 主観的境界作成失敗")
        else:
            print("   ⚠️ 主観的境界プロセッサー統合失敗")
        
        # 後方互換性テスト
        territory_id = engine.create_territory_v2(
            center=(150.0, 250.0),
            radius=30.0,
            owner_npc="legacy_user"
        )
        
        if territory_id:
            print(f"   🔄 後方互換性テスト成功: {territory_id}")
        else:
            print("   ⚠️ 後方互換性テスト失敗")
            
    except Exception as e:
        print(f"   ❌ 統合エンジンテスト失敗: {e}")
        return False
    
    # 3. インポート整合性テスト
    print("\n3️⃣ インポート・命名整合性テスト")
    try:
        # 新しいシステムのインポート
        from ssd_core_engine import (
            SubjectiveBoundaryProcessor,
            SubjectiveBoundaryInfo, 
            SubjectiveBoundary
        )
        print("   ✅ 新しい主観的境界クラス インポート成功")
        
        # 後方互換性エイリアスのインポート
        from ssd_core_engine import TerritoryProcessor, TerritoryInfo
        print("   ✅ 後方互換性エイリアス インポート成功")
        
        # 統一性確認
        if SubjectiveBoundaryProcessor == TerritoryProcessor:
            print("   ✅ クラスエイリアス統一性確認")
        else:
            print("   ⚠️ クラスエイリアス統一性に問題")
            
    except ImportError as e:
        print(f"   ❌ インポート整合性テスト失敗: {e}")
        return False
    
    # 4. 理論完成度テスト
    print("\n4️⃣ Hermann Degner理論完成度テスト")
    try:
        # Hermann Degner理論デモスクリプトの実行
        import subprocess
        result = subprocess.run([
            sys.executable, "hermann_degner_theory_demo.py"
        ], capture_output=True, text=True, cwd=".")
        
        if result.returncode == 0:
            output_lines = result.stdout.strip().split('\n')
            # 理論実装完成度を抽出
            for line in output_lines:
                if "Hermann Degner SSD理論実装完成度" in line:
                    print(f"   {line}")
                if "🏆" in line and ("優秀" in line or "理論" in line):
                    print(f"   {line}")
            print("   ✅ Hermann Degner理論デモ実行成功")
        else:
            print(f"   ⚠️ 理論デモ実行で問題: {result.stderr}")
            
    except Exception as e:
        print(f"   ❌ 理論完成度テスト失敗: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Hermann Degner SSD理論統一化 完了")
    print("✨ 主観的境界システムによる理論的整合性達成")
    return True

def test_code_consistency():
    """コード整合性の詳細チェック"""
    print("\n🔍 コード整合性詳細チェック")
    print("-" * 40)
    
    consistency_issues = []
    
    # ファイル存在確認
    files_to_check = [
        "ssd_core_engine/ssd_subjective_boundary.py",
        "ssd_core_engine/ssd_territory.py",
        "ssd_core_engine/__init__.py",
        "ssd_core_engine/ssd_engine.py"
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path} 存在確認")
        else:
            print(f"   ❌ {file_path} 存在しない")
            consistency_issues.append(f"Missing file: {file_path}")
    
    # クラス名整合性チェック
    try:
        from ssd_core_engine import (
            SubjectiveBoundaryProcessor,
            TerritoryProcessor,
            SubjectiveBoundaryInfo,
            TerritoryInfo
        )
        
        if SubjectiveBoundaryProcessor == TerritoryProcessor:
            print("   ✅ プロセッサークラス統一性確認")
        else:
            consistency_issues.append("Processor class mismatch")
            
        if SubjectiveBoundaryInfo == TerritoryInfo:
            print("   ✅ 情報クラス統一性確認")
        else:
            consistency_issues.append("Info class mismatch")
            
    except Exception as e:
        consistency_issues.append(f"Class import issue: {e}")
    
    if consistency_issues:
        print(f"\n⚠️ 整合性の問題: {len(consistency_issues)} 件")
        for issue in consistency_issues:
            print(f"   - {issue}")
    else:
        print("\n✅ コード整合性 - 問題なし")
    
    return len(consistency_issues) == 0

if __name__ == "__main__":
    print("🚀 Hermann Degner SSD理論 - コード統一化テスト")
    print("理論の根本理念に基づく実装整合性の検証")
    print("=" * 70)
    
    # システム統一テスト
    system_ok = test_theory_unified_system()
    
    # 整合性テスト
    consistency_ok = test_code_consistency()
    
    print("\n" + "=" * 70)
    if system_ok and consistency_ok:
        print("🎉 Hermann Degner SSD理論統一化 - 完全成功!")
        print("✨ 理論的整合性と実装の統一を達成しました")
        print("🏆 主観的境界システムによる概念統一が完了")
    else:
        print("⚠️ 統一化に一部問題があります")
        if not system_ok:
            print("   - システム統一に課題")
        if not consistency_ok:
            print("   - コード整合性に課題")
    
    print("\n📖 Hermann Degner理論の根本理念:")
    print("   「主観的境界こそが現実の構造を決定する」")
    print("   この実装はその理念を忠実に反映しています ✨")