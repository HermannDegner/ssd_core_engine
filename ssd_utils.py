"""
SSD Utility Functions and Helper Classes
構造主観力学 - ユーティリティ関数
"""

import random
import numpy as np
from typing import Dict, List, Any
from ssd_types import ObjectInfo, LayerType, SystemState, StructuralState


def create_simple_world_objects() -> List[ObjectInfo]:
    """シンプルな世界のオブジェクトを作成"""
    objects = []
    
    # 基本オブジェクト
    food = ObjectInfo(
        id="food_item_1",
        type="food",
        properties={"nutrition": 50, "taste": "sweet"},
        current_value=80.0,
        decline_rate=2.0,
        volatility=0.15,
        meaning_values={
            LayerType.PHYSICAL: 0.2,
            LayerType.BASE: 0.8,      # 生存欲求に強く関連
            LayerType.CORE: 0.3,
            LayerType.UPPER: 0.1
        }
    )
    
    threat = ObjectInfo(
        id="threat_1", 
        type="danger",
        properties={"danger_level": 70, "distance": 10},
        current_value=70.0,
        decline_rate=0.5,
        volatility=0.3,
        meaning_values={
            LayerType.PHYSICAL: 0.9,  # 物理的脅威
            LayerType.BASE: 0.9,      # 生存脅威
            LayerType.CORE: 0.4,
            LayerType.UPPER: 0.2
        }
    )
    
    tool = ObjectInfo(
        id="tool_1",
        type="tool", 
        properties={"efficiency": 60, "durability": 80},
        current_value=60.0,
        decline_rate=0.2,
        volatility=0.1,
        meaning_values={
            LayerType.PHYSICAL: 0.3,
            LayerType.BASE: 0.4,
            LayerType.CORE: 0.6,
            LayerType.UPPER: 0.8      # 概念的価値が高い
        }
    )
    
    water = ObjectInfo(
        id="water_source_1",
        type="water",
        properties={"purity": 90, "quantity": 100},
        current_value=90.0,
        decline_rate=1.5,
        volatility=0.2,
        meaning_values={
            LayerType.PHYSICAL: 0.3,
            LayerType.BASE: 0.9,      # 生存に不可欠
            LayerType.CORE: 0.2,
            LayerType.UPPER: 0.1
        }
    )
    
    shelter = ObjectInfo(
        id="shelter_1",
        type="shelter",
        properties={"protection": 85, "comfort": 60},
        current_value=85.0,
        decline_rate=0.3,
        volatility=0.05,
        meaning_values={
            LayerType.PHYSICAL: 0.8,
            LayerType.BASE: 0.7,
            LayerType.CORE: 0.5,
            LayerType.UPPER: 0.3
        }
    )
    
    objects.extend([food, threat, tool, water, shelter])
    return objects


def create_survival_scenario_objects() -> List[ObjectInfo]:
    """生存シナリオ用のオブジェクトセットを作成"""
    objects = []
    
    # 危機的状況のオブジェクト
    depleting_water = ObjectInfo(
        id="water_critical",
        type="water",
        properties={"purity": 60, "quantity": 20},
        current_value=20.0,
        decline_rate=3.0,  # 急速に減少
        volatility=0.4,
        meaning_values={
            LayerType.PHYSICAL: 0.4,
            LayerType.BASE: 1.0,  # 最高優先度
            LayerType.CORE: 0.3,
            LayerType.UPPER: 0.1
        }
    )
    
    approaching_storm = ObjectInfo(
        id="storm_threat",
        type="danger",
        properties={"intensity": 90, "eta_hours": 2},
        current_value=90.0,
        decline_rate=-5.0,  # 増加する脅威
        volatility=0.6,
        meaning_values={
            LayerType.PHYSICAL: 1.0,
            LayerType.BASE: 0.9,
            LayerType.CORE: 0.6,
            LayerType.UPPER: 0.2
        }
    )
    
    medical_supplies = ObjectInfo(
        id="medicine_kit",
        type="medicine",
        properties={"effectiveness": 80, "quantity": 5},
        current_value=80.0,
        decline_rate=0.1,
        volatility=0.1,
        meaning_values={
            LayerType.PHYSICAL: 0.2,
            LayerType.BASE: 0.8,
            LayerType.CORE: 0.5,
            LayerType.UPPER: 0.4
        }
    )
    
    objects.extend([depleting_water, approaching_storm, medical_supplies])
    return objects


class SystemMonitor:
    """システム監視・診断クラス"""
    
    def __init__(self):
        self.monitoring_enabled = True
        self.alert_thresholds = {
            'high_energy': 8.0,
            'low_energy': 0.5,
            'high_temperature': 1.5,
            'memory_usage': 1000
        }
    
    def check_system_health(self, system_state: SystemState) -> Dict[str, Any]:
        """システムヘルスチェック"""
        health_report = {
            'status': 'healthy',
            'warnings': [],
            'errors': [],
            'recommendations': []
        }
        
        # エネルギーレベルチェック
        energy = system_state.energy.get('E', 0.0)
        if energy > self.alert_thresholds['high_energy']:
            health_report['warnings'].append('High energy level detected - possible overload')
            health_report['recommendations'].append('Consider increasing leap threshold or processing capacity')
        elif energy < self.alert_thresholds['low_energy']:
            health_report['warnings'].append('Low energy level - system may be inactive')
        
        # 温度チェック
        temperature = system_state.energy.get('T', 1.0)
        if temperature > self.alert_thresholds['high_temperature']:
            health_report['warnings'].append('High exploration temperature - system may be too random')
        
        # メモリ使用量チェック
        total_memory = sum(system_state.memory_usage.values())
        if total_memory > self.alert_thresholds['memory_usage']:
            health_report['warnings'].append('High memory usage detected')
            health_report['recommendations'].append('Run system maintenance to cleanup caches')
        
        # 構造バランスチェック
        structure_stats = system_state.structure.get('layer_stats', {})
        layer_counts = [stats.get('element_count', 0) for stats in structure_stats.values()]
        if layer_counts and max(layer_counts) - min(layer_counts) > 10:
            health_report['warnings'].append('Structural imbalance detected across layers')
        
        # ステータス決定
        if health_report['errors']:
            health_report['status'] = 'critical'
        elif len(health_report['warnings']) > 2:
            health_report['status'] = 'warning'
        elif health_report['warnings']:
            health_report['status'] = 'caution'
        
        return health_report
    
    def generate_performance_report(self, layers: Dict[LayerType, Dict[str, StructuralState]], 
                                  decision_history: List[Dict], global_kappa: Dict[str, float]) -> Dict[str, Any]:
        """パフォーマンスレポート生成"""
        report = {
            'cognitive_metrics': {},
            'learning_metrics': {},
            'structure_metrics': {},
            'efficiency_metrics': {}
        }
        
        # 認知負荷計算
        cognitive_load = 0.0
        layer_mobility = {
            LayerType.PHYSICAL: 0.1,
            LayerType.BASE: 0.3,
            LayerType.CORE: 0.6,
            LayerType.UPPER: 0.9
        }
        
        for layer in LayerType:
            if layer in layers and layers[layer]:
                layer_load = np.mean([state.activation * len(state.connections) 
                                    for state in layers[layer].values()])
                cognitive_load += layer_load * layer_mobility[layer]
        
        report['cognitive_metrics']['cognitive_load'] = cognitive_load
        
        # 学習効率
        if global_kappa:
            kappa_variance = np.var(list(global_kappa.values()))
            kappa_mean = np.mean(list(global_kappa.values()))
            report['learning_metrics'] = {
                'kappa_diversity': kappa_variance,
                'avg_learning_strength': kappa_mean,
                'learned_patterns': len(global_kappa)
            }
        
        # 意思決定効率
        if decision_history:
            recent_decisions = decision_history[-20:] if len(decision_history) > 20 else decision_history
            exploration_ratio = sum(1 for d in recent_decisions 
                                  if d.get('info', {}).get('exploration_mode', False)) / len(recent_decisions)
            report['efficiency_metrics']['exploration_ratio'] = exploration_ratio
        
        # 構造統計
        total_elements = sum(len(elements) for elements in layers.values())
        total_connections = sum(
            sum(len(state.connections) for state in elements.values())
            for elements in layers.values()
        )
        
        report['structure_metrics'] = {
            'total_elements': total_elements,
            'total_connections': total_connections,
            'avg_connections_per_element': total_connections / total_elements if total_elements > 0 else 0
        }
        
        return report


class MaintenanceManager:
    """システムメンテナンス管理"""
    
    def __init__(self):
        self.maintenance_schedule = {}
        self.last_cleanup = 0
        
    def should_perform_maintenance(self, current_time: int, force: bool = False) -> Dict[str, bool]:
        """メンテナンス必要性判定"""
        maintenance_needed = {
            'cache_cleanup': False,
            'memory_optimization': False,
            'structure_stabilization': False,
            'full_maintenance': False
        }
        
        # 定期メンテナンス（100ステップごと）
        if force or current_time - self.last_cleanup > 100:
            maintenance_needed['cache_cleanup'] = True
            maintenance_needed['memory_optimization'] = True
            maintenance_needed['full_maintenance'] = True
            
        # 構造安定化（50ステップごと）
        elif current_time % 50 == 0:
            maintenance_needed['structure_stabilization'] = True
            
        # キャッシュクリーンアップ（20ステップごと）
        elif current_time % 20 == 0:
            maintenance_needed['cache_cleanup'] = True
        
        return maintenance_needed
    
    def execute_maintenance(self, system_components: Dict[str, Any], current_time: int) -> Dict[str, Any]:
        """メンテナンス実行"""
        maintenance_report = {
            'actions_taken': [],
            'memory_freed': 0,
            'caches_cleaned': 0,
            'structures_optimized': 0
        }
        
        # 各コンポーネントのメンテナンス
        for component_name, component in system_components.items():
            if hasattr(component, 'cleanup_cache'):
                component.cleanup_cache()
                maintenance_report['caches_cleaned'] += 1
                maintenance_report['actions_taken'].append(f'Cleaned {component_name} cache')
        
        self.last_cleanup = current_time
        return maintenance_report