"""
SSD Package Initialization
構造主観力学パッケージの初期化
"""

try:
    from .ssd_types import (
        LayerType, ObjectInfo, StructuralState, AlignmentResult,
        LeapResult, DecisionInfo, PredictionResult, SystemState
    )

    from .ssd_meaning_pressure import MeaningPressureProcessor
    from .ssd_alignment_leap import AlignmentProcessor, LeapProcessor
    from .ssd_decision import DecisionSystem, ActionEvaluator
    from .ssd_prediction import PredictionSystem
    from .ssd_utils import (
        SystemMonitor, MaintenanceManager,
        create_simple_world_objects, create_survival_scenario_objects
    )
    from .ssd_engine import SSDCoreEngine, create_ssd_engine, setup_basic_structure
    
    # Territory System
    try:
        from .ssd_territory import TerritoryProcessor, TerritoryInfo, SubjectiveBoundary
        TERRITORY_AVAILABLE = True
    except ImportError:
        TERRITORY_AVAILABLE = False
        
except ImportError:
    # 直接実行時のフォールバック
    from .ssd_types import (
        LayerType, ObjectInfo, StructuralState, AlignmentResult, 
        LeapResult, DecisionInfo, PredictionResult, SystemState
    )
    
    from .ssd_meaning_pressure import MeaningPressureProcessor
    from .ssd_alignment_leap import AlignmentProcessor, LeapProcessor
    from .ssd_decision import DecisionSystem, ActionEvaluator
    from .ssd_prediction import PredictionSystem
    from .ssd_utils import (
        SystemMonitor, MaintenanceManager,
        create_simple_world_objects, create_survival_scenario_objects
    )
    from .ssd_engine import SSDCoreEngine, create_ssd_engine, setup_basic_structure

__version__ = "1.0.0"
__author__ = "SSD Theory Implementation"

# パッケージレベルのエクスポート
__all__ = [
    # Core Types
    'LayerType', 'ObjectInfo', 'StructuralState', 'AlignmentResult',
    'LeapResult', 'DecisionInfo', 'PredictionResult', 'SystemState',

    # Core Processors
    'MeaningPressureProcessor', 'AlignmentProcessor', 'LeapProcessor',
    'DecisionSystem', 'ActionEvaluator', 'PredictionSystem',

    # Utilities
    'SystemMonitor', 'MaintenanceManager',
    'create_simple_world_objects', 'create_survival_scenario_objects',

    # Main Engine
    'SSDCoreEngine', 'create_ssd_engine', 'setup_basic_structure'
]

# Territory System (条件付きエクスポート)
if TERRITORY_AVAILABLE:
    __all__.extend(['TerritoryProcessor', 'TerritoryInfo', 'SubjectiveBoundary'])