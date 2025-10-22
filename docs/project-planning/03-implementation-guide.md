# Implementation Guide: Conversation History Tutorial

## Document Information
- **Version:** 1.0
- **Date:** 2025-10-22
- **Target Audience:** Developers implementing the tutorial
- **Estimated Time:** 40-60 hours

---

## 1. Getting Started

### 1.1 Prerequisites

Before starting implementation, ensure you have:

- [ ] Python 3.10+ installed
- [ ] Git configured
- [ ] DSPy repository cloned
- [ ] Development environment set up
- [ ] OpenAI API key or alternative LM access
- [ ] Familiarity with DSPy basics
- [ ] Pre-commit hooks installed

### 1.2 Environment Setup

```bash
# Clone repository
git clone https://github.com/stanfordnlp/dspy.git
cd dspy

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Set up environment variables
export OPENAI_API_KEY=your-api-key-here
```

### 1.3 Project Structure

Create the following directory structure:

```
docs/docs/tutorials/conversation_history/
├── index.md                          # Main tutorial
├── examples/
│   ├── basic_conversation.py        # Basic example
│   ├── advanced_conversation.py     # Advanced example
│   ├── conversation_manager.py      # Helper class
│   └── config_example.json          # Sample config
├── tests/
│   ├── __init__.py
│   ├── test_conversation.py         # Unit tests
│   ├── test_history.py              # History tests
│   └── test_integration.py          # Integration tests
└── assets/
    ├── conversation_flow.png        # Diagram
    └── screenshot.png               # Demo screenshot
```

---

## 2. Implementation Phases

### Phase 1: Basic Implementation (Days 1-3)

#### Step 1.1: Create Basic Example File

**File:** `examples/basic_conversation.py`

```python
"""
Basic Conversation History Example
===================================

This example demonstrates a simple conversational AI system using DSPy
with history management.

Usage:
    python basic_conversation.py
    
Requirements:
    - OPENAI_API_KEY environment variable set
    - dspy package installed
"""

import os
import dspy


def main():
    """Run basic conversation example."""
    
    # Step 1: Configure the language model
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable not set. "
            "Please set it with your OpenAI API key."
        )
    
    lm = dspy.LM("openai/gpt-4o-mini", api_key=api_key)
    dspy.settings.configure(lm=lm)
    
    # Step 2: Define the signature
    class QA(dspy.Signature):
        """Question-answering with conversation history."""
        question: str = dspy.InputField()
        history: dspy.History = dspy.InputField()
        answer: str = dspy.OutputField()
    
    # Step 3: Create predictor
    predict = dspy.Predict(QA)
    
    # Step 4: Initialize history
    history = dspy.History(messages=[])
    
    # Step 5: Conversation loop
    print("Conversation started. Type 'finish' to end.\n")
    
    while True:
        # Get user input
        question = input("You: ").strip()
        
        # Check for exit command
        if question.lower() == "finish":
            print("\nConversation ended.")
            break
        
        # Skip empty inputs
        if not question:
            print("Please enter a question.\n")
            continue
        
        try:
            # Make prediction
            result = predict(question=question, history=history)
            
            # Display response
            print(f"\nAI: {result.answer}\n")
            
            # Update history
            history.messages.append({
                "question": question,
                "answer": result.answer
            })
            
        except Exception as e:
            print(f"\nError: {e}\n")
            continue
    
    # Display conversation summary
    print(f"\nTotal turns: {len(history.messages)}")


if __name__ == "__main__":
    main()
```

**Implementation Checklist:**
- [ ] Create file
- [ ] Add imports
- [ ] Implement main function
- [ ] Add error handling
- [ ] Test with OpenAI API
- [ ] Add docstring
- [ ] Run linter

#### Step 1.2: Test Basic Example

```bash
# Run the example
python examples/basic_conversation.py

# Test conversation
# - Ask a simple question
# - Ask a follow-up question that requires context
# - Verify context is maintained
# - Type 'finish' to exit
```

#### Step 1.3: Create Unit Tests

**File:** `tests/test_conversation.py`

```python
"""Unit tests for conversation functionality."""

import pytest
import dspy
from unittest.mock import Mock, patch


class TestQASignature:
    """Tests for QA signature."""
    
    def test_signature_has_required_fields(self):
        """Verify QA signature has question, history, and answer fields."""
        from examples.basic_conversation import QA
        
        # Check input fields
        assert hasattr(QA, "__annotations__")
        assert "question" in QA.__annotations__
        assert "history" in QA.__annotations__
        assert "answer" in QA.__annotations__
    
    def test_signature_field_types(self):
        """Verify field types are correct."""
        from examples.basic_conversation import QA
        
        # This test assumes we can inspect the signature
        # Adjust based on actual DSPy API
        pass


class TestConversation:
    """Tests for conversation logic."""
    
    @pytest.fixture
    def mock_lm(self):
        """Create a mock language model."""
        with patch('dspy.LM') as mock:
            yield mock
    
    def test_empty_history_initialization(self):
        """Test that history initializes as empty."""
        history = dspy.History(messages=[])
        assert len(history.messages) == 0
    
    def test_history_append(self):
        """Test appending messages to history."""
        history = dspy.History(messages=[])
        
        history.messages.append({
            "question": "Test question",
            "answer": "Test answer"
        })
        
        assert len(history.messages) == 1
        assert history.messages[0]["question"] == "Test question"
        assert history.messages[0]["answer"] == "Test answer"
    
    def test_multiple_turns(self):
        """Test multiple conversation turns."""
        history = dspy.History(messages=[])
        
        # Add multiple turns
        for i in range(3):
            history.messages.append({
                "question": f"Question {i}",
                "answer": f"Answer {i}"
            })
        
        assert len(history.messages) == 3


class TestErrorHandling:
    """Tests for error handling."""
    
    def test_empty_question_handling(self):
        """Test handling of empty questions."""
        question = ""
        # Add actual test logic
        assert question == "" or question.isspace()
    
    def test_missing_api_key(self):
        """Test behavior when API key is missing."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="OPENAI_API_KEY"):
                from examples.basic_conversation import main
                # This should raise an error


# Add more tests as needed
```

**Testing Checklist:**
- [ ] Write signature tests
- [ ] Write history tests
- [ ] Write error handling tests
- [ ] Run tests: `pytest tests/test_conversation.py -v`
- [ ] Verify all tests pass
- [ ] Check code coverage

---

### Phase 2: Advanced Features (Days 4-7)

#### Step 2.1: Create Conversation Manager

**File:** `examples/conversation_manager.py`

```python
"""
Conversation Manager
====================

A helper class for managing conversational AI interactions with DSPy.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

import dspy


class ConversationManager:
    """Manages conversation state and history.
    
    This class provides a high-level interface for conducting conversations
    with language models while maintaining context through history.
    
    Attributes:
        predictor: DSPy Predict module
        history: Conversation history object
        config: Configuration dictionary
    
    Example:
        >>> manager = ConversationManager()
        >>> response = manager.ask("What is DSPy?")
        >>> print(response)
    """
    
    def __init__(
        self,
        signature: type[dspy.Signature] = None,
        lm_config: Optional[Dict[str, Any]] = None,
        max_history: int = 100
    ):
        """Initialize conversation manager.
        
        Args:
            signature: DSPy signature class to use
            lm_config: Language model configuration
            max_history: Maximum number of messages in history
        """
        # Set up LM if config provided
        if lm_config:
            self._configure_lm(lm_config)
        
        # Create default signature if none provided
        if signature is None:
            signature = self._create_default_signature()
        
        # Initialize predictor
        self.predictor = dspy.Predict(signature)
        
        # Initialize history
        self.history = dspy.History(messages=[])
        
        # Configuration
        self.max_history = max_history
        self.config = lm_config or {}
    
    def _create_default_signature(self) -> type[dspy.Signature]:
        """Create default QA signature."""
        class QA(dspy.Signature):
            """Question-answering with conversation history."""
            question: str = dspy.InputField()
            history: dspy.History = dspy.InputField()
            answer: str = dspy.OutputField()
        
        return QA
    
    def _configure_lm(self, config: Dict[str, Any]) -> None:
        """Configure language model from config dict."""
        provider = config.get("provider", "openai")
        model = config.get("model", "gpt-4o-mini")
        api_key = config.get("api_key") or os.environ.get("OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError("API key not found in config or environment")
        
        lm = dspy.LM(f"{provider}/{model}", api_key=api_key)
        dspy.settings.configure(lm=lm)
    
    def ask(
        self,
        question: str,
        add_to_history: bool = True,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Process a question and return response.
        
        Args:
            question: User's question
            add_to_history: Whether to add this turn to history
            metadata: Additional metadata to store
        
        Returns:
            Model's response
        
        Raises:
            ValueError: If question is empty
            RuntimeError: If prediction fails
        """
        # Validate input
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")
        
        question = question.strip()
        
        # Check history size
        if len(self.history.messages) >= self.max_history:
            self._trim_history()
        
        # Make prediction
        try:
            result = self.predictor(
                question=question,
                history=self.history
            )
            answer = result.answer
        except Exception as e:
            raise RuntimeError(f"Prediction failed: {e}")
        
        # Update history if requested
        if add_to_history:
            message = {
                "question": question,
                "answer": answer,
                "timestamp": datetime.now().isoformat()
            }
            
            if metadata:
                message["metadata"] = metadata
            
            self.history.messages.append(message)
        
        return answer
    
    def _trim_history(self, keep_last: int = None) -> None:
        """Trim history to keep only recent messages."""
        if keep_last is None:
            keep_last = self.max_history // 2
        
        self.history.messages = self.history.messages[-keep_last:]
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get conversation history.
        
        Returns:
            List of conversation messages
        """
        return self.history.messages.copy()
    
    def clear_history(self) -> None:
        """Clear conversation history."""
        self.history = dspy.History(messages=[])
    
    def save(self, filepath: str) -> None:
        """Save conversation to file.
        
        Args:
            filepath: Path to save conversation
        """
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "messages": self.history.messages,
            "config": self.config,
            "saved_at": datetime.now().isoformat()
        }
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load(self, filepath: str) -> None:
        """Load conversation from file.
        
        Args:
            filepath: Path to conversation file
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.history = dspy.History(messages=data.get("messages", []))
    
    def format_history(self, max_messages: Optional[int] = None) -> str:
        """Format history for display.
        
        Args:
            max_messages: Maximum messages to include
        
        Returns:
            Formatted string
        """
        messages = self.history.messages
        if max_messages:
            messages = messages[-max_messages:]
        
        formatted = []
        for i, msg in enumerate(messages, 1):
            formatted.append(f"Turn {i}:")
            formatted.append(f"  Q: {msg['question']}")
            formatted.append(f"  A: {msg['answer']}")
            if "timestamp" in msg:
                formatted.append(f"  Time: {msg['timestamp']}")
            formatted.append("")
        
        return "\n".join(formatted)


def main():
    """Demo conversation manager usage."""
    # Create manager
    manager = ConversationManager()
    
    # Have conversation
    print("Conversation started. Type 'finish' to end.\n")
    
    while True:
        question = input("You: ").strip()
        
        if question.lower() == "finish":
            break
        
        if not question:
            continue
        
        try:
            answer = manager.ask(question)
            print(f"\nAI: {answer}\n")
        except Exception as e:
            print(f"\nError: {e}\n")
    
    # Show summary
    print(f"\nConversation ended. Total turns: {len(manager.get_history())}")
    
    # Optionally save
    save = input("Save conversation? (y/n): ").strip().lower()
    if save == 'y':
        filename = f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        manager.save(filename)
        print(f"Saved to {filename}")


if __name__ == "__main__":
    main()
```

**Implementation Checklist:**
- [ ] Create ConversationManager class
- [ ] Implement initialization
- [ ] Implement ask() method
- [ ] Implement history management
- [ ] Implement save/load
- [ ] Add comprehensive docstrings
- [ ] Test all methods

#### Step 2.2: Create Advanced Example

**File:** `examples/advanced_conversation.py`

```python
"""
Advanced Conversation Example
==============================

Demonstrates advanced features:
- Configuration from file
- Conversation persistence
- Error handling with retries
- Context management
"""

import json
import time
from pathlib import Path
from typing import Optional

from conversation_manager import ConversationManager


def load_config(config_path: str = "config.json") -> dict:
    """Load configuration from file."""
    if Path(config_path).exists():
        with open(config_path) as f:
            return json.load(f)
    return {}


def run_conversation_with_retries(
    manager: ConversationManager,
    question: str,
    max_retries: int = 3
) -> Optional[str]:
    """Run prediction with automatic retries on failure."""
    for attempt in range(max_retries):
        try:
            return manager.ask(question)
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Failed after {max_retries} attempts: {e}")
                return None
            
            wait_time = 2 ** attempt
            print(f"Error occurred. Retrying in {wait_time}s...")
            time.sleep(wait_time)


def main():
    """Run advanced conversation example."""
    # Load config
    config = load_config()
    
    # Create manager
    manager = ConversationManager(lm_config=config.get("lm"))
    
    # Try to load previous conversation
    last_conversation = "last_conversation.json"
    if Path(last_conversation).exists():
        load = input("Load previous conversation? (y/n): ").strip().lower()
        if load == 'y':
            manager.load(last_conversation)
            print(f"Loaded {len(manager.get_history())} previous messages\n")
    
    # Conversation loop with enhanced features
    print("Advanced conversation started. Commands:")
    print("  'finish' - End conversation")
    print("  'history' - Show conversation history")
    print("  'clear' - Clear history")
    print("  'save' - Save conversation")
    print()
    
    while True:
        question = input("You: ").strip()
        
        # Handle commands
        if question.lower() == "finish":
            break
        elif question.lower() == "history":
            print("\n" + manager.format_history() + "\n")
            continue
        elif question.lower() == "clear":
            manager.clear_history()
            print("History cleared.\n")
            continue
        elif question.lower() == "save":
            filename = input("Filename: ").strip()
            manager.save(filename or "conversation.json")
            print("Saved.\n")
            continue
        
        if not question:
            continue
        
        # Process question with retries
        answer = run_conversation_with_retries(manager, question)
        if answer:
            print(f"\nAI: {answer}\n")
    
    # Auto-save on exit
    manager.save(last_conversation)
    print(f"\nConversation saved. Total turns: {len(manager.get_history())}")


if __name__ == "__main__":
    main()
```

**Implementation Checklist:**
- [ ] Create advanced example
- [ ] Add config loading
- [ ] Implement retry logic
- [ ] Add command handling
- [ ] Test all features
- [ ] Document usage

---

### Phase 3: Testing & Documentation (Days 8-10)

#### Step 3.1: Complete Test Suite

**File:** `tests/test_integration.py`

```python
"""Integration tests for conversation system."""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch

from examples.conversation_manager import ConversationManager


class TestConversationManagerIntegration:
    """Integration tests for ConversationManager."""
    
    @pytest.fixture
    def manager(self):
        """Create a conversation manager for testing."""
        with patch('dspy.LM'):
            with patch('dspy.settings.configure'):
                manager = ConversationManager()
                return manager
    
    def test_full_conversation_flow(self, manager):
        """Test a complete conversation flow."""
        # Mock the predictor
        with patch.object(manager.predictor, '__call__') as mock_predict:
            mock_predict.return_value = Mock(answer="Test answer")
            
            # Ask multiple questions
            answers = []
            for i in range(3):
                answer = manager.ask(f"Question {i}")
                answers.append(answer)
            
            # Verify
            assert len(answers) == 3
            assert len(manager.get_history()) == 3
    
    def test_save_and_load(self, manager):
        """Test saving and loading conversations."""
        # Add some messages
        with patch.object(manager.predictor, '__call__') as mock_predict:
            mock_predict.return_value = Mock(answer="Test answer")
            
            manager.ask("Question 1")
            manager.ask("Question 2")
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name
        
        try:
            manager.save(temp_path)
            
            # Create new manager and load
            new_manager = ConversationManager()
            new_manager.load(temp_path)
            
            # Verify
            assert len(new_manager.get_history()) == 2
            assert new_manager.get_history()[0]["question"] == "Question 1"
        finally:
            Path(temp_path).unlink()
    
    def test_history_trimming(self, manager):
        """Test automatic history trimming."""
        manager.max_history = 5
        
        with patch.object(manager.predictor, '__call__') as mock_predict:
            mock_predict.return_value = Mock(answer="Test answer")
            
            # Add more than max_history messages
            for i in range(10):
                manager.ask(f"Question {i}")
            
            # Should have trimmed
            assert len(manager.get_history()) <= manager.max_history
```

**Testing Checklist:**
- [ ] Write integration tests
- [ ] Test error scenarios
- [ ] Test edge cases
- [ ] Run full test suite
- [ ] Achieve >85% coverage
- [ ] Fix any failures

#### Step 3.2: Write Tutorial Documentation

**File:** `index.md`

```markdown
# Managing Conversation History

Maintaining conversation history is essential when building conversational AI 
applications. This tutorial shows you how to use DSPy to create AI systems 
that remember context across multiple turns.

## What You'll Learn

- How to use `dspy.History` for conversation management
- Building interactive conversation loops
- Maintaining context across multiple turns
- Saving and loading conversations
- Error handling in conversational AI

## Prerequisites

- Python 3.10 or later
- DSPy installed (`pip install dspy`)
- OpenAI API key (or access to another LM provider)
- Basic Python programming knowledge

**Estimated Time:** 20-30 minutes

## Quick Start

[Continue with rest of tutorial content...]
```

**Documentation Checklist:**
- [ ] Write introduction
- [ ] Add setup instructions
- [ ] Create code examples
- [ ] Add explanations
- [ ] Include troubleshooting
- [ ] Add next steps
- [ ] Review for clarity

---

### Phase 4: Polish & Validation (Days 11-12)

#### Step 4.1: Code Review

**Checklist:**
- [ ] All code follows DSPy style guide
- [ ] No hardcoded credentials
- [ ] Comprehensive error handling
- [ ] All functions have docstrings
- [ ] Type hints where appropriate
- [ ] No TODO comments
- [ ] Pre-commit hooks pass

#### Step 4.2: Documentation Review

**Checklist:**
- [ ] All examples tested and working
- [ ] No spelling/grammar errors
- [ ] Links are valid
- [ ] Code blocks are formatted correctly
- [ ] Screenshots included where helpful
- [ ] Clear and concise writing

#### Step 4.3: User Testing

**Tasks:**
- [ ] Find 3-5 test users
- [ ] Have them complete tutorial
- [ ] Collect feedback
- [ ] Note pain points
- [ ] Measure completion time
- [ ] Address feedback

---

## 3. Common Implementation Patterns

### Pattern 1: Error Handling with Retry

```python
def safe_predict(predictor, question, history, max_retries=3):
    """Predict with automatic retry."""
    for attempt in range(max_retries):
        try:
            return predictor(question=question, history=history)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
```

### Pattern 2: Context Window Management

```python
def manage_context_window(history, max_tokens=8000):
    """Keep history within token limits."""
    # Estimate tokens (rough approximation)
    total_tokens = sum(
        len(msg["question"]) + len(msg["answer"]) 
        for msg in history.messages
    ) // 4
    
    # Trim if needed
    while total_tokens > max_tokens and history.messages:
        history.messages.pop(0)
        total_tokens = sum(
            len(msg["question"]) + len(msg["answer"])
            for msg in history.messages
        ) // 4
```

### Pattern 3: Conversation State Management

```python
class ConversationState:
    """Track conversation state."""
    
    def __init__(self):
        self.is_active = False
        self.start_time = None
        self.turn_count = 0
        self.last_error = None
    
    def start(self):
        self.is_active = True
        self.start_time = datetime.now()
    
    def record_turn(self):
        self.turn_count += 1
    
    def record_error(self, error):
        self.last_error = str(error)
```

---

## 4. Testing Guidelines

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_conversation.py -v

# Run with coverage
pytest tests/ --cov=examples --cov-report=html

# Run only integration tests
pytest tests/test_integration.py -v
```

### Writing Good Tests

1. **Test behavior, not implementation**
2. **Use descriptive test names**
3. **One assertion per test (when possible)**
4. **Use fixtures for setup**
5. **Mock external dependencies**
6. **Test edge cases**

---

## 5. Troubleshooting

### Common Issues

#### Issue: ModuleNotFoundError
```
Solution: Ensure DSPy is installed: pip install dspy
```

#### Issue: API Key Not Found
```
Solution: Set environment variable: export OPENAI_API_KEY=sk-...
```

#### Issue: Tests Failing
```
Solution: Check that mocks are configured correctly
```

---

## 6. Deployment Checklist

Before merging to main:

- [ ] All tests passing
- [ ] Code coverage >85%
- [ ] Documentation complete
- [ ] Examples tested
- [ ] Pre-commit hooks pass
- [ ] User testing completed
- [ ] Feedback addressed
- [ ] Code reviewed by team member
- [ ] Performance benchmarks met
- [ ] No security issues

---

## 7. Resources

- [DSPy Documentation](https://dspy.ai/)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Python Testing Guide](https://docs.pytest.org/)
- [DSPy GitHub](https://github.com/stanfordnlp/dspy)

---

## 8. Next Steps

After completing implementation:

1. Submit PR for review
2. Address reviewer feedback
3. Update documentation based on feedback
4. Announce in community channels
5. Monitor for issues
6. Plan follow-up improvements

---

**Document Version:** 1.0  
**Last Updated:** 2025-10-22  
**Maintainer:** DSPy Project Team
