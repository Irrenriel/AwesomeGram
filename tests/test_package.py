# -*- coding: utf-8 -*-
"""
Tests for the awesomegram package and its CLI (start-project).

Run: uv sync && uv run pytest   (or: pip install -e . pytest && python -m pytest)
"""
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / 'awesomegram' / 'templates'


def awesomegram(cwd: Path, *args: str, env: dict = None) -> subprocess.CompletedProcess:
    # Same entry point as the installed 'awesomegram' console script, but from the source tree
    code = 'import sys, awesomegram; sys.argv = ["awesomegram", *sys.argv[1:]]; awesomegram.main()'
    return subprocess.run(
        [sys.executable, '-c', code, *args], cwd=cwd, capture_output=True, text=True, timeout=60,
        env={**os.environ, 'PYTHONPATH': str(ROOT), **(env or {})},
    )


def read_settings(project: Path, cwd: Path, env: dict = None) -> str:
    code = 'import settings; print(settings.DEBUG, settings.BOTS[0]["TOKEN"], settings.DATABASE_CONNECT)'
    result = subprocess.run(
        [sys.executable, '-W', 'error::DeprecationWarning', '-c', code], cwd=cwd, capture_output=True, text=True,
        timeout=60, env={**os.environ, 'PYTHONPATH': str(project), **(env or {})},
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def test_version(tmp_path):
    result = awesomegram(tmp_path, '--version')

    assert result.returncode == 0, result.stderr
    assert result.stdout.startswith('AwesomeGram ')


def test_start_project_creates_files(tmp_path):
    result = awesomegram(tmp_path, 'start-project', 'MyBotProject')

    assert result.returncode == 0, result.stderr
    project = tmp_path / 'mybotproject'
    assert sorted(p.name for p in project.iterdir()) == ['.env.example', '.gitignore', 'Dockerfile', 'settings.py']
    assert '.env' in (project / '.gitignore').read_text(encoding='utf-8').splitlines()


@pytest.mark.parametrize('name', ['my bot x', 'bot-project', '1botproject', 'import', 'short'])
def test_start_project_rejects_invalid_names(tmp_path, name):
    result = awesomegram(tmp_path, 'start-project', name)

    assert result.returncode != 0
    assert list(tmp_path.iterdir()) == []


def test_start_project_keeps_existing_files(tmp_path):
    assert awesomegram(tmp_path, 'start-project', 'mybotproject').returncode == 0
    settings = tmp_path / 'mybotproject' / 'settings.py'
    settings.write_text('# user settings\n', encoding='utf-8')

    assert awesomegram(tmp_path, 'start-project', 'mybotproject').returncode == 0

    assert settings.read_text(encoding='utf-8') == '# user settings\n'


def test_settings_read_env_file_and_environment(tmp_path):
    assert awesomegram(tmp_path, 'start-project', 'mybotproject').returncode == 0
    project = tmp_path / 'mybotproject'
    elsewhere = tmp_path / 'elsewhere'
    elsewhere.mkdir()

    assert read_settings(project, elsewhere) == 'True  postgresql+asyncpg://user:password@host:port/database'

    (project / '.env').write_text('DEBUG=false\nBOT_TOKEN=42:FILE\nDATABASE_CONNECT=sqlite:///db\n', encoding='utf-8')
    assert read_settings(project, elsewhere) == 'False 42:FILE sqlite:///db'
    assert read_settings(project, elsewhere, env={'BOT_TOKEN': '42:VAR'}) == 'False 42:VAR sqlite:///db'


@pytest.mark.skipif(shutil.which('uv') is None, reason='uv is needed to build the wheel')
def test_wheel_contains_all_templates(tmp_path):
    result = subprocess.run(
        ['uv', 'build', '--wheel', '--out-dir', str(tmp_path), str(ROOT)], capture_output=True, text=True, timeout=300
    )
    assert result.returncode == 0, result.stderr

    (wheel,) = tmp_path.glob('*.whl')
    names = set(zipfile.ZipFile(wheel).namelist())
    templates = {p.relative_to(ROOT).as_posix() for p in TEMPLATES.rglob('*') if p.is_file()}
    assert templates and templates <= names, templates - names
    assert not any(n.startswith(('resources/', 'tests/')) for n in names)
