# Setup for Visual Studio Code Environment

## 1. Install the following extensions

- `ms-python.python`: v2022.14.0
- `ms-python.vscode-pylance`: v2022.9.40

## 2. Use the **Black** formatter

Add the following to your `settings.json`:

```json
"[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
}
```

## 3. Use the **flake8** linter

Open the Command Palette (**Ctrl/⌘+Shift+P** by default) and choose **Python: Select Linter** $\rightarrow$ **flake8**.

# Install mypy for style check and Linting

## 1. Install mypy
```python
pip install mypy
```

## 2. Add Gitlens extension
https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens

## 3. Add these settings in your local settings.json
```json
{
  "python.linting.mypyEnabled": true,
  "python.linting.mypyArgs": [
    "--ignore-missing-imports",
    "--follow-imports=silent",
    "--show-column-numbers",
    "--allow-untyped-defs",
    "--allow-subclassing-any",
    "--allow-untyped-calls",
    "--strict"
  ]
}
```
