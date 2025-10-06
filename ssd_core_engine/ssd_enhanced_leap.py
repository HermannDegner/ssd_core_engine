"""
SSD Enhanced Leap System
構造主観力学 - 跳躍システム（真の非線形性実装）

Hermann Degnerの理論に基づく真のカオス的跳躍メカニズム
"""

import numpy as np
import random
import math
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

try:
    from .ssd_types import LayerType, StructuralState
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from ssd_types import LayerType, StructuralState


class LeapType(Enum):
    """跳躍の種類"""
    CREATIVE = "creative"        # 創造的跳躍
    DESTRUCTIVE = "destructive"  # 破壊的跳躍
    TRANSFORMATIVE = "transformative"  # 変容的跳躍
    EMERGENT = "emergent"       # 創発的跳躍


@dataclass
class LeapEvent:
    """跳躍イベントの記録"""
    leap_type: LeapType
    magnitude: float
    source_layer: LayerType
    target_layer: LayerType
    chaos_factor: float
    predictability: float  # 0.0 = 完全予測不可能, 1.0 = 完全予測可能
    energy_release: float
    structural_transformation: Dict[str, float]
    timestamp: int


class ChaoticLeapProcessor:
    """
    真のカオス的跳躍処理システム
    
    Hermann Degner理論の核心：
    「跳躍は整合の限界を超えた時に発生する、非連続的で予測困難な構造変化」
    """
    
    def __init__(self):
        self.leap_history: List[LeapEvent] = []
        self.chaos_seed = random.random()
        self.lyapunov_exponent = 0.3  # カオスの度合い
        self.strange_attractor_state = np.array([0.1, 0.1, 0.1])
        self.time_step = 0
        
    def calculate_leap_probability(self, meaning_pressure: float, 
                                 alignment_resistance: float,
                                 layer: LayerType) -> Tuple[float, float]:
        """
        真の非線形カオス的跳躍確率計算
        
        理論的基盤：
        - 意味圧が整合抵抗を超えた時の相転移現象
        - アトラクタの不安定周期軌道近傍での鋭敏性
        - 蝶々効果による予測不可能性
        """
        # 1. 基本的な跳躍条件
        pressure_threshold = alignment_resistance * 1.2
        basic_leap_condition = meaning_pressure > pressure_threshold
        
        if not basic_leap_condition:
            return 0.0, 1.0  # 跳躍なし、完全予測可能
        
        # 2. カオス力学系による予測困難性生成
        self._update_strange_attractor()
        
        # 3. ローレンツ方程式風の非線形結合
        # dx/dt = σ(y-x), dy/dt = x(ρ-z)-y, dz/dt = xy-βz
        x, y, z = self.strange_attractor_state
        sigma, rho, beta = 10.0, 28.0, 8.0/3.0
        
        chaos_x = meaning_pressure / 10.0
        chaos_y = alignment_resistance / 10.0
        
        # 4. 非線形相互作用項
        nonlinear_coupling = (
            np.sin(chaos_x * np.pi) * np.exp(-chaos_y) +
            np.cos(chaos_y * np.pi) * np.tanh(chaos_x) +
            x * y * z / 10.0
        )
        
        # 5. 層別の跳躍感受性
        layer_sensitivity = self._get_layer_leap_sensitivity(layer)
        
        # 6. 真のカオス的跳躍確率
        chaos_factor = abs(nonlinear_coupling) * layer_sensitivity
        leap_probability = min(1.0, chaos_factor * random.uniform(0.3, 1.7))
        
        # 7. 予測困難性の計算（リアプノフ指数ベース）
        unpredictability = 1.0 - math.exp(-self.lyapunov_exponent * chaos_factor)
        
        return leap_probability, unpredictability
    
    def _update_strange_attractor(self):
        """ストレンジアトラクタ状態の更新"""
        x, y, z = self.strange_attractor_state
        dt = 0.01
        
        # ローレンツアトラクタの時間発展
        sigma, rho, beta = 10.0, 28.0, 8.0/3.0
        dx = sigma * (y - x) * dt
        dy = (x * (rho - z) - y) * dt
        dz = (x * y - beta * z) * dt
        
        self.strange_attractor_state += np.array([dx, dy, dz])
        
        # 意味圧による外部擾乱
        perturbation = np.random.normal(0, 0.01, 3)
        self.strange_attractor_state += perturbation
        
        self.time_step += 1
    
    def _get_layer_leap_sensitivity(self, layer: LayerType) -> float:
        """層別跳躍感受性"""
        sensitivities = {
            LayerType.PHYSICAL: 0.1,   # 物理層は最も安定
            LayerType.BASE: 0.4,       # 基層は中程度
            LayerType.CORE: 0.7,       # 中核層は変化しやすい
            LayerType.UPPER: 0.9       # 上層は最も流動的
        }
        return sensitivities.get(layer, 0.5)
    
    def execute_leap(self, meaning_pressure: float, alignment_state: float, 
                    layer: LayerType, structural_states: Dict[str, StructuralState]) -> Optional[LeapEvent]:
        """
        跳躍の実行
        
        真の非連続性：段階的変化ではなく瞬間的な構造転換
        """
        leap_prob, unpredictability = self.calculate_leap_probability(
            meaning_pressure, alignment_state, layer
        )
        
        if random.random() > leap_prob:
            return None  # 跳躍発生せず
        
        # 跳躍タイプの決定（カオス的）
        chaos_state = abs(self.strange_attractor_state[0])
        if chaos_state < 5:
            leap_type = LeapType.CREATIVE
        elif chaos_state < 10:
            leap_type = LeapType.TRANSFORMATIVE
        elif chaos_state < 15:
            leap_type = LeapType.EMERGENT
        else:
            leap_type = LeapType.DESTRUCTIVE
        
        # 跳躍の強度計算
        magnitude = min(10.0, meaning_pressure * unpredictability * random.uniform(0.5, 2.0))
        
        # エネルギー放出（非可逆的変化）
        energy_release = magnitude * magnitude * 0.1
        
        # 構造的変容の計算
        structural_transformation = {}
        for state_id, state in structural_states.items():
            if state.layer == layer:
                # 非線形変容
                transformation = np.sin(magnitude * np.pi / 4) * random.uniform(-1.0, 1.0)
                structural_transformation[state_id] = transformation
        
        # 跳躍先レイヤーの決定（時には層間跳躍も）
        target_layer = layer
        if random.random() < 0.3:  # 30%の確率で層間跳躍
            layers = list(LayerType)
            target_layer = random.choice(layers)
        
        # 跳躍イベントの記録
        leap_event = LeapEvent(
            leap_type=leap_type,
            magnitude=magnitude,
            source_layer=layer,
            target_layer=target_layer,
            chaos_factor=chaos_state,
            predictability=1.0 - unpredictability,
            energy_release=energy_release,
            structural_transformation=structural_transformation,
            timestamp=self.time_step
        )
        
        self.leap_history.append(leap_event)
        
        # 跳躍後のカオス状態更新
        self.chaos_seed = random.random()
        self.strange_attractor_state *= (1.0 + random.uniform(-0.5, 0.5))
        
        return leap_event
    
    def analyze_leap_patterns(self) -> Dict[str, float]:
        """跳躍パターンの分析（メタ認知）"""
        if not self.leap_history:
            return {"no_data": 1.0}
        
        recent_leaps = self.leap_history[-10:]  # 直近10回
        
        # 跳躍頻度分析
        creative_ratio = len([l for l in recent_leaps if l.leap_type == LeapType.CREATIVE]) / len(recent_leaps)
        destructive_ratio = len([l for l in recent_leaps if l.leap_type == LeapType.DESTRUCTIVE]) / len(recent_leaps)
        
        # 平均予測困難性
        avg_unpredictability = np.mean([1.0 - l.predictability for l in recent_leaps])
        
        # カオス度合い
        chaos_intensity = np.std([l.chaos_factor for l in recent_leaps])
        
        return {
            "creative_tendency": creative_ratio,
            "destructive_tendency": destructive_ratio,
            "unpredictability": avg_unpredictability,
            "chaos_intensity": chaos_intensity,
            "leap_frequency": len(recent_leaps) / 10.0
        }
    
    def get_system_state(self) -> Dict[str, any]:
        """システム状態の取得"""
        return {
            "attractor_state": self.strange_attractor_state.tolist(),
            "lyapunov_exponent": self.lyapunov_exponent,
            "chaos_seed": self.chaos_seed,
            "total_leaps": len(self.leap_history),
            "time_step": self.time_step
        }


class StructuralTheoria:
    """
    構造観照（テオーリア）実装
    
    Hermann Degner理論：
    「善悪や好悪の判断を保留し、事象を『構造と意味圧の相互作用』として冷静に分析する知的態度」
    """
    
    def __init__(self):
        self.judgment_suspension = True
        self.emotional_distance = True
        self.analytical_mode = True
        self.bias_monitoring = True
        
    def analyze_phenomenon_objectively(self, phenomenon_data: Dict) -> Dict[str, any]:
        """現象の客観的構造分析"""
        if not self.judgment_suspension:
            raise ValueError("構造観照モードが無効です。判断保留を有効にしてください。")
        
        # 1. 構造の抽出（価値判断なし）
        structures = self._extract_structures(phenomenon_data)
        
        # 2. 意味圧の識別
        meaning_pressures = self._identify_meaning_pressures(phenomenon_data)
        
        # 3. 相互作用の分析
        interactions = self._analyze_structure_pressure_interactions(structures, meaning_pressures)
        
        # 4. 動態パターンの認識
        dynamics = self._recognize_dynamic_patterns(interactions)
        
        return {
            "structures": structures,
            "meaning_pressures": meaning_pressures,
            "interactions": interactions,
            "dynamics": dynamics,
            "analysis_mode": "theoria",
            "bias_check": self._perform_bias_check()
        }
    
    def _extract_structures(self, data: Dict) -> List[Dict]:
        """構造の価値中立的抽出"""
        structures = []
        
        # 階層性の識別
        if "hierarchy" in data:
            structures.append({
                "type": "hierarchical",
                "layers": data["hierarchy"],
                "stability": "unknown"
            })
        
        # パターンの識別
        if "patterns" in data:
            structures.append({
                "type": "pattern",
                "repetition": data["patterns"],
                "coherence": "unknown"
            })
        
        return structures
    
    def _identify_meaning_pressures(self, data: Dict) -> List[Dict]:
        """意味圧の価値中立的識別"""
        pressures = []
        
        # エネルギー源の識別
        if "energy_sources" in data:
            for source in data["energy_sources"]:
                pressures.append({
                    "source": source,
                    "direction": "unknown",
                    "intensity": "unknown",
                    "evaluation": "suspended"  # 評価保留
                })
        
        return pressures
    
    def _analyze_structure_pressure_interactions(self, structures: List, pressures: List) -> Dict:
        """構造と意味圧の相互作用分析"""
        return {
            "alignment_attempts": len(structures) * len(pressures),
            "resistance_points": "to_be_observed",
            "transformation_potentials": "monitoring",
            "judgment": "suspended"
        }
    
    def _recognize_dynamic_patterns(self, interactions: Dict) -> Dict:
        """動態パターンの認識"""
        return {
            "stability_trends": "observing",
            "change_indicators": "monitoring",
            "leap_probabilities": "calculating",
            "prediction": "limited_by_chaos"
        }
    
    def _perform_bias_check(self) -> Dict:
        """バイアス検査"""
        return {
            "emotional_involvement": self.emotional_distance,
            "value_judgment": not self.judgment_suspension,
            "analytical_objectivity": self.analytical_mode,
            "observer_effect_awareness": True
        }


class NarrativeSphereDepthModel:
    """
    語り圏深度モデル実装
    
    Hermann Degner理論：
    「客観的事実(L1)」から「神(L5)」まで、実在性の異なる「語り」が社会にどう作用するか
    """
    
    class DepthLevel(Enum):
        L1_OBJECTIVE_FACTS = 1      # 客観的事実
        L2_SCIENTIFIC_INTERPRETATION = 2   # 科学的解釈  
        L3_SOCIAL_CONSENSUS = 3     # 社会的合意
        L4_PERSONAL_BELIEF = 4      # 個人的信念
        L5_ABSOLUTE_BEING = 5       # 神・絶対的存在
    
    def __init__(self):
        self.depth_mappings: Dict[int, List[str]] = {
            1: [],  # 事実レベル
            2: [],  # 解釈レベル
            3: [],  # 社会レベル
            4: [],  # 信念レベル
            5: []   # 絶対レベル
        }
        
    def classify_narrative_depth(self, narrative: str) -> Tuple[DepthLevel, float]:
        """語りの深度分類"""
        # 簡略版実装（実際はより高度な自然言語処理が必要）
        
        # L1: 数値データ、測定結果など
        if any(indicator in narrative.lower() for indicator in ["測定", "数値", "mm", "kg", "°c"]):
            return self.DepthLevel.L1_OBJECTIVE_FACTS, 0.9
        
        # L2: 科学的説明、理論など
        if any(indicator in narrative.lower() for indicator in ["理論", "法則", "実験", "証明"]):
            return self.DepthLevel.L2_SCIENTIFIC_INTERPRETATION, 0.8
        
        # L3: 社会的規範、常識など  
        if any(indicator in narrative.lower() for indicator in ["常識", "普通", "社会", "皆"]):
            return self.DepthLevel.L3_SOCIAL_CONSENSUS, 0.7
        
        # L4: 個人的価値観、信念など
        if any(indicator in narrative.lower() for indicator in ["思う", "信じる", "感じる", "私は"]):
            return self.DepthLevel.L4_PERSONAL_BELIEF, 0.6
        
        # L5: 絶対的・神的言及
        if any(indicator in narrative.lower() for indicator in ["神", "絶対", "永遠", "真理"]):
            return self.DepthLevel.L5_ABSOLUTE_BEING, 0.5
        
        # デフォルト
        return self.DepthLevel.L3_SOCIAL_CONSENSUS, 0.5
    
    def calculate_narrative_influence(self, narrative_depth: DepthLevel, 
                                   target_layer: LayerType) -> float:
        """語りの深度が四層構造に与える影響力計算"""
        
        # 深度と層の相互作用マトリックス
        influence_matrix = {
            (self.DepthLevel.L1_OBJECTIVE_FACTS, LayerType.PHYSICAL): 0.9,
            (self.DepthLevel.L1_OBJECTIVE_FACTS, LayerType.BASE): 0.6,
            (self.DepthLevel.L1_OBJECTIVE_FACTS, LayerType.CORE): 0.4,
            (self.DepthLevel.L1_OBJECTIVE_FACTS, LayerType.UPPER): 0.8,
            
            (self.DepthLevel.L2_SCIENTIFIC_INTERPRETATION, LayerType.PHYSICAL): 0.7,
            (self.DepthLevel.L2_SCIENTIFIC_INTERPRETATION, LayerType.BASE): 0.4,
            (self.DepthLevel.L2_SCIENTIFIC_INTERPRETATION, LayerType.CORE): 0.6,
            (self.DepthLevel.L2_SCIENTIFIC_INTERPRETATION, LayerType.UPPER): 0.9,
            
            (self.DepthLevel.L3_SOCIAL_CONSENSUS, LayerType.PHYSICAL): 0.2,
            (self.DepthLevel.L3_SOCIAL_CONSENSUS, LayerType.BASE): 0.8,
            (self.DepthLevel.L3_SOCIAL_CONSENSUS, LayerType.CORE): 0.9,
            (self.DepthLevel.L3_SOCIAL_CONSENSUS, LayerType.UPPER): 0.7,
            
            (self.DepthLevel.L4_PERSONAL_BELIEF, LayerType.PHYSICAL): 0.1,
            (self.DepthLevel.L4_PERSONAL_BELIEF, LayerType.BASE): 0.6,
            (self.DepthLevel.L4_PERSONAL_BELIEF, LayerType.CORE): 0.9,
            (self.DepthLevel.L4_PERSONAL_BELIEF, LayerType.UPPER): 0.8,
            
            (self.DepthLevel.L5_ABSOLUTE_BEING, LayerType.PHYSICAL): 0.0,
            (self.DepthLevel.L5_ABSOLUTE_BEING, LayerType.BASE): 0.9,
            (self.DepthLevel.L5_ABSOLUTE_BEING, LayerType.CORE): 0.9,
            (self.DepthLevel.L5_ABSOLUTE_BEING, LayerType.UPPER): 0.9,
        }
        
        return influence_matrix.get((narrative_depth, target_layer), 0.5)