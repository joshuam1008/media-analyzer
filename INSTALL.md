Install as developer
============
These instructions assume that you are starting with a local copy of the source code tree, created by `git clone` or by unpacking a zipped/tarball copy. They also assume that Python 3.10 or greater is installed and accessible as `python`.

### Python venv
Create a virtualenv, probably in the source root directory:
```
python -m venv venv
```

Add `SECRET_KEY` and `BEAR_TOKEN` to local environment. The value of of `SECRET_KEY` can be generated in terminal with `openssl rand -base64 32`. A Twitter bearer token will need to be generated (https://developer.twitter.com/en/docs/authentication/oauth-2-0/bearer-tokens).
One way to add these to your local environment is to add them to the venv `activate` script.
```
export SECRET_KEY=""
export BEAR_TOKEN=""
```
where you add the values between the quotations.

Activate venv (linux/mac):
```bash
source venv/bin/activate
which python
# `which python` should now point to venv/bin/python 
```

Activate venv (Windows Powershell):
```powershell
.\venv\Scripts\Activate.ps1
# `where.exe python` should point to the venv's python binary
```

Install requirements for project:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
If there are errors with installing requirements, `postgresql@14` may need to be installed.

Run project:
```
python manage.py runserver
```

Run tests:
```
python manage.py test
```

Deactivate venv when finished:
```
deactivate
```

### Other notes
Wording based off of Github user joshuam1008 private project. Contact for more details.
