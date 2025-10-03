"""
SSD Alignment and Leap System
構造主観力学 - 整合・跳躍システム
"""

import math
import random
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict, deque
from .ssd_types import LayerType, StructuralState, AlignmentResult, LeapResult, ObjectInfo


class AlignmentProcessor:
    """整合処理システム"""
    
    def __init__(self, layer_mobility: Dict[LayerType, float]):
        self.layer_mobility = layer_mobility
        self.global_kappa = defaultdict(lambda: 0.1)  # グローバル整合慣性
        
    def process_alignment_step(self, layers: Dict[LayerType, Dict[str, StructuralState]], 
                              current_E: float) -> AlignmentResult:
        """整合ステップの実行"""
        result = AlignmentResult()
        
        # 各層で整合処理
        for layer in LayerType:
            if layer in layers:
                layer_result = self._process_layer_alignment(layer, layers[layer], current_E)
                result.alignment_flows[layer.value] = layer_result
        
        # グローバル整合慣性の更新
        self._update_global_kappa()
        
        return result
    
    def _process_layer_alignment(self, layer: LayerType, layer_elements: Dict[str, StructuralState], 
                               current_E: float) -> Dict[str, float]:
        """特定層での整合処理"""
        alignment_flows = {}
        
        for element_id, state in layer_elements.items():
            # 整合流の計算: j = (G0 + g * κ) * p
            G0 = 0.5  # 基礎通りやすさ
            g = 0.7   # 慣性利得係数
            
            if element_id in state.kappa:
                kappa_val = state.kappa[element_id]
            else:
                kappa_val = self.global_kappa[element_id]
                
            # 現在の意味圧（簡略化）
            current_pressure = current_E * self.layer_mobility[layer]
            
            # 整合流
            alignment_flow = (G0 + g * kappa_val) * current_pressure
            alignment_flows[element_id] = alignment_flow
            
            # 活性度更新
            state.activation = min(1.0, state.activation + alignment_flow * 0.1)
        
        return alignment_flows
    
    def process_alignment_step_with_heat_loss(self, layers: Dict[LayerType, Dict[str, StructuralState]], current_E: float) -> Dict[str, float]:
        """熱損失を考慮した整合ステップ"""
        alignment_work = {}
        
        # 抵抗係数（層ごとの異なる粘性）
        layer_resistance = {
            LayerType.PHYSICAL: 0.1,  # 物理層：低抵抗
            LayerType.BASE: 0.3,      # 基層：中抵抗
            LayerType.CORE: 0.5,      # 中核層：高抵抗
            LayerType.UPPER: 0.2      # 上層：低-中抵抗（流動的）
        }
        
        for layer, elements in layers.items():
            rho = layer_resistance.get(layer, 0.3)  # 層特有の抵抗係数
            layer_mobility = self.layer_mobility.get(layer, 1.0)
            
            for elem_id, state in elements.items():
                # 整合流れの計算: j = (G0 + g * κ) * p
                kappa = self.global_kappa.get(elem_id, 0.1)
                G0 = 0.2 * layer_mobility  # 基本整合係数
                g = 0.3   # 慣性結合係数
                
                # 圧力は活性度と安定度の組み合わせで計算
                pressure = state.activation * (2.0 - state.stability)  # 不安定な要素ほど高圧力
                j = (G0 + g * kappa) * pressure
                
                # 整合仕事の計算: W = p·j - ρj²
                # 第一項：圧力による仕事、第二項：粘性による熱損失
                work = pressure * j - rho * (j ** 2)
                alignment_work[f"{layer.name}_{elem_id}"] = work
                
                # エネルギー保存の更新
                heat_loss = rho * (j ** 2)
                self.total_heat_loss = getattr(self, 'total_heat_loss', 0.0) + heat_loss
        
        return alignment_work
    
    def get_alignment_statistics(self) -> Dict[str, float]:
        """整合統計の取得（熱損失含む）"""
        return {
            'avg_inertia': np.mean(list(self.global_kappa.values())) if self.global_kappa else 0.0,
            'total_heat_loss': getattr(self, 'total_heat_loss', 0.0),
            'active_elements': len(self.global_kappa),
            'thermal_efficiency': 1.0 - min(getattr(self, 'total_heat_loss', 0.0) / max(1.0, sum(self.global_kappa.values())), 0.95)
        }
    
    def _update_global_kappa(self):
        """グローバル整合慣性の更新"""
        # 基本的な慣性更新ロジック
        for key in list(self.global_kappa.keys()):
            # 緩やかな減衰
            self.global_kappa[key] *= 0.995
            
            # 最小値を維持
            if self.global_kappa[key] < 0.05:
                self.global_kappa[key] = 0.05
    
    def calculate_enhanced_alignment_inertia(self, layers: Dict[LayerType, Dict[str, StructuralState]], 
                                           context_objects: List[ObjectInfo] = None) -> float:
        """基層的色付けを統合した整合慣性計算"""
        if context_objects is None:
            context_objects = []
        
        # 各層での整合慣性を計算
        layer_kappas = {}
        total_survival_weight = 0.0
        
        for layer in LayerType:
            layer_elements = layers.get(layer, {})
            survival_weight = layer.get_survival_weight()
            
            if layer_elements:
                # 層内の構造要素から慣性を計算
                layer_kappa = 0.0
                for element_id, state in layer_elements.items():
                    # 基本慣性
                    base_kappa = state.stability * state.activation
                    
                    # 生存関連オブジェクトとの関連性チェック
                    survival_relevance = 0.0
                    for obj in context_objects:
                        if obj.survival_relevance > 0.5:  # 高い生存関連度
                            # オブジェクトとの類似性を計算（簡略版）
                            similarity = random.uniform(0.3, 0.8)  # プレースホルダー
                            survival_relevance += obj.survival_relevance * similarity
                    
                    # 基層的色付け適用
                    enhanced_kappa = base_kappa * (1.0 + survival_relevance * survival_weight)
                    layer_kappa += enhanced_kappa
                
                layer_kappas[layer] = layer_kappa / len(layer_elements) if layer_elements else 0.0
            else:
                layer_kappas[layer] = 0.0
            
            total_survival_weight += survival_weight
        
        # 全体の整合慣性を生存重み付きで統合
        if total_survival_weight > 0:
            weighted_kappa = sum(layer_kappas[layer] * layer.get_survival_weight() 
                               for layer in LayerType) / total_survival_weight
        else:
            weighted_kappa = sum(layer_kappas.values()) / len(LayerType)
        
        return min(weighted_kappa, 5.0)  # 上限設定


class LeapProcessor:
    """跳躍処理システム"""
    
    def __init__(self, layer_mobility: Dict[LayerType, float]):
        self.layer_mobility = layer_mobility
        # 跳躍パラメータ
        self.theta_base = 0.8  # 基本跳躍閾値
        self.h0 = 0.1         # 基本跳躍強度
        self.gamma = 0.5      # 跳躍曲線の鋭さ
        
        # 二段階反応システムの統合
        self.reaction_system = TwoStageReactionSystem()
        
    def check_leap_condition(self, current_E: float, global_kappa: Dict[str, float], 
                           perceived_objects: Dict[str, ObjectInfo]) -> bool:
        """跳躍条件をチェック（数学的精密化版）"""
        # 整合慣性の統計的計算
        kappa_values = list(global_kappa.values()) if global_kappa else [0.1]
        mean_kappa = np.mean(kappa_values)
        std_kappa = np.std(kappa_values) if len(kappa_values) > 1 else 0.05
        
        # 基層的色付け：生存関連の圧力は閾値を下げる（跳躍しやすくする）
        survival_urgency = 0.0
        if perceived_objects:
            survival_relevances = [obj.survival_relevance for obj in perceived_objects.values()]
            survival_urgency = np.mean(survival_relevances)
        
        # 数学的精密化：動的閾値計算
        # θ(t) = θ_base * (1 + κ_mean ± σ_κ) * (1 - α * S)
        # S: 生存緊急度, α: 生存感度係数
        alpha = 0.6  # 生存感度係数
        kappa_fluctuation = mean_kappa + random.uniform(-std_kappa, std_kappa) * 0.5
        survival_modifier = 1.0 - (alpha * survival_urgency)
        
        threshold = self.theta_base * (1 + kappa_fluctuation) * max(0.2, survival_modifier)
        
        # 跳躍確率の精密計算
        if current_E > threshold:
            # P_leap = h0 * exp((E - θ) / γ) * (1 + β * S)
            # β: 生存ブースト係数
            beta = 2.5  # 生存ブースト係数
            survival_boost = 1.0 + (beta * survival_urgency)
            
            # シグモイド関数で確率を正規化
            raw_prob = self.h0 * math.exp((current_E - threshold) / self.gamma) * survival_boost
            normalized_prob = 2.0 / (1.0 + math.exp(-raw_prob)) - 1.0  # タンジェント双曲線
            
            return random.random() < min(max(normalized_prob, 0.05), 0.95)  # 5-95%範囲
        
        return False
    
    def execute_leap(self, layers: Dict[LayerType, Dict[str, StructuralState]], 
                    perceived_objects: Dict[str, ObjectInfo], current_E: float) -> Tuple[LeapResult, float]:
        """跳躍の実行（基層的優先度統合）"""
        leap_result = LeapResult()
        
        # 生存関連度をチェック
        survival_urgency = 0.0
        if perceived_objects:
            survival_urgency = sum(obj.survival_relevance for obj in perceived_objects.values()) / len(perceived_objects)
        
        # 基層的色付け：生存緊急度が高い場合は下位層から跳躍
        if survival_urgency > 0.6:
            # 生存関連は基層から跳躍（PHYSICAL → BASE → CORE順）
            leap_order = [LayerType.PHYSICAL, LayerType.BASE, LayerType.CORE, LayerType.UPPER]
            leap_result.leap_type = 'survival_driven_leap'
            leap_result.survival_driven = True
        else:
            # 通常は上位層から跳躍
            leap_order = [LayerType.UPPER, LayerType.CORE, LayerType.BASE]
            leap_result.leap_type = 'alignment_reorganization'
        
        # 指定順序で跳躍を試行
        for layer in leap_order:
            survival_weight = layer.get_survival_weight()
            enhanced_success = survival_urgency * survival_weight
            
            if self._attempt_layer_leap(layer, enhanced_success, layers.get(layer, {})):
                leap_result.affected_layers.append(layer.value)
                
                # 生存関連は複数層に影響しやすい
                if leap_result.survival_driven and len(leap_result.affected_layers) < 2:
                    continue  # 次の層も試行
                else:
                    break
        
        # 未処理圧をリセット（生存関連はより多く消費）
        pressure_reduction = 0.3 + (survival_urgency * 0.4)  # 最大70%減少
        new_E = max(0.0, current_E * (1.0 - pressure_reduction))
        
        return leap_result, new_E
    
    def _attempt_layer_leap(self, layer: LayerType, survival_enhancement: float, 
                          layer_elements: Dict[str, StructuralState]) -> bool:
        """特定層での跳躍試行（基層的色付け対応）"""
        base_mobility = self.layer_mobility[layer]
        
        # 基層的色付け：生存関連は下位層の跳躍を促進
        survival_weight = layer.get_survival_weight()
        enhanced_mobility = base_mobility + (survival_enhancement * survival_weight * 0.5)
        
        # モビリティが高い層ほど跳躍しやすい
        if random.random() < min(enhanced_mobility, 0.95):
            # 新しい接続や要素の創発
            self._create_emergent_connection(layer_elements)
            return True
        
        return False
    
    def _create_emergent_connection(self, layer_elements: Dict[str, StructuralState]):
        """創発的接続の生成"""
        element_ids = list(layer_elements.keys())
        
        if len(element_ids) >= 2:
            # ランダムに2つの要素を接続
            elem1, elem2 = random.sample(element_ids, 2)
            
            # 新しい接続強度
            connection_strength = random.uniform(0.3, 0.8)
            
            # 双方向接続を作成
            layer_elements[elem1].connections[elem2] = connection_strength
            layer_elements[elem2].connections[elem1] = connection_strength
    
    def process_stimulus_reaction(self, stimulus: Dict[str, Any], current_time: float) -> Dict[str, Any]:
        """刺激に対する二段階反応処理"""
        return self.reaction_system.process_reaction(stimulus, current_time)
    
    def update_conscious_processing(self, current_time: float, layers: Dict[LayerType, Dict[str, StructuralState]]) -> List[Dict[str, Any]]:
        """意識的処理の更新"""
        return self.reaction_system.process_conscious_reactions(current_time, layers)


# ===== 数理モデルの完全性向上：新機能 =====

class TwoStageReactionSystem:
    """反応の二段階モデル"""
    
    def __init__(self):
        self.unconscious_response_time = 0.05  # 50ms
        self.conscious_processing_time = 0.35  # 350ms
        self.pending_reactions = deque(maxlen=100)
        
        # 基層反応の重み（生存関連）
        self.base_response_weights = {
            'threat': 0.95,     # 脅威：即座の反応
            'food': 0.8,        # 食物：強い反応
            'water': 0.85,      # 水：強い反応
            'shelter': 0.7,     # 避難所：中程度
            'social': 0.6,      # 社会的：中程度
            'tool': 0.4,        # 道具：低-中程度
            'abstract': 0.2     # 抽象的：低反応
        }
    
    def process_reaction(self, stimulus: Dict[str, Any], current_time: float) -> Dict[str, Any]:
        """二段階反応処理"""
        # 第1段階：無意識的即時反応（基層）
        unconscious = self._immediate_base_layer_response(stimulus, current_time)
        
        # 第2段階：意識的再処理（中核・上層）を予約
        self.pending_reactions.append({
            'stimulus': stimulus,
            'unconscious': unconscious,
            'process_at': current_time + self.conscious_processing_time,
            'timestamp': current_time
        })
        
        return unconscious
    
    def _immediate_base_layer_response(self, stimulus: Dict[str, Any], current_time: float) -> Dict[str, Any]:
        """即座の基層反応"""
        stimulus_type = stimulus.get('type', 'abstract')
        intensity = stimulus.get('intensity', 0.5)
        
        # 生存関連度による反応強度
        base_weight = self.base_response_weights.get(stimulus_type, 0.3)
        response_strength = base_weight * intensity
        
        # 基層的判定（fight/flight/freeze）
        if stimulus_type == 'threat' and response_strength > 0.7:
            action = 'flee' if intensity > 0.8 else 'freeze'
        elif stimulus_type in ['food', 'water'] and response_strength > 0.6:
            action = 'approach'
        else:
            action = 'observe'
        
        return {
            'action': action,
            'strength': response_strength,
            'reaction_time': self.unconscious_response_time,
            'layer': 'BASE',
            'confidence': base_weight,
            'timestamp': current_time
        }
    
    def process_conscious_reactions(self, current_time: float, layers: Dict[LayerType, Dict[str, StructuralState]]) -> List[Dict[str, Any]]:
        """意識的再処理の実行"""
        processed = []
        remaining = deque()
        
        # 処理時刻に達した反応を処理
        while self.pending_reactions:
            reaction = self.pending_reactions.popleft()
            
            if current_time >= reaction['process_at']:
                # 中核・上層による再評価
                conscious_response = self._conscious_reprocessing(
                    reaction['stimulus'], 
                    reaction['unconscious'],
                    layers
                )
                processed.append(conscious_response)
            else:
                remaining.append(reaction)
        
        # 未処理の反応を戻す
        self.pending_reactions = remaining
        return processed
    
    def _conscious_reprocessing(self, stimulus: Dict[str, Any], unconscious: Dict[str, Any], 
                              layers: Dict[LayerType, Dict[str, StructuralState]]) -> Dict[str, Any]:
        """意識的再処理（中核・上層）"""
        # 中核層による社会的適正性チェック
        core_adjustment = self._core_layer_adjustment(stimulus, unconscious)
        
        # 上層による価値的・理念的評価
        upper_evaluation = self._upper_layer_evaluation(stimulus, unconscious)
        
        # 統合的判断
        final_action = self._integrate_multi_layer_response(
            unconscious, core_adjustment, upper_evaluation
        )
        
        return {
            'final_action': final_action,
            'unconscious_response': unconscious,
            'core_adjustment': core_adjustment,
            'upper_evaluation': upper_evaluation,
            'processing_time': self.conscious_processing_time,
            'integration_confidence': (core_adjustment['confidence'] + upper_evaluation['confidence']) / 2
        }
    
    def _core_layer_adjustment(self, stimulus: Dict[str, Any], unconscious: Dict[str, Any]) -> Dict[str, Any]:
        """中核層による調整（社会的適正性）"""
        social_appropriateness = 0.7  # 社会的適正度
        
        # 基層反応が社会的に不適切な場合の抑制
        if unconscious['action'] == 'flee' and stimulus.get('social_context', False):
            return {
                'action': 'controlled_withdrawal',
                'confidence': 0.8,
                'suppression_factor': 0.6
            }
        elif unconscious['action'] == 'approach' and stimulus.get('danger_level', 0) > 0.3:
            return {
                'action': 'cautious_approach', 
                'confidence': 0.7,
                'suppression_factor': 0.4
            }
        
        return {
            'action': unconscious['action'],
            'confidence': social_appropriateness,
            'suppression_factor': 0.1
        }
    
    def _upper_layer_evaluation(self, stimulus: Dict[str, Any], unconscious: Dict[str, Any]) -> Dict[str, Any]:
        """上層による価値評価"""
        value_alignment = stimulus.get('value_alignment', 0.5)
        long_term_benefit = stimulus.get('long_term_benefit', 0.5)
        
        # 理念的評価
        if value_alignment > 0.8:
            recommendation = 'enhance'
        elif value_alignment < 0.3:
            recommendation = 'suppress'
        else:
            recommendation = 'neutral'
        
        return {
            'recommendation': recommendation,
            'value_score': value_alignment,
            'long_term_score': long_term_benefit,
            'confidence': (value_alignment + long_term_benefit) / 2
        }
    
    def _integrate_multi_layer_response(self, unconscious: Dict[str, Any], 
                                       core: Dict[str, Any], 
                                       upper: Dict[str, Any]) -> str:
        """多層統合判断"""
        base_strength = unconscious['strength']
        core_suppression = core['suppression_factor']
        upper_modifier = 1.0 if upper['recommendation'] == 'enhance' else \
                        0.5 if upper['recommendation'] == 'suppress' else 0.8
        
        # 最終強度計算
        final_strength = base_strength * (1 - core_suppression) * upper_modifier
        
        # 閾値による最終行動決定
        if final_strength > 0.7:
            return unconscious['action']
        elif final_strength > 0.4:
            return core['action']
        else:
            return 'deliberate'