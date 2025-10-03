# SSD Core Engine Architecture Guidelines

## 🎯 Design Philosophy: SSD-Centric Architecture

This document establishes the fundamental design principles for integrating with ssd_core_engine.

### 📐 Core Principle

**ssd_core_engine is the architectural foundation. All surrounding code adapts TO it, never the reverse.**

```text
┌─────────────────────────────────────┐
│         ssd_core_engine/            │  ← FOUNDATION
│  ┌─────────────────────────────┐    │     (Preserve integrity)
│  │   Theoretical Framework     │    │
│  │ • Four-Layer Structure      │    │
│  │ • Meaning Pressure          │    │
│  │ • Alignment Processing      │    │
│  │ • Leap Mechanics           │    │
│  │ • Decision Systems          │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
            ↑ ADAPTS TO
┌─────────────────────────────────────┐
│        Surrounding Systems          │
│ • NPC Classes                       │
│ • Environment                       │
│ • Simulation Logic                  │
│ • Data Conversion Layers            │
└─────────────────────────────────────┘
```

### ✅ DO: Best Practices

1. **Preserve SSD Theoretical Integrity**
   - Never modify core SSD logic to fit external requirements
   - Maintain mathematical consistency in SSD equations
   - Respect four-layer structural hierarchy

2. **Create Adaptation Layers**
   - Build ObjectInfo conversion functions for external data
   - Create wrapper methods that translate between systems
   - Implement compatibility interfaces without touching SSD core

3. **Maximize SSD Utilization**
   - Use full SSD engine instances per NPC when possible
   - Leverage all available SSD features (prediction, crisis detection, etc.)
   - Prefer SSD decision-making over legacy algorithms

4. **Follow SSD Data Patterns**
   - Use SSD-compatible data types (ObjectInfo, LayerType, etc.)
   - Structure data flow to match SSD expectations
   - Implement proper SSD lifecycle (step, maintenance, etc.)

### ❌ DON'T: Anti-Patterns

1. **Never Modify SSD Core for Compatibility**
   ```python
   # ❌ Wrong - modifying SSD engine for external system
   def modified_ssd_step(self, legacy_data_format):
       # Converting SSD to fit legacy format
   
   # ✅ Right - adapting external system to SSD
   def convert_to_ssd_format(legacy_data):
       return [ObjectInfo(id=..., type=..., ...)]
   ```

2. **Don't Create Competing Decision Systems**
   - Avoid bypassing SSD decision-making with custom logic
   - Don't create parallel prediction systems
   - Don't override SSD results with external calculations

3. **Don't Break SSD Consistency**
   - Don't mix SSD and non-SSD state management
   - Don't ignore SSD maintenance requirements
   - Don't shortcut SSD initialization procedures

### 🔧 Integration Patterns

#### Pattern 1: NPC Integration
```python
class NPCWithSSD:
    def __init__(self, name):
        # Create dedicated SSD engine
        self.ssd_engine = create_ssd_engine(f"npc_{name}")
        setup_basic_structure(self.ssd_engine)
    
    def make_decision(self, situation):
        # Convert situation to SSD format
        objects = self._convert_to_ssd_objects(situation)
        
        # Use SSD decision-making
        result = self.ssd_engine.step(objects, available_actions)
        
        # Execute SSD decision
        return result['decision']['chosen_action']
```

#### Pattern 2: Environment Integration
```python
def environment_to_ssd(environment_data, npc_state):
    """Convert environment and NPC data to SSD ObjectInfo format"""
    return [
        ObjectInfo(
            id="health",
            type="health", 
            current_value=npc_state.health,
            decline_rate=calculate_decline_rate(npc_state),
            volatility=0.2,
            survival_relevance=1.0
        ),
        # ... more objects
    ]
```

### 📊 Integration Checklist

When adding new functionality:

- [ ] Does it preserve SSD theoretical consistency?
- [ ] Does it adapt TO ssd_core_engine rather than modifying it?
- [ ] Does it maximize utilization of SSD features?
- [ ] Does it follow SSD data patterns and lifecycle?
- [ ] Does it avoid creating competing decision systems?
- [ ] Does it maintain clear separation between SSD core and adaptation layers?

### 🎖️ Success Metrics

A well-integrated system should achieve:

- **100% SSD Feature Utilization**: All available SSD capabilities are used
- **Zero Core Modifications**: No changes to ssd_core_engine for compatibility
- **Clean Separation**: Clear boundaries between SSD core and adaptation layers
- **Theoretical Consistency**: All SSD mathematical relationships preserved

This architecture ensures maximum benefit from SSD's advanced AI capabilities while maintaining system reliability and theoretical coherence.