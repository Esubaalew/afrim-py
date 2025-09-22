<div align="center">

  <h1><code>afrim-py</code></h1>

  <strong>Python bindings for the <a href="https://github.com/pythonbrad/afrim">afrim ime engine</a>.</strong>

  <p>
    <img alt="Python" src="https://img.shields.io/badge/python-3.8+-blue.svg"/>
    <img alt="Rust" src="https://img.shields.io/badge/rust-1.70+-orange.svg"/>
    <img alt="License" src="https://img.shields.io/badge/license-MIT-green.svg"/>
  </p>

  <h3>
    <a href="https://github.com/esubaalew/afrim-py">Repository</a>
  </h3>

  <sub>Built with 🦀🐍 by <a href="https://github.com/esubaalew">@esubaalew</a></sub>
  <br>
  <sub>Inspired by <a href="https://github.com/pythonbrad/afrim">afrim</a> and <a href="https://github.com/pythonbrad/afrim-js">afrim-js</a></sub>
</div>

## About

`afrim-py` provides Python bindings for the powerful afrim input method engine, enabling developers to build sophisticated input method applications in Python. This project brings the capabilities of the Rust-based afrim engine to the Python ecosystem through PyO3 bindings.

## 🛠️ Build with `maturin`

```bash
# Development build
maturin develop

# Production build
maturin build --release
```

## 🔋 Features Included

* **Preprocessor** - Advanced key sequence processing and input transformation
* **Translator** - Dictionary-based text translation with multiple candidates
* **TOML Support** - Easy configuration through TOML files
* **Unicode Support** - Full support for international characters
* **Rhai Scripting** - Dynamic translation scripts (when `rhai` feature is enabled)
* **String Similarity** - Fuzzy matching with `strsim` feature

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/esubaalew/afrim-py.git
cd afrim-py

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
maturin develop
```

### Requirements

- Python 3.8+
- Rust 1.70+
- Cargo and maturin

## Usage

### Basic Example

```python
from afrim_py import Preprocessor, Translator, convert_toml_to_json

# Configure the preprocessor with key mappings
preprocessor_data = {
    "a1": "à",
    "e1": "é", 
    "u1": "ù",
    "hello": "hi"
}

# Configure the translator with dictionary
translator_dict = {
    "hello": ["hi", "hey", "greetings"],
    "world": ["earth", "globe", "planet"],
    "python": ["snake", "programming language"]
}

# Create instances
preprocessor = Preprocessor(preprocessor_data, buffer_size=64)
translator = Translator(translator_dict, auto_commit=True)

# Process keyboard events
changed = preprocessor.process("h", "keydown")
changed = preprocessor.process("e", "keydown") 
changed = preprocessor.process("l", "keydown")
changed = preprocessor.process("l", "keydown")
changed = preprocessor.process("o", "keydown")

# Get the processed input
current_input = preprocessor.get_input()  # "hello"

# Translate the input
translations = translator.translate(current_input)
print(translations)
# [{'texts': ['hi', 'hey', 'greetings'], 'code': 'hello', 'remaining_code': '', 'can_commit': True}]

# Process commands from the queue
while True:
    command = preprocessor.pop_queue()
    if command == "NOP":
        break
    print(f"Command: {command}")
```

### TOML Configuration

```python
from afrim_py import convert_toml_to_json
import json

# TOML configuration
toml_config = '''
[preprocessor]
a1 = "à"
e1 = "é"
hello = "hi"

[translator.greetings]
values = ["hello", "hi", "hey"]

[translator.world]
values = ["earth", "globe", "planet"]
'''

# Convert TOML to JSON
config_json = convert_toml_to_json(toml_config)
config = json.loads(config_json)

# Use the configuration
preprocessor = Preprocessor(config["preprocessor"], 64)
translator_dict = {k: v["values"] for k, v in config["translator"].items()}
translator = Translator(translator_dict, True)
```

### Advanced Usage with Command Processing

```python
import asyncio
from afrim_py import Preprocessor, Translator

class InputMethodEngine:
    def __init__(self, preprocessor_data, translator_dict):
        self.preprocessor = Preprocessor(preprocessor_data, 64)
        self.translator = Translator(translator_dict, True)
        self.running = False
    
    async def process_commands(self):
        """Process commands from the preprocessor queue"""
        while self.running:
            command = self.preprocessor.pop_queue()
            
            if command == "NOP":
                await asyncio.sleep(0.01)  # Small delay
                continue
                
            # Handle different command types
            if isinstance(command, dict):
                if "Insert" in command:
                    text = command["Insert"]["text"]
                    print(f"Insert: {text}")
                elif "Delete" in command:
                    count = command["Delete"]["count"]
                    print(f"Delete: {count} characters")
            else:
                print(f"Command: {command}")
    
    def handle_key_event(self, key, state="keydown"):
        """Handle keyboard events"""
        changed = self.preprocessor.process(key, state)
        
        if changed:
            current_input = self.preprocessor.get_input()
            if current_input:
                translations = self.translator.translate(current_input)
                return translations
        return []
    
    def commit_text(self, text):
        """Commit selected text"""
        self.preprocessor.commit(text)
    
    async def start(self):
        """Start the input method engine"""
        self.running = True
        await self.process_commands()
    
    def stop(self):
        """Stop the input method engine"""
        self.running = False

# Usage
async def main():
    ime = InputMethodEngine(
        preprocessor_data={"hello": "hi", "world": "earth"},
        translator_dict={"hi": ["hello", "greetings"], "earth": ["world", "planet"]}
    )
    
    # Simulate key events
    translations = ime.handle_key_event("h")
    translations = ime.handle_key_event("e")
    translations = ime.handle_key_event("l")
    translations = ime.handle_key_event("l")
    translations = ime.handle_key_event("o")
    
    print("Translations:", translations)
    
    # Commit text
    if translations:
        ime.commit_text(translations[0]["texts"][0])

# Run the example
# asyncio.run(main())
```


## Testing

The project includes a comprehensive test suite with 49+ test cases covering all functionality:

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=afrim_py --cov-report=html

# Run the comprehensive test suite
python run_tests.py
```

## Development

### Prerequisites

- Python 3.8+
- Rust 1.70+
- maturin (`pip install maturin`)

### Setup

```bash
# Clone and setup
git clone https://github.com/esubalew/afrim-py.git
cd afrim-py
python -m venv .venv
source .venv/bin/activate

# Install development dependencies
pip install -r requirements-test.txt

# Build in development mode
maturin develop

# Run tests
python run_tests.py
```

### Building

```bash
# Development build
maturin develop

# Release build
maturin build --release

# Build wheel
maturin build --interpreter python
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Guidelines

1. Run tests before submitting: `python run_tests.py`
2. Follow Python PEP 8 style guidelines
3. Add tests for new functionality
4. Update documentation as needed

## Acknowledgments

- **[afrim](https://github.com/pythonbrad/afrim)** - The original input method engine
- **[afrim-js](https://github.com/pythonbrad/afrim-js)** - Web bindings that inspired this project
- **[@pythonbrad](https://github.com/pythonbrad)** - Creator of the original afrim project

## License

Licensed under MIT license ([LICENSE](LICENSE) or http://opensource.org/licenses/MIT).

## Author

**Esubalew Chekol** ([@esubalew](https://github.com/esubalew))

---

<div align="center">
  <sub>Built with ❤️ using Rust and Python</sub>
</div>
