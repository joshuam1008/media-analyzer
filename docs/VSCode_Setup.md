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
