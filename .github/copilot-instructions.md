<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->
- [x] Verify that the copilot-instructions.md file in the .github directory is created.

- [x] Clarify Project Requirements

- [x] Scaffold the Project

- [x] Customize the Project

- [x] Install Required Extensions

- [x] Compile the Project

- [x] Create and Run Task

- [x] Launch the Project

- [x] Ensure Documentation is Complete

## ETA Python Development Project

This workspace contains a Python development project scaffolded similarly to emtv structure.

### Project Structure
- **src/eta/**: Main application code
- **tests/**: Unit tests
- **docs/**: Documentation
- **requirements.txt**: Python dependencies
- **pyproject.toml**: Modern Python project configuration
- **setup.py**: Package setup configuration

### Development Setup
1. Python environment configured (Python 3.11.9)
2. Dependencies installed (requests, click, pytest, black, flake8, mypy)
3. VS Code tasks configured for running the application

### Usage
- Run the application using the "Run ETA Application" task
- Execute tests with `pytest tests/`
- Format code with `black src/ tests/`
- Lint code with `flake8 src/ tests/`