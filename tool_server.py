import os
import subprocess
import json

BASE_PROJECTS = r"C:\ai_system\projects"

def safe_path(path):
    full = os.path.abspath(path)

    if not full.startswith(BASE_PROJECTS):
        raise Exception("Unsafe path")

    return full


def create_file(path, content):

    path = safe_path(path)

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return {"status": "success", "file": path}


def read_file(path):

    path = safe_path(path)

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def run_command(command, cwd):

    cwd = safe_path(cwd)

    result = subprocess.run(
        command,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True
    )

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "code": result.returncode
    }


if __name__ == "__main__":

    print("AI Tool Server Ready")