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
    from ssd_types import (
        LayerType, ObjectInfo, StructuralState, AlignmentResult, 
        LeapResult, DecisionInfo, PredictionResult, SystemState
    )
    from ssd_meaning_pressure import MeaningPressureProcessor
    from ssd_alignment_leap import AlignmentProcessor, LeapProcessor
    from ssd_decision import DecisionSystem, ActionEvaluator
    from ssd_prediction import PredictionSystem
    from ssd_utils import SystemMonitor, MaintenanceManager
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
        
        # オブジェクト認知システム
        self.perceived_objects: Dict[str, ObjectInfo] = {}
        self.attention_focus: Optional[str] = None
        
        # システム状態
        self.current_time = 0
        self.experience_log = []

    def add_structural_element(self, layer: LayerType, element_id: str, 
                             initial_connections: Dict[str, float] = None,
                             stability: float = None):
        """構造要素を追加"""
        if stability is None:
            stability = 1.0 / self.layer_mobility[layer]  # 層に応じた安定度
            
        self.layers[layer][element_id] = StructuralState(
            layer=layer,
            connections=initial_connections or {},
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