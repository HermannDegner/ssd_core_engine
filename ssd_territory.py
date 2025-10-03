#!/usr/bin/env python3
"""
SSD Territory System - 構造主観力学 縄張りシステム
SSD Core Engine統合用の縄張りプロセッサー

SSD理論に基づく縄張りの力学：
- 内と外を分ける境界として定義
- 内側：整合が容易で快・安心を得やすい領域
- 外側：整合が困難で未知の意味圧として警戒を生む領域
"""

import math
import random
from typing import Dict, List, Set, Tuple, Optional, Any
from collections import defaultdict
from dataclasses import dataclass

from .ssd_types import LayerType, ObjectInfo
from .ssd_meaning_pressure import MeaningPressureProcessor


@dataclass
class TerritoryInfo:
    """縄張り情報"""
    territory_id: str
    center: Tuple[float, float]
    radius: float
    owner_npc: str
    members: Set[str]
    established_tick: int
    territorial_strength: float = 0.0
    
    def contains(self, position: Tuple[float, float]) -> bool:
        """位置が縄張り内にあるかチェック"""
        x, y = position
        cx, cy = self.center
        return math.sqrt((x-cx)**2 + (y-cy)**2) <= self.radius
    
    def get_distance_from_center(self, position: Tuple[float, float]) -> float:
        """縄張り中心からの距離"""
        x, y = position
        cx, cy = self.center
        return math.sqrt((x-cx)**2 + (y-cy)**2)
    
    def add_member(self, npc_id: str) -> None:
        """メンバー追加"""
        self.members.add(npc_id)
    
    def remove_member(self, npc_id: str) -> None:
        """メンバー削除"""
        self.members.discard(npc_id)
    
    def get_community_size(self) -> int:
        """コミュニティサイズ"""
        return len(self.members)


@dataclass 
class SubjectiveBoundary:
    """主観的境界情報"""
    npc_id: str
    inner_objects: Set[str]  # 内側として認識するオブジェクト
    outer_objects: Set[str]  # 外側として認識するオブジェト
    boundary_strength: Dict[str, float]  # {object_id: strength}
    
    def is_inner(self, object_id: str) -> bool:
        """オブジェクトが内側かどうか"""
        return object_id in self.inner_objects
    
    def is_outer(self, object_id: str) -> bool:
        """オブジェクトが外側かどうか"""
        return object_id in self.outer_objects
    
    def get_boundary_strength(self, object_id: str) -> float:
        """境界強度を取得"""
        return self.boundary_strength.get(object_id, 0.0)


class TerritoryProcessor:
    """SSD Core Engine用縄張りプロセッサー"""
    
    def __init__(self):
        # 縄張り管理
        self.territories: Dict[str, TerritoryInfo] = {}
        self.npc_territories: Dict[str, str] = {}  # {npc_id: territory_id}
        
        # 主観的境界システム
        self.subjective_boundaries: Dict[str, SubjectiveBoundary] = {}
        
        # 縄張り経験の履歴
        self.territorial_experiences: Dict[str, List[Dict]] = defaultdict(list)
        
        # 集団境界
        self.collective_boundaries: Dict[str, Set[str]] = defaultdict(set)
        
        # 意味圧プロセッサー
        self.meaning_processor = MeaningPressureProcessor()
        
        # SSD理論パラメータ
        self.territory_claim_threshold = 0.6  # 縄張り主張の閾値
        self.boundary_strength_decay = 0.02   # 境界強度の減衰率
        self.innerness_learning_rate = 0.1    # 内側度学習率
        
    def initialize_npc_boundaries(self, npc_id: str) -> None:
        """NPCの主観的境界を初期化"""
        if npc_id not in self.subjective_boundaries:
            self.subjective_boundaries[npc_id] = SubjectiveBoundary(
                npc_id=npc_id,
                inner_objects=set(),
                outer_objects=set(),
                boundary_strength={}
            )
    
    def process_territorial_experience(self, npc_id: str, location: Tuple[float, float], 
                                     experience_type: str, experience_valence: float,
                                     other_npcs: List[str] = None, tick: int = 0) -> Dict[str, Any]:
        """
        縄張り経験の処理（SSD理論ベース）
        
        Args:
            npc_id: NPC ID
            location: 経験が発生した位置
            experience_type: 経験タイプ ('safe_rest', 'successful_forage', 'social_cooperation', etc.)
            experience_valence: 経験の感情価 (-1.0 to 1.0)
            other_npcs: 共同経験したNPCs
            tick: 現在のティック
            
        Returns:
            処理結果の辞書
        """
        self.initialize_npc_boundaries(npc_id)
        
        result = {
            'territorial_changes': [],
            'boundary_updates': [],
            'collective_formation': None,
            'meaning_pressure_delta': 0.0
        }
        
        # 経験を記録
        experience = {
            'tick': tick,
            'location': location,
            'type': experience_type,
            'valence': experience_valence,
            'participants': other_npcs or []
        }
        self.territorial_experiences[npc_id].append(experience)
        
        # 位置の内側度を更新
        location_id = f"loc_{location[0]:.1f}_{location[1]:.1f}"
        self._update_innerness(npc_id, location_id, experience_valence, experience_type)
        
        # 縄張り主張の判定
        if experience_valence > self.territory_claim_threshold:
            territory_result = self._evaluate_territory_claim(npc_id, location, experience, tick)
            if territory_result:
                result['territorial_changes'].append(territory_result)
        
        # 共同経験による集団境界形成
        if other_npcs and experience_valence > 0.3:
            collective_result = self._form_collective_boundary(npc_id, other_npcs, location, experience_type, tick)
            if collective_result:
                result['collective_formation'] = collective_result
        
        # SSD意味圧の計算
        meaning_pressure_delta = self._calculate_territorial_meaning_pressure(npc_id, location, experience_valence)
        result['meaning_pressure_delta'] = meaning_pressure_delta
        
        return result
    
    def _update_innerness(self, npc_id: str, object_id: str, valence: float, experience_type: str) -> None:
        """オブジェクトの内側度を更新"""
        boundary = self.subjective_boundaries[npc_id]
        
        # 現在の強度を取得
        current_strength = boundary.get_boundary_strength(object_id)
        
        # SSD理論：反復接触による内側化
        experience_weights = {
            'safe_rest': 0.8,
            'successful_forage': 0.6,
            'social_cooperation': 0.7,
            'water_access': 0.5,
            'territory_defense': 0.9,
            'hostile_encounter': -0.8,
            'resource_theft': -0.9
        }
        
        weight = experience_weights.get(experience_type, 0.3)
        strength_delta = self.innerness_learning_rate * valence * weight
        
        new_strength = current_strength + strength_delta
        new_strength = max(-1.0, min(1.0, new_strength))  # クランプ
        
        boundary.boundary_strength[object_id] = new_strength
        
        # 内側・外側の判定更新
        if new_strength > 0.3:
            boundary.inner_objects.add(object_id)
            boundary.outer_objects.discard(object_id)
        elif new_strength < -0.3:
            boundary.outer_objects.add(object_id)
            boundary.inner_objects.discard(object_id)
    
    def _evaluate_territory_claim(self, npc_id: str, location: Tuple[float, float], 
                                experience: Dict, tick: int) -> Optional[Dict]:
        """縄張り主張の評価"""
        # 既に縄張りを持っている場合はスキップ
        if npc_id in self.npc_territories:
            return None
        
        # 安全感の計算（SSD理論ベース）
        safety_feeling = self._calculate_safety_feeling(npc_id, location)
        
        if safety_feeling >= self.territory_claim_threshold:
            # 新しい縄張りを作成
            territory_id = f"territory_{npc_id}_{tick}"
            radius = 8 + int(safety_feeling * 8)  # 安全感による可変半径
            
            territory = TerritoryInfo(
                territory_id=territory_id,
                center=location,
                radius=radius,
                owner_npc=npc_id,
                members={npc_id},
                established_tick=tick,
                territorial_strength=safety_feeling
            )
            
            self.territories[territory_id] = territory
            self.npc_territories[npc_id] = territory_id
            
            return {
                'action': 'territory_claimed',
                'npc_id': npc_id,
                'territory_id': territory_id,
                'location': location,
                'radius': radius,
                'safety_feeling': safety_feeling,
                'tick': tick
            }
        
        return None
    
    def _calculate_safety_feeling(self, npc_id: str, location: Tuple[float, float]) -> float:
        """安全感の計算（オキシトシン的縄張り効果）"""
        safety = 0.0
        
        # 1. 場所の慣れ（反復滞在による安心感）
        location_id = f"loc_{location[0]:.1f}_{location[1]:.1f}"
        boundary = self.subjective_boundaries[npc_id]
        place_familiarity = boundary.get_boundary_strength(location_id)
        safety += max(0, place_familiarity) * 0.4
        
        # 2. 仲間の存在による安心感
        nearby_allies = self._count_nearby_allies(npc_id, location)
        safety += min(0.3, nearby_allies * 0.1)
        
        # 3. 資源へのアクセス性
        resource_accessibility = self._evaluate_resource_access(location)
        safety += resource_accessibility * 0.3
        
        return min(1.0, safety)
    
    def _count_nearby_allies(self, npc_id: str, location: Tuple[float, float]) -> int:
        """近くの仲間の数をカウント"""
        # 実装では実際のNPC位置情報が必要
        # ここでは仮の実装
        allies = 0
        for other_npc in self.subjective_boundaries:
            if other_npc != npc_id:
                boundary = self.subjective_boundaries[npc_id]
                if boundary.is_inner(other_npc):
                    allies += 1
        return allies
    
    def _evaluate_resource_access(self, location: Tuple[float, float]) -> float:
        """資源へのアクセス性評価"""
        # 実装では実際の環境情報が必要
        # ここでは仮の実装
        return random.uniform(0.2, 0.8)
    
    def _form_collective_boundary(self, leader_npc: str, participant_npcs: List[str], 
                                location: Tuple[float, float], experience_type: str, tick: int) -> Dict:
        """集団境界の形成"""
        group_id = f"group_{leader_npc}_{tick}"
        participants = {leader_npc} | set(participant_npcs)
        
        self.collective_boundaries[group_id] = participants
        
        # 参加者全員の主観的境界を更新
        for npc_id in participants:
            self.initialize_npc_boundaries(npc_id)
            # お互いを内側として認識
            for other_npc in participants:
                if other_npc != npc_id:
                    boundary = self.subjective_boundaries[npc_id]
                    boundary.inner_objects.add(other_npc)
                    boundary.boundary_strength[other_npc] = 0.7
        
        return {
            'action': 'collective_boundary_formed',
            'group_id': group_id,
            'participants': list(participants),
            'location': location,
            'experience_type': experience_type,
            'tick': tick
        }
    
    def _calculate_territorial_meaning_pressure(self, npc_id: str, location: Tuple[float, float], 
                                              valence: float) -> float:
        """縄張り的意味圧の計算"""
        # SSD理論：縄張り侵犯や協調による意味圧の変化
        pressure_delta = 0.0
        
        # 1. 既存縄張りとの関係
        for territory_id, territory in self.territories.items():
            if territory.contains(location):
                if npc_id in territory.members:
                    # 自分の縄張り内での経験
                    pressure_delta -= abs(valence) * 0.3  # 意味圧軽減
                else:
                    # 他者の縄張りへの侵入
                    pressure_delta += abs(valence) * 0.5  # 意味圧増加
        
        # 2. 社会的意味圧
        boundary = self.subjective_boundaries[npc_id]
        if len(boundary.inner_objects) > 0:
            # 仲間がいる場合は意味圧軽減
            pressure_delta -= 0.2
        
        return pressure_delta
    
    def get_territorial_state(self, npc_id: str) -> Dict[str, Any]:
        """NPCの縄張り状態を取得"""
        self.initialize_npc_boundaries(npc_id)
        
        territory_info = None
        if npc_id in self.npc_territories:
            territory_id = self.npc_territories[npc_id]
            territory_info = self.territories[territory_id]
        
        boundary = self.subjective_boundaries[npc_id]
        
        return {
            'has_territory': territory_info is not None,
            'territory_info': territory_info,
            'inner_objects_count': len(boundary.inner_objects),
            'outer_objects_count': len(boundary.outer_objects),
            'collective_memberships': [
                group_id for group_id, members in self.collective_boundaries.items()
                if npc_id in members
            ],
            'total_experiences': len(self.territorial_experiences[npc_id])
        }
    
    def check_territorial_interaction(self, npc_id: str, target_location: Tuple[float, float]) -> Dict[str, Any]:
        """縄張り的相互作用のチェック"""
        result = {
            'is_own_territory': False,
            'is_others_territory': False,
            'territory_owner': None,
            'intrusion_level': 0.0,
            'recommended_action': 'neutral'
        }
        
        # 各縄張りとの関係をチェック
        for territory_id, territory in self.territories.items():
            if territory.contains(target_location):
                if npc_id in territory.members:
                    result['is_own_territory'] = True
                    result['recommended_action'] = 'safe_stay'
                else:
                    result['is_others_territory'] = True
                    result['territory_owner'] = territory.owner_npc
                    
                    # 侵入レベルの計算
                    distance_from_center = territory.get_distance_from_center(target_location)
                    intrusion_level = 1.0 - (distance_from_center / territory.radius)
                    result['intrusion_level'] = intrusion_level
                    
                    # 関係性による推奨行動
                    boundary = self.subjective_boundaries[npc_id]
                    if boundary.is_inner(territory.owner_npc):
                        result['recommended_action'] = 'friendly_approach'
                    elif intrusion_level > 0.7:
                        result['recommended_action'] = 'retreat'
                    else:
                        result['recommended_action'] = 'cautious_approach'
                break
        
        return result
    
    def decay_boundaries(self) -> None:
        """境界強度の自然減衰"""
        for npc_id, boundary in self.subjective_boundaries.items():
            for object_id in list(boundary.boundary_strength.keys()):
                current = boundary.boundary_strength[object_id]
                decayed = current * (1 - self.boundary_strength_decay)
                
                if abs(decayed) < 0.1:
                    # 閾値以下になったら削除
                    del boundary.boundary_strength[object_id]
                    boundary.inner_objects.discard(object_id)
                    boundary.outer_objects.discard(object_id)
                else:
                    boundary.boundary_strength[object_id] = decayed