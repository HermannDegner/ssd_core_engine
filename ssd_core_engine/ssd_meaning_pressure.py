"""
SSD Meaning Pressure System
構造主観力学 - 意味圧システム
"""

import random
import numpy as np
from typing import Dict, List, Optional
from collections import defaultdict

try:
    from .ssd_types import ObjectInfo, LayerType, StructuralState
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from ssd_types import ObjectInfo, LayerType, StructuralState


class MeaningPressureProcessor:
    """意味圧処理システム"""
    
    def __init__(self):
        self.E = 0.0  # 未処理圧（熱）
        self.experience_log = []
        self._similarity_cache = {}
        
    def calculate_layer_meaning_pressure(self, obj_info: ObjectInfo, layer: LayerType, 
                                       existing_structures: Dict[str, StructuralState]) -> float:
        """特定層での意味圧を計算（数学的厳密性向上）"""
        base_meaning = obj_info.meaning_values.get(layer, 0.0)
        
        # 意味圧の基本式: P = φ * exp(-β * t) + α * ∇²φ
        # φ: 意味場の強度, β: 減衰係数, α: 拡散係数
        phi = base_meaning * obj_info.survival_relevance
        beta = 0.1  # 減衰係数
        alpha = 0.3  # 拡散係数
        
        # その層の既存構造との整合性をチェック
        alignment_resistance = 0.0
        structural_interaction = 0.0
        
        for element_id, state in existing_structures.items():
            if state.layer == layer:
                # 既存要素との相互作用（改善された類似度計算）
                similarity = self.calculate_enhanced_similarity(obj_info, element_id, layer)
                resistance = (1.0 - similarity) * state.activation
                alignment_resistance += resistance
                
                # 構造的相互作用項
                structural_interaction += similarity * state.stability * 0.2
        
        # 改善された意味圧計算: P = φ * (1 + α * ∇²φ) - β * R + γ * S
        # R: 整合抵抗, S: 構造的相互作用, γ: 相互作用係数
        gamma = 0.4
        enhanced_pressure = phi * (1 + alpha * structural_interaction) - beta * alignment_resistance + gamma * structural_interaction
        
        return max(0.0, enhanced_pressure)
    
    def calculate_enhanced_similarity(self, obj_info: ObjectInfo, element_id: str, layer: LayerType) -> float:
        """改善された類似度計算（キャッシュ付き）"""
        cache_key = f"{obj_info.id}_{element_id}_{layer.value}"
        
        # キャッシュチェック（短期記憶）
        if cache_key in self._similarity_cache:
            return self._similarity_cache[cache_key]
        
        # 類似度計算の改善
        base_similarity = 0.5
        
        # タイプベースの類似度
        type_bonus = 0.3 if obj_info.type in element_id else 0.0
        
        # 生存関連度による修正
        survival_modifier = obj_info.survival_relevance * layer.get_survival_weight() * 0.2
        
        # プロパティベースの類似度（簡略版）
        property_similarity = 0.1 if obj_info.properties else 0.0
        
        # ランダム要素（創発性確保）
        random_factor = random.uniform(-0.2, 0.2)
        
        similarity = min(1.0, max(0.0, base_similarity + type_bonus + survival_modifier + property_similarity + random_factor))
        
        # キャッシュに保存（メモリ制限付き）
        if len(self._similarity_cache) < 1000:  # メモリ制限
            self._similarity_cache[cache_key] = similarity
        
        return similarity
    
    def add_meaning_pressure(self, pressure: float, source_id: str):
        """未処理圧を蓄積"""
        self.E = min(10.0, self.E + pressure * 0.3)
        
        # 体験ログ
        self.experience_log.append({
            'source': source_id,
            'pressure': pressure,
            'total_E': self.E,
            'timestamp': len(self.experience_log)
        })
    
    def calculate_total_pressure(self, obj_info: ObjectInfo, layer_structures: Dict[LayerType, Dict[str, StructuralState]], 
                               layer_mobility: Dict[LayerType, float]) -> float:
        """全層での総意味圧を計算"""
        total_pressure = 0.0
        for layer in LayerType:
            existing_structures = layer_structures.get(layer, {})
            layer_pressure = self.calculate_layer_meaning_pressure(obj_info, layer, existing_structures)
            total_pressure += layer_pressure * layer_mobility[layer]
        
        self.add_meaning_pressure(total_pressure, obj_info.id)
        return total_pressure
    
    def natural_decay(self, decay_rate: float = 0.95):
        """未処理圧の自然減衰"""
        self.E = max(0.0, self.E * decay_rate)
    
    def cleanup_cache(self, max_size: int = 500):
        """類似度キャッシュのクリーンアップ"""
        if len(self._similarity_cache) > max_size:
            # 古いキャッシュの半分を削除
            cache_items = list(self._similarity_cache.items())
            self._similarity_cache = dict(cache_items[-max_size//2:])
    
    def get_pressure_statistics(self) -> Dict[str, float]:
        """意味圧統計の取得"""
        if not self.experience_log:
            return {'mean_pressure': 0.0, 'max_pressure': 0.0, 'pressure_count': 0}
        
        pressures = [exp.get('pressure', 0) for exp in self.experience_log if 'pressure' in exp]
        
        return {
            'mean_pressure': np.mean(pressures) if pressures else 0.0,
            'max_pressure': max(pressures) if pressures else 0.0,
            'pressure_count': len(pressures),
            'current_E': self.E
        }