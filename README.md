# ETA - Python Development Project

A Python development project scaffolded similarly to emtv structure.

## Project Structure

```
eta/
├── .github/
│   └── copilot-instructions.md
├── src/
│   └── eta/
│       ├── __init__.py
│       └── main.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── docs/
├── .gitignore
├── requirements.txt
├── setup.py
├── pyproject.toml
└── README.md
```

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main application:
```bash
python -m src.eta.main
```

Or use the VS Code task "Run ETA Application" for convenience.

## Development

### Testing
Run tests:
```bash
python -m pytest tests/
```

### Code Quality
Format code:
```bash
python -m black src/ tests/
```

Lint code:
```bash
python -m flake8 src/ tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request