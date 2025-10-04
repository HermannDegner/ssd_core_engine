"""
SSD Decision and Action System
構造主観力学 - 意思決定・行動システム
"""

import random
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from collections import deque

try:
    from .ssd_types import LayerType, StructuralState, DecisionInfo, ObjectInfo
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from ssd_types import LayerType, StructuralState, DecisionInfo, ObjectInfo


class DecisionSystem:
    """意思決定システム"""
    
    def __init__(self, layer_mobility: Dict[LayerType, float]):
        self.layer_mobility = layer_mobility
        self.T = 1.0  # 探索温度
        self.decision_history = deque(maxlen=100)
        
    def make_decision(self, available_actions: List[str], layers: Dict[LayerType, Dict[str, StructuralState]], 
                     global_kappa: Dict[str, float], perceived_objects: Dict[str, ObjectInfo], 
                     current_E: float) -> Tuple[str, DecisionInfo]:
        """意思決定の実行"""
        if not available_actions:
            return None, DecisionInfo(chosen_action="", scores={})
        
        # 各行動の評価
        action_scores = {}
        
        for action in available_actions:
            score = self._evaluate_action(action, layers, global_kappa, perceived_objects)
            action_scores[action] = score
        
        # 最高スコアの行動を選択（探索ノイズ付き）
        exploration_mode = random.random() < self.T * 0.5
        if exploration_mode:  # 探索
            chosen_action = random.choice(available_actions)
        else:  # 活用
            chosen_action = max(action_scores, key=action_scores.get)
        
        decision_info = DecisionInfo(
            chosen_action=chosen_action,
            scores=action_scores,
            exploration_mode=exploration_mode,
            E_level=current_E,
            T_level=self.T
        )
        
        # 決定履歴に追加
        self.decision_history.append({
            'action': chosen_action,
            'info': decision_info,
            'timestamp': len(self.decision_history)
        })
        
        return chosen_action, decision_info
    
    def _evaluate_action(self, action: str, layers: Dict[LayerType, Dict[str, StructuralState]], 
                        global_kappa: Dict[str, float], perceived_objects: Dict[str, ObjectInfo]) -> float:
        """行動の評価（基層的色付け統合）"""
        base_score = 0.5
        
        # 整合慣性による評価
        kappa_bonus = global_kappa.get(action, 0.1) * 0.4
        
        # 基層的色付け：生存関連行動の評価強化
        survival_bonus = 0.0
        survival_actions = {
            'eat': 1.0,           # 最高優先度
            'drink': 1.0,         # 最高優先度  
            'seek_shelter': 0.9,  # 高優先度
            'craft': 0.7,         # 中-高優先度（道具作成）
            'gather': 0.6,        # 中優先度（資源収集）
            'explore': 0.4,       # 中優先度（新資源発見）
            'rest': 0.5,          # 中優先度（体力回復）
            'store': 0.5,         # 中優先度（備蓄）
            'observe': 0.3,       # 低-中優先度（情報収集）
            'approach': 0.4,      # 中優先度
            'avoid': 0.6,         # 中-高優先度（安全）
            'investigate': 0.3,   # 低-中優先度
            'use': 0.5            # 中優先度
        }
        
        action_survival_value = survival_actions.get(action, 0.2)
        
        # 現在の生存緊急度を考慮
        current_survival_need = 0.0
        if perceived_objects:
            # 高い生存関連度のオブジェクトが多いほど緊急度が高い
            high_survival_objects = [obj for obj in perceived_objects.values() if obj.survival_relevance > 0.7]
            current_survival_need = len(high_survival_objects) / len(perceived_objects)
        
        survival_bonus = action_survival_value * current_survival_need * 0.8  # 最大80%ボーナス
        
        # 各層での評価（基層的重み付き）
        layer_evaluation = 0.0
        for layer in LayerType:
            layer_weight = self.layer_mobility[layer]
            survival_weight = layer.get_survival_weight()
            
            # 層の活性度に基づく評価
            layer_activation = np.mean([
                state.activation for state in layers.get(layer, {}).values()
            ]) if layers.get(layer, {}) else 0.0
            
            # 基層的色付け：生存関連層は重み強化
            enhanced_weight = layer_weight * (1.0 + survival_weight * current_survival_need)
            layer_evaluation += layer_activation * enhanced_weight * 0.2
        
        total_score = base_score + kappa_bonus + survival_bonus + layer_evaluation
        return min(total_score, 2.0)  # 上限設定
    
    def update_temperature(self, current_E: float):
        """探索温度の更新"""
        # 未処理圧が高いほど探索的になる
        base_temp = 0.3
        pressure_influence = min(1.0, current_E / 5.0) * 0.7
        
        self.T = base_temp + pressure_influence
    
    def get_decision_statistics(self) -> Dict[str, float]:
        """意思決定統計の取得"""
        if not self.decision_history:
            return {'exploration_ratio': 0.5, 'decision_count': 0}
        
        recent_decisions = list(self.decision_history)[-10:]
        exploration_count = sum(1 for d in recent_decisions if d['info'].exploration_mode)
        
        return {
            'exploration_ratio': exploration_count / len(recent_decisions) if recent_decisions else 0.5,
            'decision_count': len(self.decision_history),
            'current_temperature': self.T
        }


class ActionEvaluator:
    """行動評価システム"""
    
    def __init__(self):
        self.action_history = deque(maxlen=200)
        self.success_rates = {}
        
    def record_action_result(self, action: str, success: bool, context: Dict[str, Any] = None):
        """行動結果の記録"""
        self.action_history.append({
            'action': action,
            'success': success,
            'context': context or {},
            'timestamp': len(self.action_history)
        })
        
        # 成功率の更新
        if action not in self.success_rates:
            self.success_rates[action] = {'successes': 0, 'attempts': 0}
        
        self.success_rates[action]['attempts'] += 1
        if success:
            self.success_rates[action]['successes'] += 1
    
    def get_action_success_rate(self, action: str) -> float:
        """行動の成功率取得"""
        if action not in self.success_rates or self.success_rates[action]['attempts'] == 0:
            return 0.5  # デフォルト値
        
        stats = self.success_rates[action]
        return stats['successes'] / stats['attempts']
    
    def suggest_best_actions(self, available_actions: List[str], top_k: int = 3) -> List[str]:
        """最適行動の提案"""
        action_scores = []
        
        for action in available_actions:
            success_rate = self.get_action_success_rate(action)
            attempt_count = self.success_rates.get(action, {}).get('attempts', 0)
            
            # 成功率と経験値を組み合わせたスコア
            confidence_bonus = min(attempt_count / 10.0, 1.0)  # 経験による信頼度
            score = success_rate * (0.7 + 0.3 * confidence_bonus)
            
            action_scores.append((action, score))
        
        # スコアでソートして上位k個を返す
        action_scores.sort(key=lambda x: x[1], reverse=True)
        return [action for action, _ in action_scores[:top_k]]