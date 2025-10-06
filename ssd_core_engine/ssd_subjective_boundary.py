#!/usr/bin/env python3
"""
SSD Subjective Boundary System - 構造主観力学 主観的境界システム
SSD Core Engine統合用の主観的境界プロセッサー

Hermann Degner SSD理論に基づく主観的境界の力学：
- 内と外を分ける主観的境界として定義
- 内側：整合が容易で快・安心を得やすい領域
- 外側：整合が困難で未知の意味圧として警戒を生む領域
- 境界は主観的体験により動的に形成・変化する
"""

import math
import random
from typing import Dict, List, Set, Tuple, Optional, Any
from collections import defaultdict
from dataclasses import dataclass

try:
    # 相対インポート（パッケージとして使用時）
    from .ssd_types import LayerType, ObjectInfo
    from .ssd_meaning_pressure import MeaningPressureProcessor
except ImportError:
    # 絶対インポート（直接実行時）
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from ssd_types import LayerType, ObjectInfo
    from ssd_meaning_pressure import MeaningPressureProcessor


@dataclass
class SubjectiveBoundaryInfo:
    """主観的境界情報 - Hermann Degner理論に基づく境界定義"""
    boundary_id: str
    center: Tuple[float, float]
    radius: float
    owner_npc: str
    members: Set[str]
    established_tick: int
    boundary_strength: float = 0.0
    
    def contains(self, position: Tuple[float, float]) -> bool:
        """位置が主観的境界内にあるかチェック"""
        x, y = position
        cx, cy = self.center
        return math.sqrt((x-cx)**2 + (y-cy)**2) <= self.radius
    
    def get_distance_from_center(self, position: Tuple[float, float]) -> float:
        """境界中心からの距離"""
        x, y = position
        cx, cy = self.center
        return math.sqrt((x-cx)**2 + (y-cy)**2)
    
    def get_boundary_strength_at(self, position: Tuple[float, float]) -> float:
        """特定位置における境界強度"""
        distance = self.get_distance_from_center(position)
        if distance <= self.radius:
            # 中心に近いほど強い境界強度
            return self.boundary_strength * (1.0 - distance / self.radius)
        return 0.0


@dataclass  
class SubjectiveBoundary:
    """主観的境界 - Hermann Degner理論の核心概念"""
    npc_id: str
    inner_objects: Set[str]
    outer_objects: Set[str] 
    boundary_strength: Dict[str, float]
    
    def add_inner_experience(self, object_id: str, strength: float) -> None:
        """内側体験の追加 - 快・安心の領域拡大"""
        self.inner_objects.add(object_id)
        if object_id in self.outer_objects:
            self.outer_objects.remove(object_id)
        self.boundary_strength[object_id] = max(
            self.boundary_strength.get(object_id, 0.0), strength
        )
    
    def add_outer_experience(self, object_id: str, strength: float) -> None:
        """外側体験の追加 - 警戒・未知の領域設定"""
        self.outer_objects.add(object_id)
        if object_id in self.inner_objects:
            self.inner_objects.remove(object_id)
        self.boundary_strength[object_id] = min(
            self.boundary_strength.get(object_id, 0.0), -abs(strength)
        )
    
    def get_innerness(self, object_id: str) -> float:
        """内側度の取得 - Hermann Degner理論の主観性指標"""
        return self.boundary_strength.get(object_id, 0.0)


class SubjectiveBoundaryProcessor:
    """SSD Core Engine用主観的境界プロセッサー（Hermann Degner理論統合版）"""
    
    def __init__(self, layer_mobility: Optional[Dict[LayerType, float]] = None):
        # 主観的境界管理
        self.boundaries: Dict[str, SubjectiveBoundaryInfo] = {}
        self.npc_boundaries: Dict[str, str] = {}  # {npc_id: boundary_id}
        
        # 主観的境界システム - 理論の核心
        self.subjective_boundaries: Dict[str, SubjectiveBoundary] = {}
        
        # 境界経験の履歴
        self.boundary_experiences: Dict[str, List[Dict]] = defaultdict(list)
        
        # 集団境界
        self.collective_boundaries: Dict[str, Set[str]] = defaultdict(set)
        
        # 意味圧プロセッサー
        self.meaning_processor = MeaningPressureProcessor()
        
        # SSD理論パラメータ
        self.layer_mobility = layer_mobility or {
            LayerType.PHYSICAL: 0.1,  # 最も動きにくい
            LayerType.BASE: 0.3,      
            LayerType.CORE: 0.6,      
            LayerType.UPPER: 0.9      # 最も動きやすい
        }
        self.boundary_claim_threshold = 0.3  # 境界主張の閾値（テスト用に低く設定）
        self.boundary_strength_decay = 0.02   # 境界強度の減衰率
        self.innerness_learning_rate = 0.2    # 内側度学習率（学習を高速化）
        
    def initialize_npc_boundaries(self, npc_id: str) -> None:
        """NPCの主観的境界を初期化"""
        if npc_id not in self.subjective_boundaries:
            self.subjective_boundaries[npc_id] = SubjectiveBoundary(
                npc_id=npc_id,
                inner_objects=set(),
                outer_objects=set(),
                boundary_strength={}
            )
    
    def process_boundary_experience(self, npc_id: str, location: Tuple[float, float], 
                                  experience_type: str, experience_valence: float,
                                  other_npcs: List[str] = None, tick: int = 0) -> Dict[str, Any]:
        """
        主観的境界経験の処理（Hermann Degner SSD理論ベース）
        
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
            'boundary_changes': [],
            'boundary_updates': [],
            'meaning_pressure_delta': None,
            'collective_effects': []
        }
        
        # 位置を文字列IDに変換
        location_id = f"loc_{location[0]}_{location[1]}"
        
        # 主観的境界への経験統合
        boundary = self.subjective_boundaries[npc_id]
        
        # Hermann Degner理論：経験の感情価に基づく境界形成
        if experience_valence > 0:
            # 正の体験 → 内側領域として学習
            current_strength = boundary.get_innerness(location_id)
            new_strength = current_strength + (experience_valence * self.innerness_learning_rate)
            boundary.add_inner_experience(location_id, new_strength)
            
            result['boundary_updates'].append({
                'type': 'inner_expansion',
                'location': location,
                'strength': new_strength,
                'experience_type': experience_type
            })
        else:
            # 負の体験 → 外側領域として学習
            current_strength = boundary.get_innerness(location_id)
            new_strength = current_strength + (experience_valence * self.innerness_learning_rate)
            boundary.add_outer_experience(location_id, abs(new_strength))
            
            result['boundary_updates'].append({
                'type': 'outer_expansion', 
                'location': location,
                'strength': new_strength,
                'experience_type': experience_type
            })
        
        # 経験履歴に追加
        experience_record = {
            'tick': tick,
            'location': location,
            'type': experience_type,
            'valence': experience_valence,
            'other_npcs': other_npcs or []
        }
        self.boundary_experiences[npc_id].append(experience_record)
        
        # 意味圧の変化を計算
        try:
            objects = [ObjectInfo(
                id=location_id,
                type="location",
                properties={
                    'position': location,
                    'experience_valence': experience_valence,
                    'layer_type': LayerType.PHYSICAL
                }
            )]
            
            meaning_pressure_result = self.meaning_processor.process_meaning_pressure(
                npc_id=npc_id,
                objects=objects,
                context_info={'tick': tick, 'experience_type': experience_type}
            )
            
            if meaning_pressure_result:
                result['meaning_pressure_delta'] = meaning_pressure_result.get('pressure_delta', 0.0)
            
        except Exception as e:
            print(f"意味圧計算エラー: {e}")
            result['meaning_pressure_delta'] = 0.0
        
        # 境界形成閾値チェック（Hermann Degner理論に基づく）
        if abs(boundary.get_innerness(location_id)) > self.boundary_claim_threshold:
            boundary_formed = self._attempt_boundary_formation(npc_id, location, tick)
            if boundary_formed:
                result['boundary_changes'].append({
                    'type': 'new_boundary',
                    'boundary_info': boundary_formed
                })
        
        # 集団効果の処理
        if other_npcs:
            collective_effect = self._process_collective_boundary_effect(
                npc_id, other_npcs, location, experience_valence, tick
            )
            result['collective_effects'].append(collective_effect)
        
        return result
    
    def _attempt_boundary_formation(self, npc_id: str, location: Tuple[float, float], 
                                   tick: int) -> Optional[Dict[str, Any]]:
        """主観的境界の形成を試行"""
        boundary_id = f"boundary_{npc_id}_{tick}"
        
        # 既存の境界と重複チェック
        if npc_id in self.npc_boundaries:
            existing_id = self.npc_boundaries[npc_id]
            existing_boundary = self.boundaries[existing_id]
            
            # 近すぎる場合は境界拡張
            distance = existing_boundary.get_distance_from_center(location)
            if distance < existing_boundary.radius * 1.5:
                # 既存境界を拡張
                new_radius = max(existing_boundary.radius, distance + 5.0)
                existing_boundary.radius = new_radius
                existing_boundary.boundary_strength += 0.1
                
                return {
                    'action': 'boundary_expansion',
                    'boundary_id': existing_id,
                    'new_radius': new_radius
                }
        
        # 新しい境界を作成
        subjective_boundary = self.subjective_boundaries[npc_id]
        location_id = f"loc_{location[0]}_{location[1]}"
        strength = abs(subjective_boundary.get_innerness(location_id))
        
        new_boundary = SubjectiveBoundaryInfo(
            boundary_id=boundary_id,
            center=location,
            radius=max(3.0, strength * 10.0),  # 強度に基づく半径
            owner_npc=npc_id,
            members={npc_id},
            established_tick=tick,
            boundary_strength=strength
        )
        
        self.boundaries[boundary_id] = new_boundary
        self.npc_boundaries[npc_id] = boundary_id
        
        return {
            'action': 'new_boundary_created',
            'boundary_id': boundary_id,
            'center': location,
            'radius': new_boundary.radius,
            'strength': strength
        }
    
    def _process_collective_boundary_effect(self, npc_id: str, other_npcs: List[str], 
                                          location: Tuple[float, float], 
                                          experience_valence: float, tick: int) -> Dict[str, Any]:
        """集団による境界効果の処理"""
        collective_id = f"collective_{min(npc_id, *other_npcs)}_{max(npc_id, *other_npcs)}"
        
        # 全参加者の境界を初期化
        for participant in [npc_id] + other_npcs:
            self.initialize_npc_boundaries(participant)
        
        # 集団境界に参加者を追加
        self.collective_boundaries[collective_id].update([npc_id] + other_npcs)
        
        # 集団効果強度を計算
        group_size = len(other_npcs) + 1
        collective_multiplier = 1.0 + (group_size - 1) * 0.3  # グループサイズによる増幅
        
        # 各参加者の主観的境界に集団効果を適用
        location_id = f"loc_{location[0]}_{location[1]}"
        affected_npcs = []
        
        for participant in [npc_id] + other_npcs:
            boundary = self.subjective_boundaries[participant]
            enhanced_valence = experience_valence * collective_multiplier
            
            if enhanced_valence > 0:
                current_strength = boundary.get_innerness(location_id)
                new_strength = current_strength + (enhanced_valence * self.innerness_learning_rate)
                boundary.add_inner_experience(location_id, new_strength)
            else:
                current_strength = boundary.get_innerness(location_id)  
                new_strength = current_strength + (enhanced_valence * self.innerness_learning_rate)
                boundary.add_outer_experience(location_id, abs(new_strength))
            
            affected_npcs.append({
                'npc_id': participant,
                'new_strength': new_strength,
                'enhanced_valence': enhanced_valence
            })
        
        return {
            'collective_id': collective_id,
            'group_size': group_size,
            'multiplier': collective_multiplier,
            'affected_npcs': affected_npcs
        }
    
    def get_boundary_state(self, npc_id: str) -> Dict[str, Any]:
        """NPCの主観的境界状態取得"""
        state = {
            'has_boundary': False,
            'boundary_info': None,
            'subjective_boundary': None,
            'experience_count': 0,
            'collective_memberships': []
        }
        
        # 物理的境界情報
        if npc_id in self.npc_boundaries:
            boundary_id = self.npc_boundaries[npc_id]
            state['has_boundary'] = True
            state['boundary_info'] = self.boundaries[boundary_id]
        
        # 主観的境界情報  
        if npc_id in self.subjective_boundaries:
            boundary = self.subjective_boundaries[npc_id]
            state['subjective_boundary'] = {
                'inner_count': len(boundary.inner_objects),
                'outer_count': len(boundary.outer_objects),
                'total_strength': sum(abs(v) for v in boundary.boundary_strength.values()),
                'strongest_inner': max((v for v in boundary.boundary_strength.values() if v > 0), default=0),
                'strongest_outer': min((v for v in boundary.boundary_strength.values() if v < 0), default=0)
            }
        
        # 経験数
        state['experience_count'] = len(self.boundary_experiences.get(npc_id, []))
        
        # 集団所属
        for collective_id, members in self.collective_boundaries.items():
            if npc_id in members:
                state['collective_memberships'].append({
                    'collective_id': collective_id,
                    'member_count': len(members),
                    'members': list(members)
                })
        
        return state
    
    def create_boundary_v2(self, center: Tuple[float, float], radius: float, owner_npc: str) -> str:
        """主観的境界作成（v2版）"""
        # 境界経験を処理して境界作成
        result = self.process_boundary_experience(
            npc_id=owner_npc,
            location=center,
            experience_type="boundary_establishment",
            experience_valence=0.8,  # 強い正の体験として設定
            tick=0
        )
        
        if result['boundary_changes']:
            boundary_info = result['boundary_changes'][0]['boundary_info']
            return boundary_info['boundary_id']
        
        # フォールバック：直接作成
        boundary_id = f"boundary_{owner_npc}_{hash(center) % 10000}"
        new_boundary = SubjectiveBoundaryInfo(
            boundary_id=boundary_id,
            center=center,
            radius=radius,
            owner_npc=owner_npc,
            members={owner_npc},
            established_tick=0,
            boundary_strength=0.8
        )
        
        self.boundaries[boundary_id] = new_boundary
        self.npc_boundaries[owner_npc] = boundary_id
        self.initialize_npc_boundaries(owner_npc)
        
        return boundary_id
    
    def add_npc_to_boundary(self, boundary_id: str, npc_id: str) -> bool:
        """NPCを主観的境界に追加"""
        if boundary_id not in self.boundaries:
            return False
        
        boundary = self.boundaries[boundary_id]
        boundary.members.add(npc_id)
        
        # 主観的境界も初期化
        self.initialize_npc_boundaries(npc_id)
        
        # 境界内での協力経験として記録
        self.process_boundary_experience(
            npc_id=npc_id,
            location=boundary.center,
            experience_type="boundary_joining",
            experience_valence=0.6,
            other_npcs=list(boundary.members - {npc_id}),
            tick=0
        )
        
        return True
    
    def get_boundary_interactions(self, npc_id: str, other_npc: str) -> Dict[str, Any]:
        """2つのNPC間の主観的境界相互作用を分析"""
        if npc_id not in self.subjective_boundaries or other_npc not in self.subjective_boundaries:
            return {'interaction_strength': 0.0, 'shared_experiences': []}
        
        boundary1 = self.subjective_boundaries[npc_id]
        boundary2 = self.subjective_boundaries[other_npc]
        
        # 共通の内側オブジェクト
        shared_inner = boundary1.inner_objects & boundary2.inner_objects
        shared_outer = boundary1.outer_objects & boundary2.outer_objects
        
        # 相互作用強度計算
        interaction_strength = 0.0
        shared_experiences = []
        
        for obj_id in shared_inner:
            strength1 = boundary1.get_innerness(obj_id)
            strength2 = boundary2.get_innerness(obj_id)
            synergy = min(strength1, strength2) * 0.8  # 正の相乗効果
            interaction_strength += synergy
            shared_experiences.append({
                'object_id': obj_id,
                'type': 'shared_inner',
                'strength1': strength1,
                'strength2': strength2,
                'synergy': synergy
            })
        
        for obj_id in shared_outer:
            strength1 = abs(boundary1.get_innerness(obj_id))
            strength2 = abs(boundary2.get_innerness(obj_id))
            conflict = min(strength1, strength2) * -0.5  # 負の対立効果
            interaction_strength += conflict
            shared_experiences.append({
                'object_id': obj_id,
                'type': 'shared_outer',
                'strength1': -strength1,
                'strength2': -strength2,
                'conflict': conflict
            })
        
        return {
            'interaction_strength': interaction_strength,
            'shared_inner_count': len(shared_inner),
            'shared_outer_count': len(shared_outer), 
            'shared_experiences': shared_experiences
        }
    
    def decay_boundary_strengths(self, decay_rate: Optional[float] = None) -> Dict[str, int]:
        """主観的境界強度の時間減衰処理"""
        decay_rate = decay_rate or self.boundary_strength_decay
        decayed_count = {'inner': 0, 'outer': 0, 'removed': 0}
        
        for npc_id, boundary in self.subjective_boundaries.items():
            objects_to_remove = []
            
            for obj_id, strength in boundary.boundary_strength.items():
                if strength > 0:
                    # 正の強度（内側）の減衰
                    new_strength = strength * (1.0 - decay_rate)
                    if new_strength < 0.01:  # 閾値以下で削除
                        objects_to_remove.append(obj_id)
                        decayed_count['removed'] += 1
                    else:
                        boundary.boundary_strength[obj_id] = new_strength
                        decayed_count['inner'] += 1
                elif strength < 0:
                    # 負の強度（外側）の減衰
                    new_strength = strength * (1.0 - decay_rate)
                    if new_strength > -0.01:  # 閾値以上で削除
                        objects_to_remove.append(obj_id)
                        decayed_count['removed'] += 1
                    else:
                        boundary.boundary_strength[obj_id] = new_strength
                        decayed_count['outer'] += 1
            
            # 弱くなったオブジェクトを削除
            for obj_id in objects_to_remove:
                del boundary.boundary_strength[obj_id]
                boundary.inner_objects.discard(obj_id)
                boundary.outer_objects.discard(obj_id)
        
        return decayed_count

# 後方互換性のためのエイリアス（段階的移行用）
TerritoryInfo = SubjectiveBoundaryInfo  # 後方互換性
TerritoryProcessor = SubjectiveBoundaryProcessor  # 後方互換性