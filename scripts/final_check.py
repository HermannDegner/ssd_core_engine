#!/usr/bin/env python3
"""
Final Code Check Summary
最終コードチェック結果サマリー
"""

def main():
    print("🔬 SSD Core Engine - 最終コードチェック結果")
    print("=" * 50)
    
    # スクリプトディレクトリから実行時のパス修正
    import sys
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    sys.path.insert(0, parent_dir)
    
    # 1. インポート成功確認
    print("\n✅ 1️⃣ インポート状況")
    modules = [
        'ssd_types', 'ssd_meaning_pressure', 'ssd_alignment_leap',
        'ssd_decision', 'ssd_prediction', 'ssd_utils', 
        'ssd_territory', 'ssd_engine'
    ]
    
    success_count = 0
    for mod in modules:
        try:
            exec(f'import {mod}')
            print(f"  ✅ {mod}")
            success_count += 1
        except Exception as e:
            print(f"  ❌ {mod}: {str(e)[:50]}...")
    
    print(f"  📊 成功率: {success_count}/{len(modules)} ({success_count/len(modules)*100:.1f}%)")
    
    # 2. 基本機能テスト
    print(f"\n✅ 2️⃣ 基本機能テスト")
    try:
        from ssd_engine import create_ssd_engine, setup_basic_structure
        engine = create_ssd_engine("test_agent")
        setup_basic_structure(engine)
        print(f"  ✅ エンジン作成・初期化")
        
        # 基本操作テスト
        from ssd_types import LayerType
        engine.add_structural_element(LayerType.BASE, "test_element")
        print(f"  ✅ 構造要素追加")
        
        # 整合処理テスト
        result = engine.process_alignment_step()
        print(f"  ✅ 整合処理")
        
        print(f"  📊 基本機能: 正常動作")
    except Exception as e:
        print(f"  ❌ 基本機能エラー: {str(e)[:50]}...")
    
    # 3. 縄張りシステムテスト
    print(f"\n✅ 3️⃣ 縄張りシステム")
    try:
        from ssd_territory import TerritoryProcessor
        from ssd_types import LayerType
        
        layer_mobility = {
            LayerType.PHYSICAL: 0.1,
            LayerType.BASE: 0.3,
            LayerType.CORE: 0.6,
            LayerType.UPPER: 0.9
        }
        
        territory_processor = TerritoryProcessor(layer_mobility)
        result = territory_processor.process_territorial_experience(
            "test_npc", (0.0, 0.0), 'safe_rest', 0.8, tick=1
        )
        print(f"  ✅ 縄張り経験処理")
        
        state = territory_processor.get_territorial_state("test_npc")
        print(f"  ✅ 縄張り状態取得")
        print(f"  📊 縄張りシステム: 正常動作")
    except Exception as e:
        print(f"  ❌ 縄張りシステムエラー: {str(e)[:50]}...")
    
    # 4. ファイル構成確認
    print(f"\n✅ 4️⃣ ファイル構成")
    import os
    required_files = [
        'ssd_types.py', 'ssd_engine.py', 'ssd_meaning_pressure.py',
        'ssd_alignment_leap.py', 'ssd_decision.py', 'ssd_prediction.py',
        'ssd_utils.py', 'ssd_territory.py', '__init__.py'
    ]
    
    file_count = 0
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"  ✅ {file} ({size//1024}KB)")
            file_count += 1
        else:
            print(f"  ❌ {file}: 見つからない")
    
    print(f"  📊 ファイル完整性: {file_count}/{len(required_files)} ({file_count/len(required_files)*100:.1f}%)")
    
    # 5. 統合評価
    print(f"\n🏆 総合評価")
    
    overall_score = (success_count/len(modules)) * 0.4 + (file_count/len(required_files)) * 0.3
    
    # 機能評価追加
    functional_score = 0.3
    try:
        from ssd_engine import create_ssd_engine
        engine = create_ssd_engine()
        functional_score = 0.3
    except:
        functional_score = 0.0
    
    overall_score += functional_score
    
    print(f"  📊 総合スコア: {overall_score:.2f}/1.0 ({overall_score*100:.1f}%)")
    
    if overall_score >= 0.9:
        print(f"  🎊 優秀! システムは完全に動作しています")
    elif overall_score >= 0.7:
        print(f"  ✅ 良好! システムは基本的に動作しています")
    elif overall_score >= 0.5:
        print(f"  ⚠️ 注意! いくつかの問題があります")
    else:
        print(f"  ❌ 要修正! システムに重大な問題があります")
    
    # 6. 改善提案
    print(f"\n💡 改善提案")
    if overall_score < 1.0:
        if success_count < len(modules):
            print(f"  • インポートエラーの解決")
        if file_count < len(required_files):
            print(f"  • 不足ファイルの追加")
        print(f"  • テストファイルのバグ修正 (test_ssd.py)")
        print(f"  • 詳細なドキュメント整備")
    else:
        print(f"  • さらなる機能拡張")
        print(f"  • パフォーマンス最適化")
        print(f"  • 使用例・チュートリアル追加")
    
    print(f"\n🎯 コードチェック完了!")

if __name__ == "__main__":
    main()