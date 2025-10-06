"""
SSD Core Engine - Main Integration Module
構造主観力学 汎用AIコアエンジン - メイン統合モジュール
"""

import numpy as np
import random
from typing import Dict, List, Tuple, Any, Optional
from collections import defaultdict, deque

# 内部モジュールのインポート
try:
    from .ssd_types import (
        LayerType, ObjectInfo, StructuralState, AlignmentResult, 
        LeapResult, DecisionInfo, PredictionResult, SystemState
    )
    from .ssd_meaning_pressure import MeaningPressureProcessor
    from .ssd_alignment_leap import AlignmentProcessor, LeapProcessor
    from .ssd_decision import DecisionSystem, ActionEvaluator
    from .ssd_prediction import PredictionSystem
    from .ssd_utils import SystemMonitor, MaintenanceManager
except ImportError:
    # 開発時の直接実行用フォールバック
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    from ssd_types import (
        LayerType, ObjectInfo, StructuralState, AlignmentResult, 
        LeapResult, DecisionInfo, PredictionResult, SystemState
    )
    from ssd_meaning_pressure import MeaningPressureProcessor
    from ssd_alignment_leap import AlignmentProcessor, LeapProcessor
    from ssd_decision import DecisionSystem, ActionEvaluator
    from ssd_prediction import PredictionSystem
    from ssd_utils import SystemMonitor, MaintenanceManager


class SSDCoreEngine:
    """構造主観力学 コアエンジン - 統合クラス"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        
        # 四層構造システム
        self.layers: Dict[LayerType, Dict[str, StructuralState]] = {
            LayerType.PHYSICAL: {},
            LayerType.BASE: {},
            LayerType.CORE: {},
            LayerType.UPPER: {}
        }
        
        # 層間の動きやすさ係数
        self.layer_mobility = {
            LayerType.PHYSICAL: 0.1,  # 最も動きにくい
            LayerType.BASE: 0.3,      
            LayerType.CORE: 0.6,      
            LayerType.UPPER: 0.9      # 最も動きやすい
        }
        
        # システムコンポーネントの初期化
        self.meaning_processor = MeaningPressureProcessor()
        self.alignment_processor = AlignmentProcessor(self.layer_mobility)
        self.leap_processor = LeapProcessor(self.layer_mobility)
        self.decision_system = DecisionSystem(self.layer_mobility)
        self.action_evaluator = ActionEvaluator()
        self.prediction_system = PredictionSystem()
        self.system_monitor = SystemMonitor()
        self.maintenance_manager = MaintenanceManager()
        
        # 主観的境界システム統合 (Hermann Degner理論ベース)
        try:
            from .ssd_subjective_boundary import SubjectiveBoundaryProcessor
            self.boundary_processor = SubjectiveBoundaryProcessor(self.layer_mobility)
            # 後方互換性のためのエイリアス
            self.territory_processor = self.boundary_processor
        except ImportError:
            try:
                from .ssd_territory import TerritoryProcessor
                self.territory_processor = TerritoryProcessor(self.layer_mobility)
                self.boundary_processor = self.territory_processor
            except ImportError:
                try:
                    from ssd_subjective_boundary import SubjectiveBoundaryProcessor
                    self.boundary_processor = SubjectiveBoundaryProcessor(self.layer_mobility)
                    self.territory_processor = self.boundary_processor
                except ImportError:
                    try:
                        from ssd_territory import TerritoryProcessor
                        self.territory_processor = TerritoryProcessor(self.layer_mobility)
                        self.boundary_processor = self.territory_processor
                    except ImportError:
                        self.territory_processor = None
                        self.boundary_processor = None
        
        # 🚀 Hermann Degner理論の完全実装 - 拡張機能
        try:
            from .ssd_enhanced_leap import ChaoticLeapProcessor, StructuralTheoria, NarrativeSphereDepthModel
            self.chaotic_leap_processor = ChaoticLeapProcessor()
            self.structural_theoria = StructuralTheoria()
            self.narrative_depth_model = NarrativeSphereDepthModel()
            self.enhanced_ssd_features = True
        except ImportError:
            try:
                from ssd_enhanced_leap import ChaoticLeapProcessor, StructuralTheoria, NarrativeSphereDepthModel
                self.chaotic_leap_processor = ChaoticLeapProcessor()
                self.structural_theoria = StructuralTheoria()
                self.narrative_depth_model = NarrativeSphereDepthModel()
                self.enhanced_ssd_features = True
            except ImportError:
                self.chaotic_leap_processor = None
                self.structural_theoria = None
                self.narrative_depth_model = None
                self.enhanced_ssd_features = False
        
        # オブジェクト認知システム
        self.perceived_objects: Dict[str, ObjectInfo] = {}
        self.attention_focus: Optional[str] = None
        
        # システム状態
        self.current_time = 0
        self.experience_log = []

    def add_structural_element(self, layer: LayerType, element_id: str,
                             obj_or_connections = None,
                             stability: float = None):
        """構造要素を追加（ObjectInfoまたはコネクションを受け取る）"""
        if stability is None:
            stability = 1.0 / self.layer_mobility[layer]  # 層に応じた安定度

        # ObjectInfoが渡された場合とDict[str, float]が渡された場合を処理
        if isinstance(obj_or_connections, ObjectInfo):
            # ObjectInfoの場合は、perceived_objectsに追加してStructuralStateを作成
            self.perceived_objects[obj_or_connections.id] = obj_or_connections
            initial_connections = {}
        elif isinstance(obj_or_connections, dict):
            # 辞書の場合は接続情報として扱う
            initial_connections = obj_or_connections
        else:
            # その他の場合は空の接続
            initial_connections = obj_or_connections or {}

        self.layers[layer][element_id] = StructuralState(
            layer=layer,
            connections=initial_connections,
            stability=stability
        )

    def perceive_object(self, obj_info: ObjectInfo) -> float:
        """オブジェクトを知覚・認識"""
        self.perceived_objects[obj_info.id] = obj_info
        
        # 意味圧を計算して追加
        total_pressure = self.meaning_processor.calculate_total_pressure(
            obj_info, self.layers, self.layer_mobility
        )
        
        return total_pressure
    
    def process_alignment_step(self) -> AlignmentResult:
        """整合ステップの実行"""
        result = self.alignment_processor.process_alignment_step(
            self.layers, self.meaning_processor.E
        )
        
        # 未処理圧の自然減衰
        self.meaning_processor.natural_decay()
        
        return result
    
    def check_leap_condition(self) -> bool:
        """跳躍条件をチェック"""
        return self.leap_processor.check_leap_condition(
            self.meaning_processor.E,
            self.alignment_processor.global_kappa,
            self.perceived_objects
        )
    
    def execute_leap(self) -> LeapResult:
        """跳躍の実行"""
        leap_result, new_E = self.leap_processor.execute_leap(
            self.layers, self.perceived_objects, self.meaning_processor.E
        )
        
        # 未処理圧を更新
        self.meaning_processor.E = new_E
        
        # 体験として記録
        self.experience_log.append({
            'event': 'leap',
            'result': leap_result,
            'timestamp': self.current_time
        })
        
        return leap_result
    
    def make_decision(self, available_actions: List[str]) -> Tuple[str, DecisionInfo]:
        """意思決定システム"""
        if not available_actions:
            return None, DecisionInfo(chosen_action="")
        
        chosen_action, decision_info = self.decision_system.make_decision(
            available_actions, self.layers, self.alignment_processor.global_kappa,
            self.perceived_objects, self.meaning_processor.E
        )
        
        return chosen_action, decision_info
    
    def update_temperature(self):
        """探索温度の更新"""
        self.decision_system.update_temperature(self.meaning_processor.E)
    
    def predict_future_state(self, target_object_id: str, steps_ahead: int = None) -> PredictionResult:
        """未来状態予測"""
        return self.prediction_system.predict_future_state(
            target_object_id, self.perceived_objects, steps_ahead, self.current_time
        )
    
    def predict_multiple_futures(self, object_ids: List[str], steps_ahead: int = None) -> Dict[str, Any]:
        """複数オブジェクトの未来予測"""
        return self.prediction_system.predict_multiple_futures(
            object_ids, self.perceived_objects, steps_ahead, self.current_time
        )
    
    def detect_crisis_conditions(self) -> Dict[str, Any]:
        """危機状況の検出"""
        return self.prediction_system.detect_crisis_conditions(
            self.perceived_objects, self.current_time
        )
    
    def get_system_state(self) -> SystemState:
        """システム状態の取得"""
        # メモリ使用量の概算
        memory_usage = {
            'prediction_cache': len(self.prediction_system.prediction_cache),
            'similarity_cache': len(getattr(self.meaning_processor, '_similarity_cache', {})),
            'experience_log': len(self.experience_log),
            'trend_memory': len(self.prediction_system.trend_memory)
        }
        
        # レイヤー統計の効率的計算
        layer_stats = {}
        total_elements = 0
        total_connections = 0
        
        for layer, elements in self.layers.items():
            if elements:
                activations = [state.activation for state in elements.values()]
                stabilities = [state.stability for state in elements.values()]
                connections = sum(len(state.connections) for state in elements.values())
                
                layer_stats[layer.value] = {
                    'element_count': len(elements),
                    'avg_activation': np.mean(activations),
                    'avg_stability': np.mean(stabilities),
                    'total_connections': connections,
                    'connection_density': connections / len(elements) if elements else 0.0
                }
                
                total_elements += len(elements)
                total_connections += connections
            else:
                layer_stats[layer.value] = {
                    'element_count': 0,
                    'avg_activation': 0.0,
                    'avg_stability': 0.0,
                    'total_connections': 0,
                    'connection_density': 0.0
                }
        
        return SystemState(
            agent_id=self.agent_id,
            energy={'E': self.meaning_processor.E, 'T': self.decision_system.T},
            structure={
                'total_elements': total_elements,
                'total_connections': total_connections,
                'layer_stats': layer_stats
            },
            cognition={
                'perceived_objects': len(self.perceived_objects),
                'decision_history_length': len(self.decision_system.decision_history),
                'global_kappa_size': len(self.alignment_processor.global_kappa),
                'kappa_mean': np.mean(list(self.alignment_processor.global_kappa.values())) if self.alignment_processor.global_kappa else 0.0
            },
            memory_usage=memory_usage,
            performance={
                'prediction_horizon': self.prediction_system.prediction_horizon,
                'prediction_accuracy': self.prediction_system.prediction_accuracy
            }
        )
    
    def step(self, perceived_objects: List[ObjectInfo] = None, 
             available_actions: List[str] = None) -> Dict[str, Any]:
        """1ステップの実行（数理完全性向上版）"""
        step_result = {}
        self.current_time += 1
        
        # 1. オブジェクト知覚
        if perceived_objects:
            perception_results = []
            for obj in perceived_objects:
                pressure = self.perceive_object(obj)
                perception_results.append({
                    'object': obj.id,
                    'pressure': pressure
                })
            step_result['perception'] = perception_results
        
        # 2. 整合処理（従来版）
        alignment_result = self.process_alignment_step()
        step_result['alignment'] = alignment_result
        
        # 2b. 熱損失を考慮した整合処理（新機能）
        try:
            alignment_work = self.alignment_processor.process_alignment_step_with_heat_loss(
                self.layers, self.meaning_processor.E
            )
            thermal_stats = self.alignment_processor.get_alignment_statistics()
            step_result['thermal_dynamics'] = {
                'alignment_work': alignment_work,
                'thermal_stats': thermal_stats
            }
        except AttributeError:
            # フォールバック（古いシステム）
            step_result['thermal_dynamics'] = {'status': 'legacy_mode'}
        
        # 2c. 二段階反応システム（新機能）
        if perceived_objects and hasattr(self.leap_processor, 'reaction_system'):
            for obj in perceived_objects:
                try:
                    stimulus = {
                        'type': obj.type,
                        'intensity': min(obj.current_value / 100.0, 1.0),
                        'social_context': obj.type in ['social', 'tool'],
                        'danger_level': obj.properties.get('danger_level', 0.0),
                        'value_alignment': 0.5,
                        'long_term_benefit': 0.5
                    }
                    
                    immediate_reaction = self.leap_processor.process_stimulus_reaction(
                        stimulus, float(self.current_time)
                    )
                    step_result[f'immediate_reaction_{obj.id}'] = immediate_reaction
                except (AttributeError, TypeError):
                    continue
            
            # 意識的再処理の更新
            try:
                conscious_reactions = self.leap_processor.update_conscious_processing(
                    float(self.current_time), self.layers
                )
                if conscious_reactions:
                    step_result['conscious_reactions'] = conscious_reactions
            except (AttributeError, TypeError):
                pass
        
        # 3. 跳躍判定・実行
        if self.check_leap_condition():
            leap_result = self.execute_leap()
            step_result['leap'] = leap_result
        
        # 4. 温度更新
        self.update_temperature()
        
        # 5. 意思決定
        if available_actions:
            decision, decision_info = self.make_decision(available_actions)
            step_result['decision'] = {
                'chosen_action': decision,
                'info': decision_info.__dict__
            }
        
        # 6. システム状態
        step_result['system_state'] = self.get_system_state().__dict__
        
        # 7. 定期メンテナンス
        maintenance_needed = self.maintenance_manager.should_perform_maintenance(self.current_time)
        if any(maintenance_needed.values()):
            maintenance_report = self.system_maintenance()
            step_result['maintenance'] = maintenance_report
        
        return step_result
    
    def system_maintenance(self) -> Dict[str, Any]:
        """システムメンテナンス"""
        maintenance_report = {
            'cache_cleanup': False,
            'memory_optimization': False,
            'stability_check': True
        }
        
        # 各コンポーネントのクリーンアップ
        components = {
            'prediction_system': self.prediction_system,
            'meaning_processor': self.meaning_processor
        }
        
        report = self.maintenance_manager.execute_maintenance(components, self.current_time)
        maintenance_report.update(report)
        
        # 構造的安定性の自動調整
        self._auto_stabilize_structure()
        
        # 経験ログの圧縮
        if len(self.experience_log) > 200:
            self._compress_experience_log()
            maintenance_report['memory_optimization'] = True
        
        return maintenance_report
    
    def _auto_stabilize_structure(self):
        """構造的安定性の自動調整"""
        for layer in LayerType:
            if layer in self.layers:
                elements_to_remove = []
                for element_id, state in self.layers[layer].items():
                    # 過度に活性化した要素の安定化
                    if state.activation > 0.9:
                        state.stability = min(1.0, state.stability + 0.1)
                        state.activation *= 0.9
                    
                    # 非活性要素の削除（メモリ効率化）
                    if state.activation < 0.05 and len(state.connections) == 0:
                        if random.random() < 0.1:  # 10%確率で削除
                            elements_to_remove.append(element_id)
                
                # 安全な削除処理
                for element_id in elements_to_remove:
                    del self.layers[layer][element_id]
    
    def _compress_experience_log(self):
        """経験ログの圧縮"""
        if len(self.experience_log) <= 100:
            return
        
        # 古い経験を統計的要約に変換
        old_experiences = self.experience_log[:-100]  # 最新100以外
        
        # 圧力統計
        pressure_stats = {
            'mean_pressure': np.mean([exp.get('pressure', 0) for exp in old_experiences if 'pressure' in exp]),
            'max_pressure': max([exp.get('pressure', 0) for exp in old_experiences if 'pressure' in exp], default=0),
            'leap_count': sum(1 for exp in old_experiences if exp.get('event') == 'leap'),
            'compressed_from': len(old_experiences)
        }
        
        # 統計を経験ログに追加
        self.experience_log = self.experience_log[-100:]  # 最新100のみ保持
        self.experience_log.append({
            'event': 'compression_summary',
            'stats': pressure_stats,
            'timestamp': self.current_time
        })
    
    def get_performance_metrics(self) -> Dict[str, float]:
        """パフォーマンス指標の取得"""
        return self.system_monitor.generate_performance_report(
            self.layers, 
            list(self.decision_system.decision_history),
            self.alignment_processor.global_kappa
        )
    
    def get_health_status(self) -> Dict[str, Any]:
        """システムヘルス状況の取得"""
        system_state = self.get_system_state()
        return self.system_monitor.check_system_health(system_state)
    
    # ======= 主観的境界システムメソッド (Hermann Degner理論) =======
    
    def create_boundary_v2(self, center: Tuple[float, float], radius: float, owner_npc: str) -> str:
        """主観的境界作成（Hermann Degner理論v2版）"""
        if not self.boundary_processor:
            return None
            
        # 主観的境界経験を処理して境界作成
        boundary_result = self.boundary_processor.process_boundary_experience(
            npc_id=owner_npc,
            location=center,
            experience_type='safe_rest',
            experience_valence=0.8,  # 高い安心感
            tick=self.current_time
        )
        
        # 作成された主観的境界IDを返す
        for change in boundary_result.get('boundary_changes', []):
            if change.get('action') in ['boundary_claimed', 'new_boundary_created', 'new_boundary']:
                return change.get('boundary_id') or change.get('boundary_info', {}).get('boundary_id')
        
        return None
    
    # 後方互換性エイリアス
    def create_territory_v2(self, center: Tuple[float, float], radius: float, owner_npc: str) -> str:
        """縄張り作成（v2版） - 後方互換性エイリアス"""
        return self.create_boundary_v2(center, radius, owner_npc)
    
    def check_boundary_contains_v2(self, boundary_id: str, location: Tuple[float, float]) -> bool:
        """主観的境界内包含チェック（Hermann Degner理論v2版）"""
        if not self.boundary_processor or not boundary_id:
            return False
            
        # 主観的境界情報を取得
        boundary = self.boundary_processor.boundaries.get(boundary_id)
        return boundary.contains(location) if boundary else False
    
    # 後方互換性エイリアス
    def check_territory_contains_v2(self, territory_id: str, location: Tuple[float, float]) -> bool:
        """縄張り内包含チェック（v2版） - 後方互換性エイリアス"""
        return self.check_boundary_contains_v2(territory_id, location)
    
    def invite_to_boundary_v2(self, boundary_id: str, invitee_npc: str) -> bool:
        """主観的境界への招待（Hermann Degner理論v2版）"""
        if not self.boundary_processor or not boundary_id:
            return False
        return self.boundary_processor.add_npc_to_boundary(boundary_id, invitee_npc)
    
    # 後方互換性エイリアス
    def invite_to_territory_v2(self, territory_id: str, invitee_npc: str) -> bool:
        """縄張りへの招待（v2版） - 後方互換性エイリアス"""
        return self.invite_to_boundary_v2(territory_id, invitee_npc)
        
        # 招待者を縄張りに追加
        territory.add_member(invitee_npc)
        
        # NPCの縄張りマッピングを更新
        self.territory_processor.npc_territories[invitee_npc] = territory_id
        
        return True
        
    def get_boundary_info(self, boundary_id: str) -> Optional[Dict]:
        """主観的境界情報取得（Hermann Degner理論）"""
        if not self.boundary_processor or not boundary_id:
            return None
            
        boundary = self.boundary_processor.boundaries.get(boundary_id)
        if not boundary:
            return None
            
        return {
            'boundary_id': boundary.boundary_id,
            'center': boundary.center,
            'radius': boundary.radius,
            'owner': boundary.owner_npc,
            'members': list(boundary.members),
            'boundary_strength': boundary.boundary_strength,
            'established_tick': boundary.established_tick,
        }
    
    # 後方互換性エイリアス
    def get_territory_info(self, territory_id: str) -> Optional[Dict]:
        """縄張り情報取得 - 後方互換性エイリアス"""
        return self.get_boundary_info(territory_id)
    
    # 🚀 Hermann Degner理論の完全実装 - 新メソッド群
    
    def perform_chaotic_leap_analysis(self, meaning_pressure: float, layer: LayerType) -> Dict[str, any]:
        """
        カオス的跳躍分析の実行
        
        Hermann Degner理論の核心：真の非線形性・予測困難性の実装
        """
        if not self.enhanced_ssd_features or not self.chaotic_leap_processor:
            return {"error": "拡張機能が利用できません"}
        
        # 現在の整合状態を取得
        layer_structures = self.layers.get(layer, {})
        total_alignment = sum(state.stability for state in layer_structures.values()) / max(1, len(layer_structures))
        
        # 真のカオス的跳躍分析
        leap_event = self.chaotic_leap_processor.execute_leap(
            meaning_pressure, total_alignment, layer, layer_structures
        )
        
        # 跳躍パターン分析
        patterns = self.chaotic_leap_processor.analyze_leap_patterns()
        
        # システム状態
        system_state = self.chaotic_leap_processor.get_system_state()
        
        return {
            "leap_occurred": leap_event is not None,
            "leap_event": leap_event.__dict__ if leap_event else None,
            "patterns": patterns,
            "system_state": system_state,
            "theoretical_basis": "Hermann_Degner_SSD_Chaos_Theory"
        }
    
    def perform_structural_theoria_analysis(self, phenomenon_description: str, 
                                          phenomenon_data: Dict = None) -> Dict[str, any]:
        """
        構造観照（テオーリア）による客観的分析
        
        Hermann Degner理論：判断保留による純粋な構造分析
        """
        if not self.enhanced_ssd_features or not self.structural_theoria:
            return {"error": "構造観照機能が利用できません"}
        
        # 現象データの準備
        if phenomenon_data is None:
            phenomenon_data = {
                "description": phenomenon_description,
                "current_structures": {
                    layer.value: list(structures.keys()) 
                    for layer, structures in self.layers.items()
                },
                "energy_sources": [self.meaning_processor.E],
                "hierarchy": ["physical", "base", "core", "upper"]
            }
        
        # 構造観照による客観的分析
        analysis = self.structural_theoria.analyze_phenomenon_objectively(phenomenon_data)
        
        return {
            "theoria_analysis": analysis,
            "judgment_suspension": self.structural_theoria.judgment_suspension,
            "emotional_distance": self.structural_theoria.emotional_distance,
            "theoretical_basis": "Hermann_Degner_Structural_Theoria",
            "warning": "この分析は価値判断を含まず、純粋な構造分析です"
        }
    
    def analyze_narrative_depth(self, narrative_text: str, target_layer: LayerType = None) -> Dict[str, any]:
        """
        語り圏深度モデルによる分析
        
        Hermann Degner理論：L1-L5の実在性階層分析
        """
        if not self.enhanced_ssd_features or not self.narrative_depth_model:
            return {"error": "語り圏深度モデルが利用できません"}
        
        # 語りの深度分類
        depth_level, confidence = self.narrative_depth_model.classify_narrative_depth(narrative_text)
        
        # 各層への影響力計算
        layer_influences = {}
        for layer in LayerType:
            influence = self.narrative_depth_model.calculate_narrative_influence(depth_level, layer)
            layer_influences[layer.value] = influence
        
        # 特定層への影響（指定された場合）
        target_influence = None
        if target_layer:
            target_influence = self.narrative_depth_model.calculate_narrative_influence(depth_level, target_layer)
        
        return {
            "narrative": narrative_text,
            "depth_level": depth_level.name,
            "depth_value": depth_level.value,
            "classification_confidence": confidence,
            "layer_influences": layer_influences,
            "target_layer_influence": target_influence,
            "theoretical_basis": "Hermann_Degner_Narrative_Sphere_Depth_Model",
            "depth_explanation": {
                1: "L1: 客観的事実",
                2: "L2: 科学的解釈", 
                3: "L3: 社会的合意",
                4: "L4: 個人的信念",
                5: "L5: 神・絶対的存在"
            }
        }
    
    def get_comprehensive_ssd_analysis(self) -> Dict[str, any]:
        """
        Hermann Degner構造主観力学理論の包括的分析
        
        理論の6つの核心概念すべてを統合した分析
        """
        if not self.enhanced_ssd_features:
            return {"error": "拡張SSD機能が利用できません", "basic_features_only": True}
        
        analysis = {
            "theoretical_framework": "Hermann_Degner_Structural_Subjectivity_Dynamics",
            "core_concepts": {
                "meaning_pressure": "意味圧 - 構造に作用するあらゆるエネルギー・影響",
                "alignment": "整合 - エネルギー効率の良い安定状態維持", 
                "leap": "跳躍 - 非連続的で予測困難な構造変化",
                "four_layer_structure": "四層構造 - 物理・基層・中核・上層の階層",
                "structural_theoria": "構造観照 - 判断保留による冷静分析",
                "narrative_depth": "語り圏深度 - L1-L5の実在性階層"
            },
            "current_system_state": {}
        }
        
        # 1. 意味圧状態
        analysis["current_system_state"]["meaning_pressure"] = {
            "total_pressure": self.meaning_processor.E,
            "experience_count": len(self.meaning_processor.experience_log)
        }
        
        # 2. 四層構造状態
        analysis["current_system_state"]["four_layer_structure"] = {}
        for layer in LayerType:
            layer_structures = self.layers.get(layer, {})
            analysis["current_system_state"]["four_layer_structure"][layer.value] = {
                "structure_count": len(layer_structures),
                "total_stability": sum(s.stability for s in layer_structures.values()),
                "mobility": self.layer_mobility.get(layer, 0.5)
            }
        
        # 3. カオス跳躍システム状態
        if self.chaotic_leap_processor:
            analysis["current_system_state"]["chaotic_leap_system"] = self.chaotic_leap_processor.get_system_state()
        
        # 4. 構造観照状態
        if self.structural_theoria:
            analysis["current_system_state"]["structural_theoria"] = {
                "judgment_suspension": self.structural_theoria.judgment_suspension,
                "emotional_distance": self.structural_theoria.emotional_distance,
                "analytical_mode": self.structural_theoria.analytical_mode
            }
        
        # 5. 主観的境界システム（Hermann Degner理論統合）
        if self.boundary_processor:
            analysis["current_system_state"]["subjective_boundary_system"] = {
                "boundary_count": len(self.boundary_processor.boundaries),
                "total_npcs": len(getattr(self.boundary_processor, 'npc_boundaries', {})),
                "subjective_boundaries": len(self.boundary_processor.subjective_boundaries)
            }
        elif self.territory_processor:
            # 後方互換性
            analysis["current_system_state"]["territory_system"] = {
                "territory_count": len(getattr(self.territory_processor, 'territories', {})),
                "total_npcs": len(getattr(self.territory_processor, 'npc_territories', {}))
            }
        
        # 6. システム全体の理論準拠性
        analysis["theoretical_compliance"] = {
            "hermann_degner_theory_implementation": True,
            "enhanced_features_active": self.enhanced_ssd_features,
            "chaos_theory_integration": self.chaotic_leap_processor is not None,
            "theoria_capability": self.structural_theoria is not None,
            "narrative_depth_analysis": self.narrative_depth_model is not None
        }
        
        return analysis


# エクスポート用の関数
def create_ssd_engine(agent_id: str = "default_agent") -> SSDCoreEngine:
    """SSDエンジンの作成"""
    return SSDCoreEngine(agent_id)


def setup_basic_structure(engine: SSDCoreEngine):
    """基本構造要素の設定"""
    # 基本構造要素を追加
    engine.add_structural_element(LayerType.PHYSICAL, "survival_instinct")
    engine.add_structural_element(LayerType.BASE, "hunger_drive")
    engine.add_structural_element(LayerType.BASE, "fear_response")
    engine.add_structural_element(LayerType.CORE, "self_preservation")
    engine.add_structural_element(LayerType.UPPER, "planning_ability")