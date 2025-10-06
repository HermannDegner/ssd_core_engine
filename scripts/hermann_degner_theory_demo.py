"""
Hermann Degner構造主観力学理論 - 完全実装デモ
SSD Theory Comprehensive Demo

このデモはHermann Degnerの構造主観力学理論の6つの核心概念すべてを実演します：
1. 意味圧 (Meaning Pressure)
2. 整合 (Alignment) 
3. 跳躍 (Leap)
4. 四層構造 (Four-Layer Structure)
5. 構造観照（テオーリア）(Structural Theoria)
6. 語り圏深度モデル (Narrative Sphere Depth Model)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from ssd_core_engine import SSDCoreEngine, LayerType, ObjectInfo
    from ssd_core_engine.ssd_enhanced_leap import LeapType
    print("✅ パッケージから正常にインポート")
    PACKAGE_MODE = True
except ImportError:
    print("⚠️ パッケージモードでインポートできません。直接実行モードを試行します...")
    PACKAGE_MODE = False
    try:
        # 直接実行モード
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ssd_core_engine'))
        from ssd_engine import SSDCoreEngine
        from ssd_types import LayerType, ObjectInfo
        from ssd_enhanced_leap import LeapType
        print("✅ 直接実行モードで正常にインポート")
    except ImportError as e:
        print(f"❌ インポートエラー: {e}")
        print("パッケージのインストールを確認してください: pip install ssd-core-engine")
        sys.exit(1)


def print_section_header(title: str):
    """セクションヘッダーの出力"""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")


def print_subsection(title: str):
    """サブセクションヘッダーの出力"""
    print(f"\n--- {title} ---")


def demonstrate_hermann_degner_ssd_theory():
    """Hermann Degner構造主観力学理論の完全デモンストレーション"""
    
    print("🚀 Hermann Degner構造主観力学（SSD）理論 - 完全実装デモ")
    print(f"理論リポジトリ: https://github.com/HermannDegner/Structural-Subjectivity-Dynamics")
    print(f"パッケージモード: {PACKAGE_MODE}")
    
    # エンジンの初期化
    print_section_header("エンジン初期化")
    engine = SSDCoreEngine(agent_id="ssd_theory_demo")
    print(f"✅ SSDCoreEngine初期化完了: {engine.agent_id}")
    print(f"拡張機能有効: {engine.enhanced_ssd_features}")
    
    # 理論の包括的分析
    print_section_header("Hermann Degner理論の包括的分析")
    comprehensive_analysis = engine.get_comprehensive_ssd_analysis()
    
    print("🔬 理論フレームワーク:")
    print(f"  {comprehensive_analysis['theoretical_framework']}")
    
    print("\n🎯 6つの核心概念:")
    for concept, description in comprehensive_analysis['core_concepts'].items():
        print(f"  • {concept}: {description}")
    
    print(f"\n⚙️ 理論準拠性:")
    for key, value in comprehensive_analysis['theoretical_compliance'].items():
        status = "✅" if value else "❌"
        print(f"  {status} {key}: {value}")
    
    # 1. 四層構造システムのデモ
    print_section_header("1. 四層構造システム (Four-Layer Structure)")
    
    # 各層に構造要素を追加
    layers_demo = {
        LayerType.PHYSICAL: "物理制約（呼吸、重力）",
        LayerType.BASE: "生存本能（食欲、恐怖）", 
        LayerType.CORE: "価値観（正義感、愛情）",
        LayerType.UPPER: "抽象概念（哲学、数学）"
    }
    
    for layer, description in layers_demo.items():
        engine.add_structural_element(layer, f"demo_{layer.value}", stability=0.7)
        print(f"📍 {layer.value.upper()}: {description}")
    
    print("\n🏗️ 四層構造の状態:")
    for layer_info in comprehensive_analysis['current_system_state']['four_layer_structure'].items():
        layer_name, info = layer_info
        print(f"  {layer_name}: 構造数={info['structure_count']}, 安定性={info['total_stability']:.2f}, 流動性={info['mobility']}")
    
    # 2. 意味圧システムのデモ
    print_section_header("2. 意味圧システム (Meaning Pressure)")
    
    # 様々な意味圧を加える
    meaning_pressures = [
        ("食物発見", 0.8, "生存に関わる強い意味圧"),
        ("社会的批判", 0.6, "中程度の社会的意味圧"),
        ("抽象的疑問", 0.3, "軽微な知的意味圧")
    ]
    
    for source, pressure, description in meaning_pressures:
        engine.meaning_processor.add_meaning_pressure(pressure, source)
        print(f"💫 {source}: 圧力={pressure}, {description}")
    
    current_pressure = engine.meaning_processor.E
    print(f"\n⚡ 現在の未処理意味圧: {current_pressure:.3f}")
    
    # 3. カオス的跳躍システムのデモ
    print_section_header("3. カオス的跳躍システム (Chaotic Leap)")
    
    if engine.enhanced_ssd_features:
        print("🌪️ 真の非線形カオス跳躍システムを実行中...")
        
        # 各層で跳躍分析を実行
        for layer in LayerType:
            leap_analysis = engine.perform_chaotic_leap_analysis(current_pressure * 0.3, layer)
            
            if leap_analysis.get("leap_occurred"):
                leap_event = leap_analysis["leap_event"]
                print(f"🚀 {layer.value}層で跳躍発生!")
                print(f"   種類: {leap_event['leap_type']}")
                print(f"   強度: {leap_event['magnitude']:.3f}")
                print(f"   予測困難性: {1.0 - leap_event['predictability']:.3f}")
                print(f"   エネルギー放出: {leap_event['energy_release']:.3f}")
            else:
                print(f"⚖️ {layer.value}層: 整合状態維持（跳躍なし）")
        
        # 跳躍パターンの分析
        if engine.chaotic_leap_processor.leap_history:
            patterns = engine.chaotic_leap_processor.analyze_leap_patterns()
            print(f"\n📊 跳躍パターン分析:")
            for key, value in patterns.items():
                print(f"   {key}: {value:.3f}")
    else:
        print("❌ 拡張機能が利用できません")
    
    # 4. 構造観照（テオーリア）のデモ
    print_section_header("4. 構造観照（テオーリア）(Structural Theoria)")
    
    if engine.enhanced_ssd_features:
        print("👁️ 価値判断を保留した純粋な構造分析を実行中...")
        
        # 現象の客観的分析
        phenomenon = "AIが人間の仕事を奪うという議論"
        theoria_analysis = engine.perform_structural_theoria_analysis(phenomenon)
        
        print(f"🔬 分析対象: {phenomenon}")
        print(f"📊 テオーリア分析結果:")
        analysis_data = theoria_analysis["theoria_analysis"]
        print(f"   構造数: {len(analysis_data.get('structures', []))}")
        print(f"   意味圧源数: {len(analysis_data.get('meaning_pressures', []))}")
        print(f"   判断保留: {theoria_analysis['judgment_suspension']}")
        print(f"   感情的距離: {theoria_analysis['emotional_distance']}")
        print(f"⚠️ {theoria_analysis['warning']}")
    else:
        print("❌ 構造観照機能が利用できません")
    
    # 5. 語り圏深度モデルのデモ
    print_section_header("5. 語り圏深度モデル (Narrative Sphere Depth Model)")
    
    if engine.enhanced_ssd_features:
        print("🌐 L1-L5実在性階層分析を実行中...")
        
        # 様々な深度の語りを分析
        narratives = [
            ("水の沸点は100度である", "L1: 客観的事実"),
            ("進化論によれば生物は変化する", "L2: 科学的解釈"),
            ("常識的に考えて挨拶は大切だ", "L3: 社会的合意"),
            ("私は自由が最も重要だと信じている", "L4: 個人的信念"),
            ("神は愛である", "L5: 絶対的存在")
        ]
        
        for narrative, expected in narratives:
            depth_analysis = engine.analyze_narrative_depth(narrative, LayerType.CORE)
            
            print(f"\n📝 語り: 「{narrative}」")
            print(f"   分類: {depth_analysis['depth_level']} (期待: {expected})")
            print(f"   信頼度: {depth_analysis['classification_confidence']:.3f}")
            print(f"   中核層への影響: {depth_analysis['target_layer_influence']:.3f}")
    else:
        print("❌ 語り圏深度モデルが利用できません")
    
    # 6. 統合システムの協調動作デモ
    print_section_header("6. 統合システム協調動作")
    
    print("🔗 全システムの協調実行...")
    
    # シミュレーション実行
    try:
        from ssd_core_engine.ssd_utils import create_simple_world_objects
        perceived_objects = create_simple_world_objects()
    except ImportError:
        # フォールバック用の簡単なオブジェクト作成
        # ObjectInfoとLayerTypeは既にグローバルにインポート済み
        
        perceived_objects = [
            ObjectInfo(
                id="ethical_dilemma",
                type="decision_point",
                survival_relevance=0.9,
                meaning_values={
                    LayerType.PHYSICAL: 0.1,
                    LayerType.BASE: 0.7,
                    LayerType.CORE: 0.9,
                    LayerType.UPPER: 0.8
                }
            ),
            ObjectInfo(
                id="daily_routine", 
                type="habit",
                survival_relevance=0.2,
                meaning_values={
                    LayerType.PHYSICAL: 0.3,
                    LayerType.BASE: 0.2,
                    LayerType.CORE: 0.1,
                    LayerType.UPPER: 0.1
                }
            )
        ]
    
    actions = ["深く考える", "慣例に従う", "新しい視点を試す", "判断を保留する"]
    
    print("🎭 シナリオ: 倫理的ジレンマに直面")
    print(f"知覚オブジェクト: {[obj.id if hasattr(obj, 'id') else str(obj) for obj in (perceived_objects if isinstance(perceived_objects, list) else perceived_objects.keys())]}")
    print(f"可能な行動: {actions}")
    
    # ステップ実行
    result = engine.step(perceived_objects, actions)
    
    print(f"\n🎯 決定結果:")
    print(f"   選択行動: {result['decision']['chosen_action']}")
    print(f"   システムエネルギー: {result['system_state']['energy']['E']:.3f}")
    
    # 危機レベルは結果に含まれていない場合があるため、安全に取得
    crisis_level = result['system_state'].get('crisis_level', 0.0)
    print(f"   危機レベル: {crisis_level:.3f}")
    
    # 最終的な理論分析
    print_section_header("理論実装の完成度評価")
    
    final_analysis = engine.get_comprehensive_ssd_analysis()
    compliance = final_analysis['theoretical_compliance']
    
    total_features = len(compliance)
    active_features = sum(1 for v in compliance.values() if v)
    completion_rate = (active_features / total_features) * 100
    
    print(f"📊 Hermann Degner SSD理論実装完成度: {completion_rate:.1f}%")
    print(f"🎯 アクティブ機能: {active_features}/{total_features}")
    
    if completion_rate >= 80:
        print("🏆 優秀: 理論の核心概念が高い精度で実装されています")
    elif completion_rate >= 60:
        print("👍 良好: 基本的な理論要素が実装されています")
    else:
        print("⚠️ 改善余地: より多くの理論要素の実装が推奨されます")
    
    print(f"\n🔗 理論詳細: {comprehensive_analysis.get('SSD_THEORY_URL', 'https://github.com/HermannDegner/Structural-Subjectivity-Dynamics')}")
    print("✨ デモンストレーション完了")


def demonstrate_real_world_applications():
    """実世界応用例のデモ"""
    print_section_header("実世界応用例")
    
    engine = SSDCoreEngine(agent_id="real_world_demo")
    
    applications = [
        {
            "name": "ビジネス意思決定支援",
            "scenario": "新製品開発の判断",
            "meaning_pressures": {"市場競争": 0.8, "技術リスク": 0.6, "投資コスト": 0.7},
            "narrative": "この新技術は革命的だと業界専門家が言っている"
        },
        {
            "name": "教育システム設計", 
            "scenario": "カリキュラム改革の検討",
            "meaning_pressures": {"学生ニーズ": 0.9, "社会要請": 0.7, "予算制約": 0.5},
            "narrative": "教育は社会の基盤であり、常に改善が必要だ"
        },
        {
            "name": "心理療法支援",
            "scenario": "クライエントの心理状態分析", 
            "meaning_pressures": {"トラウマ": 0.9, "社会復帰": 0.6, "家族関係": 0.7},
            "narrative": "私はもうダメな人間なのかもしれない"
        }
    ]
    
    for app in applications:
        print_subsection(app["name"])
        print(f"シナリオ: {app['scenario']}")
        
        # 意味圧の設定
        for source, pressure in app["meaning_pressures"].items():
            engine.meaning_processor.add_meaning_pressure(pressure, source)
        
        # 語り圏深度分析（拡張機能有効時）
        if engine.enhanced_ssd_features:
            depth_analysis = engine.analyze_narrative_depth(app["narrative"])
            print(f"語り分析: {depth_analysis['depth_level']} (信頼度: {depth_analysis['classification_confidence']:.2f})")
        
        # 構造観照による客観分析（拡張機能有効時）
        if engine.enhanced_ssd_features:
            theoria = engine.perform_structural_theoria_analysis(app["scenario"])
            print(f"テオーリア分析: 構造{len(theoria['theoria_analysis'].get('structures', []))}個識別")
        
        # システム推奨（ObjectInfoオブジェクトを作成）
        actions = ["詳細分析", "段階的実施", "現状維持", "根本的変更"] 
        
        # 意味圧をObjectInfoに変換
        meaning_objects = []
        for source, pressure in app["meaning_pressures"].items():
            obj = ObjectInfo(
                id=source,
                type="pressure_source",
                survival_relevance=pressure,
                meaning_values={
                    LayerType.PHYSICAL: pressure * 0.2,
                    LayerType.BASE: pressure * 0.6,
                    LayerType.CORE: pressure * 0.8,
                    LayerType.UPPER: pressure * 0.4
                }
            )
            meaning_objects.append(obj)
        
        result = engine.step(meaning_objects, actions)
        print(f"推奨行動: {result['decision']['chosen_action']}")
        crisis_level = result['system_state'].get('crisis_level', 0.0)
        print(f"システム信頼度: {1.0 - crisis_level:.2f}")


if __name__ == "__main__":
    print("🎯 Hermann Degner構造主観力学理論 - 完全実装デモ開始\n")
    
    try:
        # メインデモ
        demonstrate_hermann_degner_ssd_theory()
        
        # 実世界応用例
        demonstrate_real_world_applications()
        
        print(f"\n🎉 全デモンストレーション正常終了")
        print(f"📚 Hermann Degner理論について更に学ぶ:")
        print(f"   https://github.com/HermannDegner/Structural-Subjectivity-Dynamics")
        
    except Exception as e:
        print(f"\n❌ エラー発生: {e}")
        import traceback
        print(traceback.format_exc())
        print(f"\n🔧 トラブルシューティング:")
        print(f"   1. パッケージの正常インストールを確認: pip install ssd-core-engine")
        print(f"   2. Python 3.8以上を使用していることを確認")
        print(f"   3. 依存関係を確認: pip install numpy typing-extensions")