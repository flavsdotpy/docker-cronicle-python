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


ROOT_PYTHON_RUNTIME_PATH = Path("_runtime/python")
ROOT_SOURCE_SCRIPTS_PATH = Path("scripts/python")


try:
    stdinput = sys.stdin.readline()
    data = json.loads(stdinput)

    event_id = data["event"]
    source_script_path = data["params"]["scriptpath"]
    required_packages = data["params"]["requirements"].splitlines()
    environment_variables = data["params"]["environ"].splitlines()
    params = data["params"]["params"]

    job_script_path = Path(ROOT_PYTHON_RUNTIME_PATH / str(event_id) / source_script_path)
    job_runtime_path = job_script_path.parent
    if not job_runtime_path.exists():
        print(f"Initializing event runtime path: {job_runtime_path}")
        job_runtime_path.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT_SOURCE_SCRIPTS_PATH / source_script_path, job_script_path)
        open(job_runtime_path / "requirements.txt", 'w').close()
    elif (
        hashlib.md5(open(ROOT_SOURCE_SCRIPTS_PATH / source_script_path, "rb").read()).hexdigest() !=
        hashlib.md5(open(job_script_path,"rb").read()).hexdigest()
    ):
        print("Script changed... Updating...")
        shutil.copy2(ROOT_SOURCE_SCRIPTS_PATH / source_script_path, job_script_path)

    if required_packages:
        tmp_req_file = f"{uuid4()}.txt"
        with open(tmp_req_file, "w") as fout:
            fout.writelines(required_packages)
        if (
            hashlib.md5(open(job_runtime_path / "requirements.txt","rb").read()).hexdigest() !=
            hashlib.md5(open(tmp_req_file,"rb").read()).hexdigest()
        ):
            print("Installing dependencies...")
            print("")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-t", job_runtime_path, *required_packages])
            shutil.copy2(tmp_req_file, job_runtime_path / "requirements.txt")
        os.remove(tmp_req_file)

    env = os.environ.copy()
    if environment_variables:
        print("Setting up environment variables: ")
        for env_var in environment_variables:
            env_var_key, env_var_val = env_var.split("=")
            print(env_var_key)
            env[env_var_key] = env_var_val

    split_params = list()
    if params:
        split_params = shlex.split(params)

    subprocess.check_call([sys.executable, job_script_path, *split_params], env=env)

    print(json.dumps({
        "complete": 1
    }))
except Exception as e:
    print(json.dumps({
        "complete": 1,
        "code": 999,
        "description": str(e)
    }))
