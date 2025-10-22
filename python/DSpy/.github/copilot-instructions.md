# DSPy Copilot Instructions

## Overview
DSPy is a framework for programmatically optimizing language model (LM) prompts and weights. It decouples the specification of your problem from its optimization, treating your program as a modular computational graph that can be improved through compilation.

**Key Concept**: DSPy separates *program definition* (what you want to do) from *program optimization* (how the LM solves it).

## Architecture Overview

### Core Components

1. **Modules** (`dspy/primitives/`): The building blocks of DSPy programs
   - `Module`: Base class for all DSPy programs. All DSPy modules inherit from this.
   - `BaseModule`: Lower-level interface with `named_parameters()` and `named_sub_modules()` for introspection
   - Modules use `forward()` (sync) and `aforward()` (async) methods; called via `__call__()` or `acall()`

# Modules (implementation)
# - Language: Python modules (.py files or packages) that implement the behavior declared by a signature.
# - Purpose: implement the runtime behavior of a declared contract (signature) and expose a small, well-known API.
# - Conventions:
#     * Module entrypoint should follow a simple API (for example: a function `run(inputs: dict, params: dict) -> dict`
#       or a `dspy.Module` subclass implementing `forward()`/`aforward()`).
#     * Call `super().__init__()` when subclassing dspy.Module so metaclass initialization runs.
#     * Store predictors and other trainable components as attributes so they are discoverable via introspection.
#     * The keys in inputs/params/outputs must match names declared in the corresponding signature.
#     * Modules should validate inputs (types, required fields) before processing.
# - Organization: keep implementation logic in Python, keep declarative surface (I/O spec) in signature files (TOML or Signature classes).
# - Integration: a loader reads the signature, validates/coerces incoming data, then calls the module's run/forward function.
#
# Example module (Python)
# def run(inputs: dict, params: dict) -> dict:
#     """
#     inputs: {'image': '/path/to/input.png'}
#     params: {'width': 800, 'height': 600}
#     returns: {'resized_image': '/path/to/output.png'}
#     """
#     # 1) validate inputs against signature (types, required)
#     # 2) perform processing
#     # 3) return outputs keyed by signature output names
#     return {'resized_image': '/path/to/output.png'}
#
# Example Module Class Pattern (dspy.Module)
# class MyProgram(dspy.Module):
#     def __init__(self):
#         super().__init__()
#         # Initialize predictors with signatures
#         self.classify = dspy.ChainOfThought("text -> sentiment: bool")
#         self.explain = dspy.Predict("sentiment, text -> explanation")
#
#     def forward(self, text):
#         sentiment = self.classify(text=text)
#         explanation = self.explain(sentiment=sentiment.sentiment, text=text)
#         return explanation
#
# Notes & best practices for modules
# - Keep business logic in Python and minimal glue in signatures.
# - Use dspy's introspection (named_parameters(), named_sub_modules()) for optimizers.
# - Validate inputs early and return outputs keyed by signature names.
# - When adding async behavior implement aforward() and use acall() for invocation.

# Signatures (dspy/signatures/)
# - Purpose: declarative specs that describe a module's inputs, outputs, parameters and metadata.
# - Preferred file format for external declarative specs: TOML files (*.toml). TOML is human-friendly and maps well to typed fields.
#   JSON or YAML are acceptable alternatives if your toolchain prefers them, but examples below use TOML for clarity.
# - In-code signature forms: string specifications or Signature subclasses (class form) for stronger typing and documentation.
# - Typical fields for TOML signature files:
#     [meta]                 -> name, version, description, tags, author, etc.
#     [[inputs]]             -> repeated table for each input: name, type, description, required, default
#     [[params]]             -> repeated table for configuration parameters: name, type, default, description
#     [[outputs]]            -> repeated table for each output: name, type, description
# - Types: prefer simple primitive types (string, int, float, bool, file, array, object). Be explicit about units/format.
# - Intended use: validation, UI generation, wiring modules together, documentation and runtime type checking.
#
# String form vs Class form (paired explanation + example)
# - String form: compact inline specification, useful for quick prototypes.
#     Example:
#         dspy.Predict("query -> answer")
#
# - Class form: subclass dspy.Signature to provide typed fields, descriptions and richer metadata.
#     Example:
#         class QASignature(dspy.Signature):
#             """Answer questions about the context."""
#             query: str = dspy.InputField(desc="The question to answer")
#             answer: str = dspy.OutputField(desc="The answer", prefix="Answer:")
#
# - Conversion helper: use ensure_signature() to convert either a string or class into a canonical Signature object
#   before use by predictors or modules.
#
# Example signature (TOML)
# [meta]
# name = "resize_image"
# version = "0.1"
# description = "Resize an image to the requested width and height"
#
# [[inputs]]
# name = "image"
# type = "file"
# description = "Path to input image"
# required = true
#
# [[params]]
# name = "width"
# type = "int"
# default = 800
# description = "Target width in pixels"
#
# [[params]]
# name = "height"
# type = "int"
# default = 600
# description = "Target height in pixels"
#
# [[outputs]]
# name = "resized_image"
# type = "file"
# description = "Path to the resized output image"
#
# Notes & best practices for signatures
# - Keep signatures stable and bump version in [meta] when making breaking changes.
# - Prefer TOML for readability and explicit typing; use JSON for strict tooling and YAML when comments/multi-docs are needed.
# - Automate validation: load TOML with toml/tomli and assert presence/types of fields before calling module code.
# - Use clear descriptions and examples within signatures to help UI generators and integrators.
2. **Signatures** (`dspy/signatures/`): Declarative specs defining module I/O
   - String form: `"input1, input2 -> output1: type"`
   - Class form: Subclass with `InputField`/`OutputField` attributes
   - `ensure_signature()`: Convert string or class to Signature type
   - Field descriptors add context: `InputField(desc="...")`, `OutputField(prefix="...")`

3. **Predictors** (`dspy/predict/`): Modules that call LMs
   - `Predict`: Basic predictor; stores demos, instructions, and LM calls
   - `ChainOfThought`: Prepends reasoning field for step-by-step thinking
   - `ReAct`, `CodeAct`: Agent-style modules with tool use
   - `ProgramOfThought`: Generates Python code for execution
   - All inherit from `Module` and `Parameter` (for optimization)

4. **Language Models** (`dspy/clients/lm.py`)
   - `LM`: Unified interface to LiteLLM (supports 100+ models)
   - Configure globally: `dspy.settings.configure(lm=dspy.LM("openai/gpt-4"))`
   - Supports caching, retries, callbacks, usage tracking
   - Models require format `"provider/model"` (e.g., `"openai/gpt-4o"`)

5. **Teleprompters/Optimizers** (`dspy/teleprompt/`): Compilation engines
   - `Teleprompter`: Base class defining `compile(student, trainset, ...)` interface
   - `BootstrapFewShot`, `BootstrapRS`: Few-shot demo selection
   - `MIPROv2`: Multi-task instruction + prompt + in-context learning optimization
   - `SignatureOptimizer`: Optimizes instruction text
   - Optimize programs by: selecting demos, tuning instructions, adjusting hyperparams

6. **Data Primitives** (`dspy/primitives/`)
   - `Example`: Dict-like container for input/output data. Supports attribute access: `example.input_field`
   - `Prediction`: Subclass of Example; holds LM outputs + optional completions (for beam search)
   - Predictions support score comparisons: `pred1 < pred2` compares `score` fields

### Data Flow

```
User Program (Module)
    ↓
[Input: Example or kwargs]
    ↓
Predict/ChainOfThought/etc (calls forward())
    ↓
LM Call (via dspy.settings.lm or module's lm attribute)
    ↓
Output: Prediction (Example subclass with LM outputs)
    ↓
Compilation: Optimizer trains demos/instructions on trainset
    ↓
Optimized Module with adjusted signatures, demos, configs
```

## Critical Developer Patterns

### 1. Module Definition Pattern
Always inherit from `dspy.Module` and implement `forward()`:

```python
class MyProgram(dspy.Module):
    def __init__(self):
        super().__init__()
        # Initialize predictors with signatures
        self.classify = dspy.ChainOfThought("text -> sentiment: bool")
        self.explain = dspy.Predict("sentiment, text -> explanation")

    def forward(self, text):
        sentiment = self.classify(text=text)
        explanation = self.explain(sentiment=sentiment.sentiment, text=text)
        return explanation
```

**Key points:**
- Call `super().__init__()` (metaclass `ProgramMeta` injects `_base_init()`)
- Store predictors as attributes for `named_parameters()` discovery
- `forward()` receives kwargs matching signature input fields
- Return `Prediction` or dict (auto-converted)
- Use `aforward()` for async execution

### 2. Signature Definition Pattern

**What it does**: A signature is like a function contract—it defines what information your module expects as input and what it will produce as output. The language model sees this contract and follows it when generating responses.

Think of it like a restaurant menu: the inputs are what you order, the outputs are what you get. The LM uses this specification to format its responses correctly.

```python
# String form (simplest) - good for quick prototypes
dspy.Predict("query -> answer")

# Class form (for complex types) - better for production with rich documentation
class QASignature(dspy.Signature):
    """Answer questions about the context."""
    query: str = dspy.InputField(desc="The question to answer")
    answer: str = dspy.OutputField(desc="The answer", prefix="Answer:")

dspy.ChainOfThought(QASignature)

# Dynamic construction with custom types
sig = dspy.Signature("input: CustomType -> output: str", custom_types={"CustomType": CustomType})
```

**Key points:**
- `InputField` vs `OutputField` distinguish I/O
- Descriptions improve LM understanding
- Prefixes/suffixes control prompt formatting
- Types can be custom Pydantic models or built-ins
- Use `ensure_signature()` when converting unknowns

### 3. Settings and Configuration Pattern

**What it does**: DSPy is like an orchestra where the language model is the conductor. Settings let you configure which conductor (LM) and what tempo (temperature), how many musicians play at once (threads), and whether to remember past performances (caching). You can set these globally or temporarily override them for specific moments.

```python
import dspy

# Configure globally (persists until next configure() call)
dspy.settings.configure(
    lm=dspy.LM("openai/gpt-4o", cache=True, temperature=0.7),
    num_threads=4,
    track_usage=True,  # Enable token counting
)

# Temporary overrides via context manager
with dspy.settings.context(lm=dspy.LM("anthropic/claude-3-opus")):
    output = program(input_data)

# Access settings
current_lm = dspy.settings.lm
```

**Key points:**
- `dspy.settings.configure()` is the main entry point
- Use `context()` for temporary overrides (e.g., testing with cheaper model)
- `track_usage=True` enables `prediction.get_lm_usage()` for billing/analysis
- Settings are thread-local via `thread_local_overrides`

### 4. Compilation/Optimization Pattern

**What it does**: Compilation is like taking an untrained student (your module) and tutoring them with examples and feedback until they get better. You provide training examples, define what "good" means with a metric, and an optimizer learns the best prompts and examples to include in your module.

```python
from dspy.teleprompt import BootstrapFewShot

# Define metric function
def metric(example, prediction, trace=None):
    """Return float score: higher = better."""
    return float(prediction.answer.lower() == example.answer.lower())

# Create optimizer
optimizer = BootstrapFewShot(metric_fn=metric, max_bootstrapped_demos=3)

# Compile (freezes module as "trained")
compiled_program = optimizer.compile(
    student=program,
    trainset=train_examples,  # list[Example]
    teacher=None,  # optional teacher program for few-shot
    valset=val_examples,  # optional validation set
)

# Compiled modules have _compiled=True (frozen from further updates)
assert compiled_program._compiled
```

**Key points:**
- Metrics must return float; higher = better
- Signature is `metric(example, prediction, trace=None)` or with `pred_name` params for component selection
- Teleprompters store optimal demos/instructions in module's predictors
- Compiled modules are saved/loaded with `module.save(path)` and `dspy.load(path)`

### 5. Async Execution Pattern

**What it does**: Async execution lets you run multiple language model calls at the same time instead of waiting for each one to finish. Think of it like a restaurant with multiple kitchen stations working simultaneously—instead of one chef completing each dish before starting the next, multiple chefs work on different dishes in parallel.

```python
class AsyncProgram(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.ChainOfThought("query -> answer")

    async def aforward(self, query):
        # Concurrent LM calls
        result = await self.predict.acall(query=query)
        return result

# Call async method
import asyncio
output = asyncio.run(program.acall(query="What is 2+2?"))
```

**Key points:**
- Use `acall()` to invoke async modules (returns awaitable)
- `aforward()` is called by `acall()` (mirrors `forward()`/`__call__()`)
- DSPy uses `asyncer` for async-to-sync conversion internally

### 6. Introspection Pattern

**What it does**: Introspection is like opening up your module to see which parts are trainable and need optimization. Instead of treating your module as a black box, you can peek inside to discover all the predictors, sub-modules, and parameters that the optimizer can tune. It's like examining a car engine to identify which parts need adjustment.

```python
# Find all parameters (Predict instances) that can be optimized
for name, param in program.named_parameters():
    print(f"Parameter: {name}")
    if hasattr(param, 'demos'):
        print(f"  Demos: {param.demos}")
    if hasattr(param, 'signature'):
        print(f"  Signature: {param.signature}")

# Find sub-modules
for name, submodule in program.named_sub_modules():
    print(f"Submodule: {name} ({type(submodule).__name__})")

# Access predictor by name
for name, pred in program.named_predictors():
    print(f"Predictor: {name}")
```

**Key points:**
- `named_parameters()` finds `Parameter` instances (Predict, ChainOfThought, etc.)
- Respects `_compiled=True` flag to skip optimization of pre-trained modules
- `named_sub_modules()` finds all nested `Module` instances
- Used by optimizers to selectively train components

## Project-Specific Conventions

### Testing Conventions
- Test marks: `@pytest.mark.llm_call`, `@pytest.mark.extra`, `@pytest.mark.reliability`
- Skip marked tests by default; run with `--llm_call`, `--extra`, `--reliability` flags
- Use `lm_for_test` fixture for mock LM in tests
- `conftest.py` auto-clears settings after each test (idempotency)
- Coverage excludes `tests/reliability/` (stress tests)

### Code Organization
- `dspy/predict/`: All predictor modules (Predict, ChainOfThought, ReAct, etc.)
- `dspy/signatures/`: Signature classes and field definitions
- `dspy/primitives/`: Core data structures (Module, Example, Prediction)
- `dspy/teleprompt/`: Optimization engines (Teleprompter subclasses)
- `dspy/clients/`: LM interfaces (LM, OpenAI, Anthropic, local models)
- `dspy/adapters/`: Format converters (JSON, XML, Chat adapters)
- `dspy/evaluate/`: Evaluation utilities and metrics
- `dspy/dsp/`: Legacy DSP compatibility (ColBERTv2, retrieval)

### Import Pattern
Main exports via `dspy/__init__.py`:
```python
import dspy

# Common usage
dspy.Module, dspy.Predict, dspy.ChainOfThought
dspy.Signature, dspy.InputField, dspy.OutputField
dspy.Example, dspy.Prediction
dspy.LM, dspy.settings, dspy.settings.configure
dspy.load, dspy.track_usage, dspy.asyncify
# Optimizers
dspy.BootstrapFewShot, dspy.MIPROv2, dspy.SignatureOptimizer
```

### 7. Callback Pattern

**What it does**: Callbacks are hooks that let you intercept and observe what's happening during LM calls. Think of them like a supervisor watching each step of production—you can log when calls start, what parameters they're using, and what results come back. This is useful for debugging, monitoring, or collecting data about your module's behavior.

```python
from dspy.utils.callback import BaseCallback

class MyCallback(BaseCallback):
    def on_predict_start(self, **kwargs):
        print(f"LM call starting: {kwargs}")

    def on_predict_end(self, **kwargs):
        print(f"LM call ended: {kwargs}")

# Attach to module
program.callbacks.append(MyCallback())

# Or pass to LM
dspy.settings.configure(lm=dspy.LM(..., callbacks=[MyCallback()]))
```

**Key points:**
- Callbacks inherit from `BaseCallback` and override lifecycle hooks
- `on_predict_start` fires before LM call; `on_predict_end` fires after
- Can attach callbacks to individual modules or globally via settings
- Useful for logging, tracing, and debugging

### 8. Caching Pattern

**What it does**: Caching saves LM API responses so that identical requests don't need to call the LM again. Think of it like keeping a library of recipes you've already made—if someone asks for the same recipe again, you pull it from your notebook instead of making the dish from scratch. This saves time and money.

```python
# Enabled by default with persistent storage
dspy.settings.configure(
    lm=dspy.LM("openai/gpt-4o-mini", cache=True)
)

# Caching respects model, prompt, temperature, max_tokens, and other parameters
# so different configurations don't share cached results

# Use rollout_id to partition cache (useful for reinforcement learning experiments)
with dspy.settings.context(rollout_id="experiment_v1"):
    result = program(input_data)
```

**Key points:**
- Enabled by default in `dspy.LM(..., cache=True)`
- Uses `diskcache` for persistent caching across runs
- Cache key includes: model, prompt, temperature, max_tokens, etc.
- Respects `rollout_id` parameter to partition cache entries (useful for RL)
- Cache location configurable via settings

## Common Implementation Tasks

### Adding a New Predictor Module
1. Inherit from `Module` and optionally `Parameter`
2. Accept signature + config in `__init__`
3. Use `ensure_signature()` to normalize input
4. Optionally modify signature (e.g., ChainOfThought prepends reasoning field)
5. Create internal `Predict` instance with modified signature
6. Implement `forward()` to delegate to internal predictor
7. Implement `aforward()` if async support needed
8. Export in `dspy/predict/__init__.py`

**Example from codebase** (see `dspy/predict/chain_of_thought.py`):
```python
class ChainOfThought(Module):
    def __init__(self, signature: str | type[Signature], **config):
        super().__init__()
        signature = ensure_signature(signature)
        rationale_field = dspy.OutputField(prefix="Reasoning: Let's think step by step")
        extended_signature = signature.prepend(name="reasoning", field=rationale_field)
        self.predict = dspy.Predict(extended_signature, **config)

    def forward(self, **kwargs):
        return self.predict(**kwargs)
```

### Adding an Optimizer

**What it does**: An optimizer is a tool that learns the best way to tune your program for better performance. Instead of you manually tweaking prompts and examples, the optimizer takes training data and automatically adjusts your module's internal settings (demos, instructions, configs) to improve how well it performs on the metric you define. It's like an automated tuning system that runs experiments and keeps what works best.

**Implementation steps**:
1. Subclass `Teleprompter`
2. Implement `compile(student, trainset, teacher=None, valset=None, **kwargs)`
3. Use `student.named_parameters()` to get trainable components
4. Update demos/instructions/configs on parameters
5. Call `student.save(path)` internally if checkpointing needed
6. Return optimized student module
7. Export in `dspy/teleprompt/__init__.py`

**Example workflow**:
```python
from dspy.teleprompt import BootstrapFewShot

# Define evaluation metric (higher = better)
def metric(example, prediction, trace=None):
    return example.answer.lower() == prediction.answer.lower()

# Create and compile with training data
optimizer = BootstrapFewShot(metric_fn=metric, max_bootstrapped_demos=3)
optimized_program = optimizer.compile(
    student=program,
    trainset=train_examples,
    teacher=teacher_program,  # Optional: use stronger model for bootstrapping
    valset=val_examples
)

# Inspect optimized prompts
dspy.inspect_history()
```

### Extending Signatures

**What it does**: Signatures can be modified dynamically to add new fields or change their properties. Think of it like taking an existing form and adding new sections or changing instructions—you can prepend questions at the top, append fields at the bottom, or override existing ones. This is useful when you want to adapt a signature for a specialized use case without rewriting everything from scratch.

```python
# Append new output field
extended_sig = signature.append(name="confidence", field=dspy.OutputField(desc="confidence score"))

# Prepend new input field
extended_sig = signature.prepend(name="context", field=dspy.InputField(desc="background info"))

# Use with custom types
custom_types = {"CustomType": MyDataClass}
sig = dspy.Signature("input: CustomType -> output: str", custom_types=custom_types)

# Verify and normalize
sig = dspy.ensure_signature(sig)
```

**Key points:**
- Use `.append()`, `.prepend()` to modify signatures dynamically
- Pass custom types via `custom_types` dict
- Define fields with `.annotation`, `.prefix`, `.desc` for control
- Test with `ensure_signature()` for compatibility

## Debugging Tips

1. **Enable logging**: `dspy.enable_logging()` or set `logging.basicConfig(level=logging.DEBUG)`
2. **Inspect module history**: `program.history` contains all LM calls with inputs/outputs
3. **Check settings**: `dspy.settings.lm`, `dspy.settings.num_threads`, etc.
4. **Use dummy LM for testing**: Create mock LM with fake responses to avoid API costs
5. **Trace execution**: Use callbacks with `on_predict_start`/`on_predict_end` hooks
6. **Inspect Predictions**: Access `prediction._completions` for beam search results; `prediction.get_lm_usage()` for tokens

## Critical Integration Points

- **LiteLLM**: All LM calls route through `dspy.clients.lm.LM`, which uses litellm library for 100+ model support
- **Pydantic**: Signatures use Pydantic BaseModel for validation and field definitions
- **Optuna**: MIPROv2 and other optimizers use Optuna for hyperparameter tuning
- **Asyncer**: Provides `asyncify()` / `syncify()` for async-to-sync adaptation
- **Diskcache**: Persistent request caching across runs
