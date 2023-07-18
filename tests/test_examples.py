import os
import re
import subprocess
import tempfile
import textwrap

import pytest

SIGTECH_API_KEY = os.environ["SIGTECH_API_KEY"]

EXAMPLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../examples")
EXAMPLE_SCRIPTS = [
    os.path.abspath(os.path.join(EXAMPLES_DIR, o)) for o in os.listdir(EXAMPLES_DIR)
]

README_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../README.md")
with open(README_PATH, "r") as f:
    README_BODY = f.read()
SNIPPETS = re.findall(r"```python([\s\S]*?)```", README_BODY)
SNIPPETS = [textwrap.dedent(o).strip() for o in SNIPPETS]


@pytest.mark.parametrize("script", EXAMPLE_SCRIPTS)
def test_examples(script):
    if script.endswith(".py"):
        cmd = "python {{path}}"
    elif script.endswith(".ipynb"):
        cmd = "jupyter nbconvert --execute {{path}} --to notebook"
    else:
        raise NotImplementedError(f"Unknown file type {script}")
    with open(script, "r") as f:
        body = f.read()
    _run_script(body, cmd)


@pytest.mark.parametrize("snippet", SNIPPETS)
def test_readme_snippets(snippet):
    print(f"Testing snippet: {snippet}")
    _run_script(snippet)


def _run_script(script: str, cmd: str = "python {{path}}"):
    print(f"Running script={script} cmd={cmd}")
    script = script.replace("<YOUR_API_KEY>", SIGTECH_API_KEY)
    fp = tempfile.NamedTemporaryFile(mode="w", delete=False)
    fp.write(script)
    fp.close()
    cmd = cmd.replace("{{path}}", fp.name)
    try:
        stdout = subprocess.check_output(cmd, shell=True)
    finally:
        os.unlink(fp.name)
    print(f"Output: \n{stdout}")
