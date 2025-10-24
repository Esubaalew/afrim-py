<div align="center">

  <h1><code>afrim-py</code></h1>

  <strong>Python bindings for the <a href="https://github.com/pythonbrad/afrim">afrim ime engine</a>.</strong>

  <p>
    <img alt="Python" src="https://img.shields.io/badge/python-3.8+-blue.svg"/>
    <img alt="Rust" src="https://img.shields.io/badge/rust-1.70+-orange.svg"/>
    <img alt="License" src="https://img.shields.io/badge/license-MIT-green.svg"/>
    <a href="https://github.com/fodydev/afrim/blob/main/CHANGELOG.md"><img alt="Changelog" src="https://img.shields.io/badge/Keep%20a%20Changelog--555.svg?logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGZpbGw9IiNmMTVkMzAiIHZpZXdCb3g9IjAgMCAxODcgMTg1Ij48cGF0aCBkPSJNNjIgN2MtMTUgMy0yOCAxMC0zNyAyMmExMjIgMTIyIDAgMDAtMTggOTEgNzQgNzQgMCAwMDE2IDM4YzYgOSAxNCAxNSAyNCAxOGE4OSA4OSAwIDAwMjQgNCA0NSA0NSAwIDAwNiAwbDMtMSAxMy0xYTE1OCAxNTggMCAwMDU1LTE3IDYzIDYzIDAgMDAzNS01MiAzNCAzNCAwIDAwLTEtNWMtMy0xOC05LTMzLTE5LTQ3LTEyLTE3LTI0LTI4LTM4LTM3QTg1IDg1IDAgMDA2MiA3em0zMCA4YzIwIDQgMzggMTQgNTMgMzEgMTcgMTggMjYgMzcgMjkgNTh2MTJjLTMgMTctMTMgMzAtMjggMzhhMTU1IDE1NSAwIDAxLTUzIDE2bC0xMyAyaC0xYTUxIDUxIDAgMDEtMTItMWwtMTctMmMtMTMtNC0yMy0xMi0yOS0yNy01LTEyLTgtMjQtOC0zOWExMzMgMTMzIDAgMDE4LTUwYzUtMTMgMTEtMjYgMjYtMzMgMTQtNyAyOS05IDQ1LTV6TTQwIDQ1YTk0IDk0IDAgMDAtMTcgNTQgNzUgNzUgMCAwMDYgMzJjOCAxOSAyMiAzMSA0MiAzMiAyMSAyIDQxLTIgNjAtMTRhNjAgNjAgMCAwMDIxLTE5IDUzIDUzIDAgMDA5LTI5YzAtMTYtOC0zMy0yMy01MWE0NyA0NyAwIDAwLTUtNWMtMjMtMjAtNDUtMjYtNjctMTgtMTIgNC0yMCA5LTI2IDE4em0xMDggNzZhNTAgNTAgMCAwMS0yMSAyMmMtMTcgOS0zMiAxMy00OCAxMy0xMSAwLTIxLTMtMzAtOS01LTMtOS05LTEzLTE2YTgxIDgxIDAgMDEtNi0zMiA5NCA5NCAwIDAxOC0zNSA5MCA5MCAwIDAxNi0xMmwxLTJjNS05IDEzLTEzIDIzLTE2IDE2LTUgMzItMyA1MCA5IDEzIDggMjMgMjAgMzAgMzYgNyAxNSA3IDI5IDAgNDJ6bS00My03M2MtMTctOC0zMy02LTQ2IDUtMTAgOC0xNiAyMC0xOSAzN2E1NCA1NCAwIDAwNSAzNGM3IDE1IDIwIDIzIDM3IDIyIDIyLTEgMzgtOSA0OC0yNGE0MSA0MSAwIDAwOC0yNCA0MyA0MyAwIDAwLTEtMTJjLTYtMTgtMTYtMzEtMzItMzh6bS0yMyA5MWgtMWMtNyAwLTE0LTItMjEtN2EyNyAyNyAwIDAxLTEwLTEzIDU3IDU3IDAgMDEtNC0yMCA2MyA2MyAwIDAxNi0yNWM1LTEyIDEyLTE5IDI0LTIxIDktMyAxOC0yIDI3IDIgMTQgNiAyMyAxOCAyNyAzM3MtMiAzMS0xNiA0MGMtMTEgOC0yMSAxMS0zMiAxMXptMS0zNHYxNGgtOFY2OGg4djI4bDEwLTEwaDExbC0xNCAxNSAxNyAxOEg5NnoiLz48L3N2Zz4K"/></a>

  </p>

  <h3>
    <a href="https://github.com/fodydev/afrim-py">Repository</a>
  </h3>

  <sub>Built with 🦀🐍 by <a href="https://github.com/esubaalew">@esubaalew</a></sub>
</div>

## About

`afrim-py` provides Python bindings for the powerful afrim input method engine, enabling developers to build sophisticated input method applications in Python. This project brings the capabilities of the Rust-based afrim engine to the Python ecosystem through PyO3 bindings.

## 🔋 Features Included

* **Preprocessor** - Advanced key sequence processing and input transformation
* **Translator** - Dictionary-based text translation with multiple candidates
* **TOML Support** - Easy configuration through TOML files
* **Unicode Support** - Full support for international characters
* **Rhai Scripting** - Dynamic translation scripts (when `rhai` feature is enabled)
* **String Similarity** - Fuzzy matching with `strsim` feature

## Installation

`afrim-py` is available on pypi.

```bash
pip install afrim-py
```

## Usage

### Basic Example

```python
from afrim_py import Preprocessor, Translator, Config

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

### Configuration

```python
from afrim_py import Config
import json

# Configuration file `config.toml`
'''
[core]
buffer_size = 64
auto_capitalize = false
auto_commit = false
page_size = 10

[data]
a1 = "à"
e2 = "é"

[translators]
datetime = { path = "./scripts/datetime.toml" }

[translation]
hi = 'hello'
'''
config = Config('config.toml')

# Use the configuration
preprocessor_data = config.extract_data()
preprocessor = Preprocessor(preprocessor_data, 64)
translator_dict = config.extract_translation()
translator = Translator(translator_dict, True)
```

### Advanced Usage with Command Processing

```python
import asyncio
from afrim_py import Preprocessor, Translator, Config

class InputMethodEngine:
    def __init__(self, config_file: str):
        config = Config(config_file)
        self.preprocessor = Preprocessor(config.extract_data(), 64)
        self.translator = Translator(config.extract_translation(), True)
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
        preprocessor_data={"A": "ዕ", "Aa": "ዓ", "C": "ጭ"},
        translator_dict={"Atarah": ["ዓጣራ"], "Adiel": ["ዓዲዔል"]}
    )
    
    # Simulate key events
    translations = ime.handle_key_event("A")
    translations = ime.handle_key_event("a")
    translations = ime.handle_key_event("C")
    
    print("Translations:", translations)
    
    # Commit text
    if translations:
        ime.commit_text(translations[0]["texts"][0])

# Run the example
# asyncio.run(main())
```

## Development

### Build requirements

- Rust 1.70+
- Cargo

- Python 3.8+ and and [maturin](https://www.maturin.rs/installation.html)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) *(optional)*

### Build from source

To simplify the development, we recommend to use `uv`.

**Using maturin**

```bash
# Clone the repository
git clone https://github.com/fodydev/afrim-py.git
cd afrim-py

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Development build
maturin develop

# Release build
maturin build --release

# Build wheel
maturin build --interpreter python
```

**Using uv**

```bash
# Clone the repository
git clone https://github.com/fodydev/afrim-py.git
cd afrim-py

# Prerelease build
uv build --prerelease

# Release build
uv build
```

### Testing

The project includes tests that represent a real user scenario:

```bash
# Run all tests
python -m pytest tests/ -v
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgments

- **[afrim-js](https://github.com/pythonbrad/afrim-js)** - Web bindings that inspired this project

## License

Licensed under the [MIT LICENSE](LICENSE).
