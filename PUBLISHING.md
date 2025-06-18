# Publishing Guide for just_facebook_mcp

This document explains how to publish the `just_facebook_mcp` package to PyPI.

## Prerequisites

1. **Python 3.10+** and **uv** installed
2. **PyPI account** - Sign up at [pypi.org](https://pypi.org/account/register/)
3. **Test PyPI account** - Sign up at [test.pypi.org](https://test.pypi.org/account/register/)
4. **API tokens** for both PyPI and Test PyPI

## Setup

### 1. Install Build Dependencies

```bash
uv sync --group build
```

### 2. Configure PyPI Authentication

Create a `~/.pypirc` file with your API tokens:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-YOUR_API_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TEST_API_TOKEN_HERE
```

### 3. Package Structure Verification

The package should have this structure:

```
facebook-mcp-server/
├── just_facebook_mcp/           # Main package
│   ├── __init__.py             # Package init with version
│   ├── server.py               # Main MCP server
│   ├── manager.py              # Business logic
│   ├── facebook_api.py         # Facebook API wrapper
│   └── config.py               # Configuration
├── scripts/                    # Build scripts
│   └── build_and_publish.py    # Automated build/publish script
├── pyproject.toml              # Project configuration
├── README.md                   # Main documentation
├── LICENSE                     # MIT License
├── MANIFEST.in                 # Distribution files spec
└── .gitignore                  # Git ignore rules
```

## Publishing Process

### Option 1: Using the Automated Script

```bash
python scripts/build_and_publish.py
```

This script will:
- Clean previous builds
- Run code formatting (black)
- Run type checking (mypy)
- Run tests (if available)
- Build the package
- Check the package
- Ask where to publish

### Option 2: Manual Steps

#### 1. Clean Previous Builds

```bash
rm -rf build/ dist/ *.egg-info/
```

#### 2. Run Quality Checks

```bash
# Format code
uv run black just_facebook_mcp/

# Type checking
uv run mypy just_facebook_mcp/

# Run tests (if available)
uv run pytest
```

#### 3. Build Package

```bash
uv build
```

#### 4. Check Package

```bash
uv run twine check dist/*
```

#### 5. Publish to Test PyPI (Recommended First)

```bash
uv run twine upload --repository testpypi dist/*
```

#### 6. Test Installation from Test PyPI

```bash
pip install --index-url https://test.pypi.org/simple/ just_facebook_mcp
```

#### 7. Publish to PyPI

```bash
uv run twine upload dist/*
```

## Version Management

The package version is automatically extracted from `just_facebook_mcp/__init__.py`. 

To release a new version:

1. Update the version in `just_facebook_mcp/__init__.py`
2. Create a git tag: `git tag v0.1.1`
3. Push the tag: `git push origin v0.1.1`
4. Run the build and publish process

## Verification

After publishing, verify the package:

### Test PyPI
```bash
pip install --index-url https://test.pypi.org/simple/ just_facebook_mcp
```

### Production PyPI
```bash
pip install just_facebook_mcp
```

### Test the Installation
```bash
just_facebook_mcp --help
```

## Troubleshooting

### Common Issues

1. **Authentication Error**: Check your API tokens in `~/.pypirc`
2. **Version Already Exists**: You cannot overwrite existing versions, increment the version number
3. **Missing Files**: Check `MANIFEST.in` includes all necessary files
4. **Import Errors**: Verify package structure and relative imports

### Package Validation

```bash
# Check package metadata
uv run twine check dist/*

# Validate package can be imported
python -c "import just_facebook_mcp; print(just_facebook_mcp.__version__)"
```

## Maintenance

### Regular Updates

1. Keep dependencies updated in `pyproject.toml`
2. Update version numbers for releases
3. Maintain backward compatibility
4. Update documentation as needed

### Security

- Regularly rotate API tokens
- Use environment variables for sensitive data
- Review dependencies for vulnerabilities 