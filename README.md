# agentic-patterns

A collection of agentic design patterns and tools for building advanced Python agents, including reflection and tool-use patterns. This project leverages modern LLMs and best practices for agentic workflows.

## Features

- Reflection agent for iterative code improvement and critique
- Utilities for completions and prompt building
- Modular structure for extensibility

## Requirements

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (a fast Python package installer and resolver)

## Environment Variables

You must create a `.env` file in the project root with your [GROQ API key](https://console.groq.com/keys):

```
GROQ_API_KEY=your_groq_api_key_here
```

See [how to generate a GROQ API key](https://console.groq.com/keys) for more information.

## Installation

1. **Install `uv`** (if you don’t have it):

   ```sh
   pip install uv
   ```

2. **Create and activate a virtual environment**:

   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies with `uv`**:

   ```sh
   uv pip install -r requirements.txt
   ```

   Or, directly from `pyproject.toml`:

   ```sh
   uv pip install .
   ```

   For development dependencies:

   ```sh
   uv pip install .[dev]
   ```

## Usage

You can run the reflection agent example by executing:

```sh
python agentic_patterns/reflection_pattern/reflection_agent.py
```

This will run a sample reflection loop that generates and critiques code.

## Project Structure

- `agentic_patterns/`
  - `reflection_pattern/` – Reflection agent implementation
  - `utils/` – Utilities for completions and prompt management

## Contributing

Contributions are welcome! Please open issues or pull requests.

## License

This project is licensed under the MIT License.

---