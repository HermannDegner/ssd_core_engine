"""
SSD Prediction and Future Analysis System
構造主観力学 - 予測・未来分析システム
"""

import random
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from collections import deque

try:
    from .ssd_types import ObjectInfo, PredictionResult
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from ssd_types import ObjectInfo, PredictionResult


class PredictionSystem:
    """未来予測システム"""
    
    def __init__(self, prediction_horizon: int = 3, prediction_accuracy: float = 0.8):
        self.prediction_horizon = prediction_horizon
        self.prediction_accuracy = prediction_accuracy
        self.trend_memory = deque(maxlen=10)
        self.prediction_cache = {}
        self.crisis_detection_enabled = True
        
    def predict_future_state(self, target_object_id: str, perceived_objects: Dict[str, ObjectInfo], 
                           steps_ahead: int = None, current_time: int = 0) -> PredictionResult:
        """未来状態予測（最適化版）"""
        if steps_ahead is None:
            steps_ahead = self.prediction_horizon
            
        # キャッシュチェック（タイムスタンプ付き）
        cache_key = f"{target_object_id}_{steps_ahead}"
        
        if (cache_key in self.prediction_cache and 
            current_time - self.prediction_cache[cache_key].timestamp < 5):  # 5ステップ有効
            return self.prediction_cache[cache_key]
        
        if target_object_id not in perceived_objects:
            return PredictionResult(
                object_id=target_object_id,
                current_value=0.0,
                predictions=[],
                crisis_level="none",
                confidence=0.0,
                timestamp=current_time
            )
        
        target_obj = perceived_objects[target_object_id]
        
        # 現在値と変化率を取得
        current_value = target_obj.current_value
        decline_rate = target_obj.decline_rate
        volatility = target_obj.volatility
        
        # トレンド分析（最近の変化を考慮）
        trend_modifier = self._calculate_trend_modifier(target_object_id)
        adjusted_decline_rate = decline_rate * trend_modifier
        
        # 未来値の予測
        predictions = []
        for step in range(1, steps_ahead + 1):
            # 基本減衰モデル
            predicted_base = current_value - (adjusted_decline_rate * step)
            
            # ランダム変動（予測精度に基づく）
            random_factor = random.uniform(-volatility, volatility) * (1 - self.prediction_accuracy)
            predicted_value = max(0, predicted_base + random_factor)
            
            predictions.append(predicted_value)
        
        # 危機レベルの判定
        crisis_level = self._assess_crisis_level(predictions, target_obj.type)
        
        # 信頼度の計算
        confidence = self._calculate_prediction_confidence(target_obj, steps_ahead)
        
        result = PredictionResult(
            object_id=target_object_id,
            current_value=current_value,
            predictions=predictions,
            crisis_level=crisis_level,
            confidence=confidence,
            trend_modifier=trend_modifier,
            steps_ahead=steps_ahead,
            timestamp=current_time
        )
        
        # 結果をキャッシュ（メモリ制限付き）
        if len(self.prediction_cache) < 100:  # メモリ制限
            self.prediction_cache[cache_key] = result
        else:
            # 古いキャッシュをクリア
            self._cleanup_prediction_cache(current_time)
            self.prediction_cache[cache_key] = result
        
        return result
    
    def predict_multiple_futures(self, object_ids: List[str], perceived_objects: Dict[str, ObjectInfo], 
                               steps_ahead: int = None, current_time: int = 0) -> Dict[str, Any]:
        """複数オブジェクトの未来予測"""
        if steps_ahead is None:
            steps_ahead = self.prediction_horizon
            
        predictions = {}
        total_crisis_score = 0.0
        objects_in_crisis = []
        
        for obj_id in object_ids:
            if obj_id in perceived_objects:
                pred = self.predict_future_state(obj_id, perceived_objects, steps_ahead, current_time)
                predictions[obj_id] = pred
                
                # 危機スコアの集計
                if pred.crisis_level != "none":
                    crisis_weight = {
                        "moderate": 0.3,
                        "severe": 0.6, 
                        "critical": 1.0
                    }.get(pred.crisis_level, 0.0)
                    
                    total_crisis_score += crisis_weight
                    objects_in_crisis.append(obj_id)
        
        # 全体的な危機レベル判定
        if len(object_ids) > 0:
            avg_crisis = total_crisis_score / len(object_ids)
            if avg_crisis >= 0.7:
                overall_crisis = "critical"
            elif avg_crisis >= 0.4:
                overall_crisis = "severe"
            elif avg_crisis >= 0.15:
                overall_crisis = "moderate"
            else:
                overall_crisis = "none"
        else:
            overall_crisis = "none"
        
        return {
            "individual_predictions": predictions,
            "overall_crisis_level": overall_crisis,
            "total_crisis_score": total_crisis_score,
            "objects_in_crisis": objects_in_crisis,
            "cooperation_urgency": min(1.0, total_crisis_score * 0.8)
        }
    
    def detect_crisis_conditions(self, perceived_objects: Dict[str, ObjectInfo], 
                               current_time: int = 0) -> Dict[str, Any]:
        """危機状況の検出"""
        if not self.crisis_detection_enabled:
            return {"crisis_detected": False}
        
        # 知覚しているオブジェクトの未来予測
        object_ids = list(perceived_objects.keys())
        
        if not object_ids:
            return {"crisis_detected": False}
        
        multi_prediction = self.predict_multiple_futures(object_ids, perceived_objects, None, current_time)
        
        crisis_detected = multi_prediction["overall_crisis_level"] != "none"
        
        return {
            "crisis_detected": crisis_detected,
            "crisis_level": multi_prediction["overall_crisis_level"],
            "cooperation_urgency": multi_prediction["cooperation_urgency"],
            "objects_in_crisis": multi_prediction["objects_in_crisis"],
            "detailed_predictions": multi_prediction["individual_predictions"]
        }
    
    def _calculate_trend_modifier(self, object_id: str) -> float:
        """トレンド修正係数の計算"""
        if len(self.trend_memory) < 3:
            return 1.0
        
        # 最近の変化傾向を分析
        recent_changes = []
        for memory in list(self.trend_memory)[-3:]:
            if object_id in memory:
                recent_changes.append(memory[object_id])
        
        if len(recent_changes) >= 2:
            # 変化率の傾向
            change_trend = sum(recent_changes) / len(recent_changes)
            return max(0.5, min(2.0, 1.0 + change_trend * 0.3))
        
        return 1.0
    
    def _assess_crisis_level(self, predictions: List[float], object_type: str) -> str:
        """危機レベルの判定"""
        if not predictions:
            return "none"
        
        min_pred = min(predictions)
        
        # オブジェクトタイプに応じた危機判定
        crisis_thresholds = {
            "health": {"critical": 20, "severe": 40, "moderate": 60},
            "water": {"critical": 10, "severe": 30, "moderate": 50},
            "food": {"critical": 15, "severe": 35, "moderate": 55},
            "energy": {"critical": 25, "severe": 45, "moderate": 65},
            "danger": {"critical": 80, "severe": 60, "moderate": 40},  # 危険は逆転
            "threat": {"critical": 80, "severe": 60, "moderate": 40}   # 脅威も逆転
        }
        
        thresholds = crisis_thresholds.get(object_type, {"critical": 20, "severe": 40, "moderate": 60})
        
        if min_pred <= thresholds["critical"]:
            return "critical"
        elif min_pred <= thresholds["severe"]:
            return "severe"
        elif min_pred <= thresholds["moderate"]:
            return "moderate"
        else:
            return "none"
    
    def _calculate_prediction_confidence(self, obj: ObjectInfo, steps_ahead: int) -> float:
        """予測信頼度の計算"""
        base_confidence = self.prediction_accuracy
        
        # 予測期間が長いほど信頼度低下
        time_decay = 0.9 ** steps_ahead
        
        # オブジェクトの変動性による信頼度調整
        volatility_factor = 1.0 - (obj.volatility * 0.5)
        
        return max(0.1, min(1.0, base_confidence * time_decay * volatility_factor))
    
    def _cleanup_prediction_cache(self, current_time: int):
        """古い予測キャッシュをクリーンアップ"""
        # 10ステップより古いキャッシュを削除
        expired_keys = [
            key for key, value in self.prediction_cache.items()
            if current_time - value.timestamp > 10
        ]
        
        for key in expired_keys:
            del self.prediction_cache[key]
        
        # それでも多い場合は古い順に削除
        if len(self.prediction_cache) > 50:
            sorted_cache = sorted(
                self.prediction_cache.items(),
                key=lambda x: x[1].timestamp
            )
            
            # 古い半分を削除
            for key, _ in sorted_cache[:len(sorted_cache)//2]:
                del self.prediction_cache[key]
    
    def update_trend_memory(self, object_changes: Dict[str, float]):
        """トレンドメモリの更新"""
        self.trend_memory.append(object_changes.copy())
    
    def get_prediction_statistics(self) -> Dict[str, Any]:
        """予測統計の取得"""
        return {
            'cache_size': len(self.prediction_cache),
            'trend_memory_size': len(self.trend_memory),
            'prediction_horizon': self.prediction_horizon,
            'prediction_accuracy': self.prediction_accuracy,
            'crisis_detection_enabled': self.crisis_detection_enabled
        }