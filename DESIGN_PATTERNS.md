# SWRL Translator Design Pattern

## Overview

This implementation uses a combination of design patterns to handle two similar but different SWRL translation approaches:

1. **Abstract Base Class (ABC)** - `SWRLTranslator`
2. **Strategy Pattern** - Different translation strategies (Graph vs Embeddings)
3. **Factory Pattern** - `SWRLTranslatorFactory` creates the right instance
4. **Template Method Pattern** - Common `generate_swrl()` with customizable steps

## Architecture

```
SWRLTranslator (ABC)
├── generate_swrl() - Common implementation
├── get_context() - Abstract (must implement)
└── _get_prompt_template() - Abstract (must implement)

GraphRAGTranslator (Concrete)
├── Requires: OntologyAnalyzer
├── get_context() - Uses ontology classes + Graph RAG
└── _get_prompt_template() - ChatPromptTemplate

EmbeddingsRAGTranslator (Concrete)
├── Requires: Only RAG engine
├── get_context() - Uses embeddings RAG
└── _get_prompt_template() - PromptTemplate

SWRLTranslatorFactory
└── create() - Returns appropriate translator based on type
```

## Benefits

### 1. **Single Responsibility**
Each class has one reason to change:
- `GraphRAGTranslator` - Changes to graph-based translation
- `EmbeddingsRAGTranslator` - Changes to embeddings-based translation
- `SWRLTranslatorFactory` - Changes to instantiation logic

### 2. **Open/Closed Principle**
Open for extension, closed for modification:
- Add new translator types without modifying existing code
- Just create a new subclass of `SWRLTranslator`

### 3. **Dependency Inversion**
Depend on abstractions, not concrete classes:
- Main code depends on `SWRLTranslator` interface
- Factory handles concrete instantiation

### 4. **Easy Configuration**
Switch between strategies via config:
```python
# Use embeddings approach
config = TranslatorConfig(translator_type="embeddings")

# Use graph approach
config = TranslatorConfig(translator_type="graph")
```

## Usage Examples

### Basic Usage

```python
from swrl_translator import SWRLTranslatorFactory
from config import EMBEDDINGS_CONFIG

# Setup your RAG engine
rag_engine = setup_rag_engine(EMBEDDINGS_CONFIG)

# Create translator via factory
translator = SWRLTranslatorFactory.create(
    translator_type="embeddings",
    model_name="llama",
    temperature=0.0,
    rag_engine=rag_engine
)

# Generate SWRL
translator.generate_swrl("If a patient has fever, then alert doctor")
```

### With Configuration

```python
from config import TranslatorConfig

config = TranslatorConfig(
    translator_type="embeddings",
    model_name="llama",
    rules_category="PARKINSON"
)

translator = SWRLTranslatorFactory.create(
    translator_type=config.translator_type,
    model_name=config.model_name,
    temperature=config.temperature,
    rag_engine=rag_engine
)
```

### Adding a New Translator Type

```python
class HybridRAGTranslator(SWRLTranslator):
    """Combines both graph and embeddings"""
    
    def __init__(self, model_name, temperature, 
                 ontology_analyzer, graph_rag, embeddings_rag, mode="LOCAL"):
        super().__init__(model_name, temperature, embeddings_rag, mode)
        self.ontology_analyzer = ontology_analyzer
        self.graph_rag = graph_rag
    
    def get_context(self, rule_in_nl: str) -> str:
        # Combine both approaches
        graph_context = self.graph_rag.get_entities(...)
        embeddings_context = self.rag_engine.get_entities(...)
        return f"{graph_context}\n\n{embeddings_context}"
    
    def _get_prompt_template(self):
        return ChatPromptTemplate.from_template(CustomPromptTemplates.hybrid_prompt)
```

Then update the factory:

```python
# In SWRLTranslatorFactory.create()
elif translator_type == "hybrid":
    return HybridRAGTranslator(...)
```

## Migration Path

### Current Code
```python
# Old way - tightly coupled
app = NL2SWRL(model_name="llama", temperature=0.0, rag_engine=embeddings_rag_engine)
# or
app = SLM4SWRL(model_name="llama", temperature=0.0, ontology_analyser=analyzer, rag_engine=graph_rag_engine)
```

### New Code
```python
# New way - flexible and configurable
translator = SWRLTranslatorFactory.create(
    translator_type="embeddings",  # or "graph"
    model_name="llama",
    temperature=0.0,
    rag_engine=rag_engine,
    ontology_analyzer=analyzer  # Only for graph type
)
```

## Files Created

1. **`swrl_translator.py`** - Abstract base class, concrete implementations, factory
2. **`config.py`** - Configuration dataclass with presets
3. **`main_refactored.py`** - Example usage with factory pattern

## Next Steps

1. Test the new implementation
2. Gradually migrate from `NL2SWRL` and `SLM4SWRL` to the new classes
3. Add unit tests for each translator type
4. Add configuration file support (YAML/JSON)
5. Consider adding logging and monitoring

## Alternative Patterns Considered

### Builder Pattern
Good for complex object construction, but overkill here since we have simple initialization.

### Singleton Pattern
Not suitable - we may want multiple translators with different configs.

### Adapter Pattern
Could wrap existing classes, but refactoring is cleaner long-term.

## Best Practices

1. **Use the factory** - Don't instantiate translators directly
2. **Configure via config objects** - Avoid scattered parameters
3. **Keep abstractions stable** - Changes to `SWRLTranslator` affect all subclasses
4. **Test each strategy independently** - Unit test each translator type
5. **Document requirements** - Each translator documents its dependencies
