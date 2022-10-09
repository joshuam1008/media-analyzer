Install as Developer
============
These instructions assume that you are starting with a local copy of the source code tree, created by `git clone` or by unpacking a zipped/tarball copy. They also assume that Python 3.10 or greater is installed and accessible as `python`.

### Set up virtual environment

1. Create a virtualenv in the root directory.
   ```bash
   python -m venv venv
   ```

2. Add `SECRET_KEY` and `BEAR_TOKEN` as environment variables.
   <details>
     <summary>Bash</summary>

      ```bash
      export SECRET_KEY="[KEY HERE]"
      export BEAR_TOKEN="[TOKEN HERE]"
      ```
   </details>
   
   <details>
     <summary>PowerShell</summary>
     
      ```powershell
      $env:SECRET_KEY = '[KEY HERE]'
      $env:BEAR_TOKEN = '[TOKEN HERE]'
      ```
   </details>   
   
   - You can automate this by adding the export commands to the venv `activate` script corresponding to your shell. The scripts are in `venv/bin`.
   - The value of `SECRET_KEY` can be generated in a terminal with
      ```bash
      openssl rand -base64 32
      ```
   A Twitter bearer token will need to be generated from here: https://developer.twitter.com/en/docs/authentication/oauth-2-0/bearer-tokens.

3. Set up Python module paths.

   - Add the required directories to your `PYTHONPATH`. This can be done from the root project directory with the following command, or added to the `activate` script.
   
   <details>
     <summary>Bash</summary>

      ```bash
      export PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/src:$(pwd)/train:$(pwd)/src/media_analyzer
      ```
   </details>
   
   <details>
     <summary>PowerShell</summary>
     
      ```powershell
      $env:PYTHONPATH += '$($pwd.path);$($pwd.path)\src;$($pwd.path)\train;$($pwd.path)\src\media_analyzer'
      ```
   </details>
   
4. Activate venv.

   <details>
     <summary>Bash</summary>

      ```bash
      source venv/bin/activate
      which python
      # `which python` should now point to venv/bin/python 
      ```
   </details>
   
   <details>
     <summary>PowerShell</summary>
     
      ```powershell
      .\venv\Scripts\Activate.ps1
      # `where.exe python` should point to the venv's python binary
      ```
   </details>
    
   You can leave the venv with `deactivate`.
    
    
## Install dependencies

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run

- Run server:
  ```
  python src/media_analyzer/manage.py runserver
  ```

- Run tests:
  ```
  python src/media_analyzer/manage.py test
  ```
  
  Visit http://localhost:8000/twitter.
