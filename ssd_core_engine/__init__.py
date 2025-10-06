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
    
    # Subjective Boundary System (Hermann Degner理論統合版)
    try:
        from .ssd_subjective_boundary import (
            SubjectiveBoundaryProcessor, 
            SubjectiveBoundaryInfo, 
            SubjectiveBoundary,
            # 後方互換性エイリアス
            TerritoryProcessor,
            TerritoryInfo
        )
        SUBJECTIVE_BOUNDARY_AVAILABLE = True
        TERRITORY_AVAILABLE = True  # 後方互換性
    except ImportError:
        # 従来システムへのフォールバック
        try:
            from .ssd_territory import TerritoryProcessor, TerritoryInfo, SubjectiveBoundary
            SubjectiveBoundaryProcessor = TerritoryProcessor
            SubjectiveBoundaryInfo = TerritoryInfo
            TERRITORY_AVAILABLE = True
            SUBJECTIVE_BOUNDARY_AVAILABLE = False
        except ImportError:
            TERRITORY_AVAILABLE = False
            SUBJECTIVE_BOUNDARY_AVAILABLE = False
    
    # 🚀 Hermann Degner理論の完全実装 - 拡張機能
    try:
        from .ssd_enhanced_leap import (
            ChaoticLeapProcessor, StructuralTheoria, NarrativeSphereDepthModel,
            LeapType, LeapEvent
        )
        ENHANCED_SSD_AVAILABLE = True
    except ImportError:
        ENHANCED_SSD_AVAILABLE = False
        
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

# Subjective Boundary System (Hermann Degner理論統合版・条件付きエクスポート)
if SUBJECTIVE_BOUNDARY_AVAILABLE:
    __all__.extend([
        'SubjectiveBoundaryProcessor', 
        'SubjectiveBoundaryInfo', 
        'SubjectiveBoundary',
        # 後方互換性エイリアス
        'TerritoryProcessor', 
        'TerritoryInfo'
    ])
elif TERRITORY_AVAILABLE:
    __all__.extend(['TerritoryProcessor', 'TerritoryInfo', 'SubjectiveBoundary'])

# 🚀 Hermann Degner理論拡張機能 (条件付きエクスポート)
if ENHANCED_SSD_AVAILABLE:
    __all__.extend([
        'ChaoticLeapProcessor', 'StructuralTheoria', 'NarrativeSphereDepthModel',
        'LeapType', 'LeapEvent'
    ])

# パッケージ情報
SSD_THEORY_URL = "https://github.com/HermannDegner/Structural-Subjectivity-Dynamics"
ENHANCED_FEATURES = ENHANCED_SSD_AVAILABLE