# Merkle

This collection of 3.6 scripts automates download, processing, and import into ActionKit of donation records from a vendor. `process.py` runs the entire process. Each step is in a separate file that can also be run independently. Each script can be run with `--help` to get info on the script and parameters. All parameters can be passed in directly or added to `settings.py`.

## Travis setup

Travis is setup to auto-deploy this repo on commits to the `main` branch. Deploying requires both `settings.py` and `zappa_settings.json`, which are excluded from the repo, but included in an encrypted tar file, `secrets.tar.enc`. If either of these files need to be updated, the process for updating what Travis uses for deploy is:

1. `tar cvf secrets.tar zappa_settings.json settings.py`
2. `travis encrypt-file secrets.tar --add`
3. `rm secrets.tar`
4. `git add .travis.yml`
5. `git add secrets.tar.enc`
