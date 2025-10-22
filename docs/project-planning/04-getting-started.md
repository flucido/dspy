# Getting Started: DSPy Conversation History Tutorial

## Welcome! 🎉

This guide will help you get started with the DSPy Conversation History Tutorial. Whether you're new to DSPy or looking to build conversational AI applications, you're in the right place!

---

## What is DSPy?

**DSPy** (Declarative Self-improving Python) is a framework for programming—rather than prompting—language models. Instead of writing brittle prompts, you write compositional Python code and use DSPy to teach your language model to deliver high-quality outputs.

### Key Concepts

- **Signatures:** Define what your LM should do (inputs/outputs)
- **Modules:** Components that use signatures to solve tasks
- **Optimizers:** Automatically improve prompts and weights
- **History:** Manage conversation context

---

## Why This Tutorial?

The Conversation History Tutorial is perfect for beginners because it:

✅ **Simple to Understand:** Clear, focused examples  
✅ **Practical:** Build a real conversational AI  
✅ **Foundation Building:** Learn core DSPy concepts  
✅ **Quick:** Complete in 20-30 minutes  
✅ **Extensible:** Easy to build upon  

---

## Prerequisites

### Required Knowledge

- **Python:** Basic Python programming (functions, classes, loops)
- **Command Line:** Comfortable using terminal/command prompt
- **APIs:** Understanding of API keys (we'll explain the rest!)

### Required Software

- **Python 3.10+** - [Download here](https://www.python.org/downloads/)
- **pip** - Python package manager (comes with Python)
- **Text Editor** - VS Code, PyCharm, or any editor you prefer
- **Terminal** - Command line interface

### Required Accounts

- **OpenAI Account** - [Sign up here](https://platform.openai.com/)
  - You'll need an API key
  - Free tier is sufficient for this tutorial
  - Alternative: Use any LM provider supported by DSPy

---

## Installation

### Step 1: Check Python Version

```bash
python --version
# Should show Python 3.10 or higher
```

If you need to install Python:
- **Windows:** Download from [python.org](https://www.python.org/downloads/)
- **Mac:** `brew install python@3.10` (requires Homebrew)
- **Linux:** `sudo apt install python3.10` (Ubuntu/Debian)

### Step 2: Create Project Directory

```bash
# Create a folder for your project
mkdir dspy-conversation
cd dspy-conversation
```

### Step 3: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

# You should see (venv) in your prompt
```

### Step 4: Install DSPy

```bash
# Install DSPy
pip install dspy

# Verify installation
python -c "import dspy; print(dspy.__version__)"
```

### Step 5: Get OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign in or create an account
3. Navigate to API Keys section
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)
6. **Important:** Save it somewhere safe - you won't see it again!

### Step 6: Set Environment Variable

```bash
# On Mac/Linux, add to ~/.bashrc or ~/.zshrc:
export OPENAI_API_KEY=sk-your-key-here

# Or set for current session:
export OPENAI_API_KEY=sk-your-key-here

# On Windows (PowerShell):
$env:OPENAI_API_KEY="sk-your-key-here"

# Or use Command Prompt:
set OPENAI_API_KEY=sk-your-key-here
```

**Security Note:** Never commit API keys to version control!

---

## Quick Start: Your First Conversation

Let's create a simple conversation in just a few minutes!

### Step 1: Create Your First Script

Create a file called `my_first_conversation.py`:

```python
import os
import dspy

# Configure DSPy with your LM
api_key = os.environ.get("OPENAI_API_KEY")
lm = dspy.LM("openai/gpt-4o-mini", api_key=api_key)
dspy.settings.configure(lm=lm)

# Define what you want the LM to do
class QA(dspy.Signature):
    """Answer questions with conversation history."""
    question: str = dspy.InputField()
    history: dspy.History = dspy.InputField()
    answer: str = dspy.OutputField()

# Create the predictor
predict = dspy.Predict(QA)

# Initialize empty history
history = dspy.History(messages=[])

# Have a conversation!
print("Ask me anything! Type 'exit' to quit.\n")

while True:
    question = input("You: ").strip()
    
    if question.lower() == 'exit':
        break
    
    if not question:
        continue
    
    # Get answer with history context
    result = predict(question=question, history=history)
    print(f"AI: {result.answer}\n")
    
    # Remember this turn
    history.messages.append({
        "question": question,
        "answer": result.answer
    })

print(f"Conversation ended. Had {len(history.messages)} turns!")
```

### Step 2: Run It!

```bash
python my_first_conversation.py
```

### Step 3: Try It Out

```
You: What is the capital of France?
AI: The capital of France is Paris.

You: What's interesting about that city?
AI: Paris is known for the Eiffel Tower, the Louvre Museum, Notre-Dame Cathedral, and its café culture...

You: exit
Conversation ended. Had 2 turns!
```

🎉 **Congratulations!** You just built your first conversational AI with DSPy!

---

## Understanding What You Built

Let's break down the code:

### 1. Configure DSPy

```python
lm = dspy.LM("openai/gpt-4o-mini", api_key=api_key)
dspy.settings.configure(lm=lm)
```

This tells DSPy which language model to use. Think of it as "connecting" to the AI.

### 2. Define a Signature

```python
class QA(dspy.Signature):
    question: str = dspy.InputField()
    history: dspy.History = dspy.InputField()
    answer: str = dspy.OutputField()
```

A **Signature** describes what goes in (inputs) and what comes out (outputs). It's like a contract: "Give me a question and history, I'll give you an answer."

### 3. Create a Predictor

```python
predict = dspy.Predict(QA)
```

This creates a **Module** that uses your signature. The module handles all the complexity of talking to the LM.

### 4. Manage History

```python
history = dspy.History(messages=[])
```

The **History** object stores previous conversation turns, giving the AI context.

### 5. The Loop

```python
result = predict(question=question, history=history)
history.messages.append({"question": question, "answer": result.answer})
```

Each turn: ask a question → get an answer → add to history → repeat!

---

## What Makes This Powerful?

### Traditional Approach (Prompting)

```python
# Fragile, hard to maintain
prompt = f"""
Previous conversation:
{format_history_somehow(history)}

User: {question}
Assistant:
"""
response = openai.chat.completions.create(...)
```

❌ Brittle prompt engineering  
❌ Manual history formatting  
❌ Hard to optimize  
❌ Difficult to compose  

### DSPy Approach (Programming)

```python
# Clean, maintainable, optimizable
result = predict(question=question, history=history)
```

✅ Declarative interface  
✅ Automatic prompt generation  
✅ Easy to optimize  
✅ Composable modules  

---

## Next Steps

Now that you have the basics working, you can:

### 1. Explore Advanced Features

- Add conversation persistence (save/load)
- Implement error handling and retries
- Manage context window limits
- Add metadata to messages

### 2. Complete the Full Tutorial

The full tutorial covers:
- Building a conversation manager class
- Advanced history management
- Testing your conversational AI
- Best practices and patterns
- Real-world examples

### 3. Build Something Cool

Ideas to get you started:
- Personal assistant chatbot
- Customer service bot
- Educational tutor
- Creative writing partner
- Code review assistant

---

## Common Questions

### Q: Do I need to pay for OpenAI?

A: OpenAI offers free credits for new users. The tutorial uses very few tokens, so you can complete it on the free tier.

### Q: Can I use a different LM provider?

A: Yes! DSPy supports many providers:
```python
# Anthropic
lm = dspy.LM("anthropic/claude-3-sonnet")

# Local model with Ollama
lm = dspy.LM("ollama/llama2")

# Azure OpenAI
lm = dspy.LM("azure/gpt-4")
```

### Q: Why use DSPy instead of direct API calls?

A: DSPy provides:
- Higher-level abstractions
- Automatic prompt optimization
- Built-in best practices
- Easier testing and debugging
- Composable modules

### Q: Is this suitable for production?

A: Yes! DSPy is used in production by many companies. The tutorial teaches production-ready patterns.

### Q: How long does the tutorial take?

A: 20-30 minutes for the basic tutorial, 1-2 hours to explore advanced features.

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'dspy'"

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install DSPy
pip install dspy
```

### Issue: "Error: OpenAI API key not found"

**Solution:**
```bash
# Check if variable is set
echo $OPENAI_API_KEY  # Mac/Linux
echo %OPENAI_API_KEY% # Windows

# Set it if not
export OPENAI_API_KEY=sk-your-key-here  # Mac/Linux
set OPENAI_API_KEY=sk-your-key-here     # Windows
```

### Issue: "API rate limit exceeded"

**Solution:**
- Wait a minute and try again
- Use a different model (gpt-3.5-turbo is faster/cheaper)
- Implement retry logic with backoff

### Issue: Slow responses

**Possible causes:**
- Network latency
- Model selection (GPT-4 is slower than GPT-3.5)
- Large context window

**Solutions:**
- Use gpt-3.5-turbo for faster responses
- Trim history to reduce context size
- Consider local models for development

---

## Resources

### Official Documentation

- [DSPy Docs](https://dspy.ai/) - Complete DSPy documentation
- [DSPy GitHub](https://github.com/stanfordnlp/dspy) - Source code and examples
- [OpenAI API Docs](https://platform.openai.com/docs) - API reference

### Community

- [DSPy Discord](https://discord.gg/XCGy2WDCQB) - Get help and share projects
- [GitHub Discussions](https://github.com/stanfordnlp/dspy/discussions) - Q&A and ideas
- [Twitter @DSPyOSS](https://twitter.com/DSPyOSS) - Updates and announcements

### Learning Resources

- [DSPy Cheat Sheet](https://dspy.ai/cheatsheet) - Quick reference
- [Example Gallery](https://github.com/stanfordnlp/dspy/tree/main/examples) - More examples
- [Research Papers](https://dspy.ai/) - Academic background

---

## Getting Help

### If you're stuck:

1. **Check the error message** - Often tells you exactly what's wrong
2. **Review this guide** - Common issues covered in Troubleshooting
3. **Search GitHub issues** - Someone may have had the same problem
4. **Ask on Discord** - Friendly community ready to help
5. **Open an issue** - If you found a bug

### When asking for help:

Include:
- Python version
- DSPy version
- Error message (full traceback)
- Code snippet showing the issue
- What you've already tried

---

## Ready to Continue?

Great! You're all set up and ready to dive deeper. Here's what to do next:

1. ✅ Complete the Quick Start above
2. 📚 Read the [Full Tutorial](index.md)
3. 💻 Explore [Advanced Examples](examples/advanced_conversation.py)
4. 🧪 Try [Testing Guide](tests/README.md)
5. 🚀 Build your own project!

---

## Feedback

We'd love to hear from you!

- Found an issue? [Open a GitHub issue](https://github.com/stanfordnlp/dspy/issues)
- Have a suggestion? [Start a discussion](https://github.com/stanfordnlp/dspy/discussions)
- Built something cool? Share it on Discord!

---

**Happy coding! 🚀**

*Last updated: 2025-10-22*  
*Tutorial version: 1.0*
