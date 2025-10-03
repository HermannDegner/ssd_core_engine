"""
SSD Types and Core Data Structures
構造主観力学 - 基本型定義

💡 FUNDAMENTAL PRINCIPLE:
整合慣性κ (Coherence Inertia) = 記憶蓄積フレームワーク

κは物理的な慣性と同様に、主観的体験の蓄積による「心理的慣性」を表現する。
過去の体験が現在の判断に与える影響の強度として機能し、
記憶に基づく適応的行動の基盤となる。

κ値の意味:
- 低κ: 新規体験、記憶蓄積が少ない状態  
- 高κ: 豊富な記憶、強い適応傾向を持つ状態

【Structure Subjective Dynamics】における κ の位置づけ:
物理層から意識層までの四層構造において、κは各層の「記憶密度」を表し、
主観的体験の物理的実装として機能する。これにより、エージェントは
過去の体験を現在の行動決定に統合できる真の学習システムを実現する。
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import random
import numpy as np

# 🔗 SSD基礎理論参照: https://github.com/HermannDegner/Structural-Subjectivity-Dynamics
# この実装は常に基礎理論リポジトリの指定に従います


class LayerType(Enum):
    """四層構造の定義"""
    PHYSICAL = "physical"    # 物理層: 最も動きにくい、基本制約
    BASE = "base"           # 基層: 本能、感情、生存
    CORE = "core"           # 中核層: アイデンティティ、価値観
    UPPER = "upper"         # 上層: 概念、理念、最も軽い
    
    def get_survival_weight(self) -> float:
        """基層的色付け：生存に関わる重み係数"""
        weights = {
            LayerType.PHYSICAL: 1.0,  # 最も基層的（生存直結）
            LayerType.BASE: 0.9,      # 基本的生存本能
            LayerType.CORE: 0.6,      # 記憶・経験による生存判断
            LayerType.UPPER: 0.3      # 抽象的思考（生存から遠い）
        }
        return weights.get(self, 0.5)


@dataclass
class ObjectInfo:
    """オブジェクト情報の統一表現"""
    id: str
    type: str
    properties: Dict[str, Any] = field(default_factory=dict)
    # 未来予測用の状態情報
    current_value: float = 0.0  # 現在の価値
    decline_rate: float = 0.0   # 減衰率
    volatility: float = 0.1     # 変動性
    # SSD理論統合情報
    survival_relevance: float = 0.0  # 生存関連度 (0.0-1.0)
    meaning_values: Dict[LayerType, float] = field(default_factory=dict)
    relationships: Dict[str, List[str]] = field(default_factory=dict)
    
    def __post_init__(self):
        # 各層のデフォルト意味値を設定
        for layer in LayerType:
            if layer not in self.meaning_values:
                self.meaning_values[layer] = 0.0
        
        # 生存関連度の自動計算
        self.calculate_survival_relevance()
    
    def calculate_survival_relevance(self) -> float:
        """生存関連度の計算（基層的色付けの基準）"""
        survival_types = {
            'food': 1.0,      # 最高優先度
            'water': 1.0,     # 最高優先度
            'shelter': 0.9,   # 高優先度
            'fire': 0.8,      # 高優先度（暖・調理）
            'tool': 0.7,      # 中優先度（生存支援）
            'weapon': 0.8,    # 高優先度（防御）
            'medicine': 0.9,  # 高優先度（健康）
            'obstacle': 0.4,  # 低優先度（回避対象）
            'threat': 0.9,    # 高優先度（危険回避）
            'danger': 0.9,    # 高優先度（危険回避）
            'resource': 0.5   # 中優先度
        }
        
        base_relevance = survival_types.get(self.type, 0.3)
        
        # プロパティによる修正
        if 'danger_level' in self.properties:
            # 危険度が高いほど生存関連度も高くなる（回避必要性）
            base_relevance += min(self.properties['danger_level'] * 0.4, 0.3)
        
        if 'nutritional_value' in self.properties:
            # 栄養価による修正
            base_relevance += min(self.properties['nutritional_value'] / 100.0, 0.2)
        
        if 'durability' in self.properties and self.type == 'tool':
            # 道具の耐久性による修正
            base_relevance += min(self.properties['durability'] / 200.0, 0.1)
        
        if 'temperature' in self.properties and self.type == 'fire':
            # 火の温度による修正（暖房・調理能力）
            base_relevance += min(self.properties['temperature'] / 1000.0, 0.15)
        
        self.survival_relevance = min(base_relevance, 1.0)
        return self.survival_relevance


@dataclass 
class StructuralState:
    """四層構造の状態"""
    layer: LayerType
    connections: Dict[str, float] = field(default_factory=dict)  # 他要素との接続強度
    activation: float = 0.0  # 現在の活性度
    stability: float = 1.0   # 安定度（動きにくさ）
    kappa: Dict[str, float] = field(default_factory=dict)  # 整合慣性


@dataclass
class AlignmentResult:
    """整合処理の結果"""
    alignment_flows: Dict[str, Dict[str, float]] = field(default_factory=dict)
    kappa_updates: Dict[str, float] = field(default_factory=dict)
    energy_changes: Dict[str, float] = field(default_factory=dict)


@dataclass
class LeapResult:
    """跳躍実行の結果"""
    leap_type: str = "none"
    affected_layers: List[str] = field(default_factory=list)
    new_connections: Dict[str, Any] = field(default_factory=dict)
    alignment_changes: Dict[str, Any] = field(default_factory=dict)
    survival_driven: bool = False


@dataclass
class DecisionInfo:
    """意思決定情報"""
    chosen_action: str
    scores: Dict[str, float] = field(default_factory=dict)
    exploration_mode: bool = False
    E_level: float = 0.0
    T_level: float = 0.0


@dataclass
class PredictionResult:
    """未来予測の結果"""
    object_id: str
    current_value: float
    predictions: List[float] = field(default_factory=list)
    crisis_level: str = "none"
    confidence: float = 0.0
    trend_modifier: float = 1.0
    steps_ahead: int = 0
    timestamp: int = 0


@dataclass
class SystemState:
    """システム全体の状態"""
    agent_id: str
    energy: Dict[str, float] = field(default_factory=dict)
    structure: Dict[str, Any] = field(default_factory=dict)
    cognition: Dict[str, Any] = field(default_factory=dict)
    memory_usage: Dict[str, int] = field(default_factory=dict)
    performance: Dict[str, float] = field(default_factory=dict)