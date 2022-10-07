Install as Developer
============
These instructions assume that you are starting with a local copy of the source code tree, created by `git clone` or by unpacking a zipped/tarball copy. They also assume that Python 3.10 or greater is installed and accessible as `python`.

### Python venv
Create a virtualenv in the source root directory:
```
python -m venv venv
```

- Add `SECRET_KEY` and `BEAR_TOKEN` as environment variables. The value of `SECRET_KEY` can be generated in terminal with `openssl rand -base64 32`. A Twitter bearer token will need to be generated from here: https://developer.twitter.com/en/docs/authentication/oauth-2-0/bearer-tokens.
- You can automate this by adding the export commands to the venv `activate` script corresponding to your shell. The scripts are in `venv/bin`.
```
export SECRET_KEY="[KEY HERE]"
export BEAR_TOKEN="[TOKEN HERE]"
```

- Add the `src` `train` directories to your `PYTHONPATH`. This can be done from the root project directory with the following command, or added to the `activate` script as well (with modified paths).
```
export PYTHONPATH=$PYTHONPATH:$(pwd)/src:$(pwd)/train
```

- Activate venv.
    - Linux/Mac:
    ```bash
    source venv/bin/activate
    which python
    # `which python` should now point to venv/bin/python 
    ```
    - PowerShell:
    ```powershell
    .\venv\Scripts\Activate.ps1
    # `where.exe python` should point to the venv's python binary
    ```

You can leave the venv with
```bash
deactivate
```


### Install requirements

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run

Run server:
```
python src/media_analyzer/manage.py runserver
```

Run tests:
```
python src/media_analyzer/manage.py test
```
