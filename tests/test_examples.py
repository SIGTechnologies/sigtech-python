import os
import platform
import re
import subprocess
import tempfile
import textwrap
from pathlib import Path
from typing import List

import pytest

SIGTECH_API_KEY = os.environ["SIGTECH_API_KEY"]
SIGTECH_ROOT_DIR = str(Path(__file__).parents[1].absolute())
if platform.system() == "Windows":
    SIGTECH_ROOT_DIR = SIGTECH_ROOT_DIR.replace("\\", "\\\\\\\\")

EXAMPLES_DIR = Path(__file__).parents[1] / "examples"


def _get_code_snippets_from_readme() -> List[str]:
    with open((Path(__file__).parents[1] / "README.md").absolute(), "r") as f:
        snippets = re.findall(r"```python([\s\S]*?)```", f.read())
        return [textwrap.dedent(o).strip() for o in snippets]


@pytest.mark.parametrize(
    "script",
    [
        pytest.param(p, id=p.name)
        for p in [
            file.absolute()
            for file in list(EXAMPLES_DIR.rglob("*.py"))
            + list(EXAMPLES_DIR.rglob("*.ipynb"))
        ]
    ],
)
def test_examples(script: Path):
    if script.suffix == ".py":
        cmd = "python {{path}}"
    elif script.suffix == ".ipynb":
        cmd = "jupyter nbconvert --execute {{path}} --to notebook"
    else:
        raise NotImplementedError(f"Unknown file type {script}")
    with open(script, "r") as f:
        body = f.read()
    _run_script(body, cmd)


@pytest.mark.parametrize("snippet", _get_code_snippets_from_readme())
def test_readme_snippets(snippet):
    print(f"Testing snippet: {snippet}")
    _run_script(snippet)


def _run_script(script: str, cmd: str = "python {{path}}"):
    print(f"Running script={script} cmd={cmd}")
    script = script.replace("<YOUR_API_KEY>", SIGTECH_API_KEY)
    script = script.replace("<SIGTECH_ROOT_DIR>", SIGTECH_ROOT_DIR)
    fp = tempfile.NamedTemporaryFile(mode="w", delete=False)
    fp.write(script)
    fp.close()
    cmd = cmd.replace("{{path}}", fp.name)
    try:
        stdout = subprocess.check_output(cmd, shell=True)
    finally:
        os.unlink(fp.name)
    print(f"Output: \n{stdout.decode()}")
