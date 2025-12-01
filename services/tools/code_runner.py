import subprocess, tempfile, os, uuid


# WARNING: This is only for trusted code snippets in dev. Do NOT run untrusted code like this in prod.


def run_python_code(code: str, timeout=5):
    fname = f"/tmp/{uuid.uuid4().hex}.py"
    with open(fname, "w") as f:
        f.write(code)
    try:
        res = subprocess.run(["python3", fname], capture_output=True, text=True, timeout=timeout)
        return {"stdout": res.stdout, "stderr": res.stderr, "returncode": res.returncode}
    finally:
        try:
            os.remove(fname)
        except Exception:
            pass
