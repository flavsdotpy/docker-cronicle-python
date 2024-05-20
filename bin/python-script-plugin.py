#!/usr/bin/env python
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from uuid import uuid4


PYTHON_RUNTIME_PATH = Path("_runtime/python")


try:
    stdinput = sys.stdin.readline()
    data = json.loads(stdinput)

    event_id = data["event"]
    script_path = data["params"]["scriptpath"]
    required_packages = data["params"]["requirements"].splitlines()
    environment_variables = data["params"]["environ"].splitlines()
    params = data["params"]["params"]

    event_runtime_path = PYTHON_RUNTIME_PATH / str(event_id)
    if not event_runtime_path.exists():
        print(f"Initializing event runtime path: {event_runtime_path}")
        event_runtime_path.mkdir(parents=True)
        shutil.copy2(f"scripts/python/{script_path}", event_runtime_path / script_path)
        open(event_runtime_path / "requirements.txt", 'w').close()
    elif (
        hashlib.md5(open(f"scripts/python/{script_path}","rb").read()).hexdigest() !=
        hashlib.md5(open(event_runtime_path / script_path,"rb").read()).hexdigest()
    ):
        print("Script changed... Updating...")
        shutil.copy2(f"scripts/python/{script_path}", event_runtime_path / script_path)

    if required_packages:
        tmp_req_file = f"{uuid4()}.txt"
        with open(tmp_req_file, "w") as fout:
            fout.writelines(required_packages)
        if (
            hashlib.md5(open(event_runtime_path / "requirements.txt","rb").read()).hexdigest() !=
            hashlib.md5(open(tmp_req_file,"rb").read()).hexdigest()
        ):
            print("Installing dependencies...")
            print("")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-t", event_runtime_path, *required_packages])
            shutil.copy2(tmp_req_file, event_runtime_path / "requirements.txt")
        os.remove(tmp_req_file)

    if environment_variables:
        print("Setting up environment variables: ")
        env = os.environ.copy()
        for env_var in environment_variables:
            env_var_key, env_var_val = env_var.split("=")
            print(env_var_key)
            env[env_var_key] = env_var_val

    split_params = list()
    if params:
        split_params = shlex.split(params)

    subprocess.check_call([sys.executable, event_runtime_path / script_path, *split_params], env=env)

    print('{ "complete": 1 }')
except:
    print('{ "complete": 1, "code": 999, "description": "Failed to execute." }')
