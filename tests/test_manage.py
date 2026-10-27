# -*- coding: utf-8 -*-
"""
Smoke tests for manage.py: every command runs on a fresh copy of the repository
and the generated files at least compile.

Run: pip install -r requirements.txt pytest aiosqlite && python -m pytest tests
(aiosqlite is optional: without it the async DB test is skipped)
"""
import os
import py_compile
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def project(tmp_path: Path) -> Path:
    # A dot in the path on purpose: it used to break file/directory checks
    dst = tmp_path / 'my.bot'
    shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns('.git', 'tests', '__pycache__', 'venv', '.venv'))
    return dst


def manage(project: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, 'manage.py', *args], cwd=project, capture_output=True, text=True, timeout=60
    )


def assert_ok(result: subprocess.CompletedProcess):
    assert result.returncode == 0, result.stderr
    assert 'Traceback' not in result.stderr, result.stderr


def assert_compiles(*files: Path):
    for file in files:
        py_compile.compile(str(file), doraise=True)


def test_help_lists_all_commands(project):
    result = manage(project, '--help')

    assert_ok(result)
    for command in ('--create-module', '--create-app', '--init-db', '--create-model'):
        assert command in result.stderr


def test_create_module_without_name_fails_with_clear_error(project):
    result = manage(project, '--create-module')

    assert result.returncode != 0
    assert 'ArgumentValueNotFound' in result.stderr


def test_create_modules_and_app(project):
    assert_ok(manage(project, '--create-module', 'first'))
    (project / 'modules' / '__pycache__').mkdir()  # appears after any import of modules.config
    assert_ok(manage(project, '--create-module', 'second'))
    assert_ok(manage(project, '--create-app'))

    installing = (project / 'modules' / 'installing.py').read_text(encoding='utf-8')
    assert 'install_first_handlers' in installing and 'install_second_handlers' in installing
    assert '__pycache__' not in installing
    assert "default_locale = 'EN'" in (project / 'app.py').read_text(encoding='utf-8')
    assert (project / 'resources' / 'locales' / 'en.yml').is_file()
    assert_compiles(
        project / 'app.py',
        project / 'modules' / 'installing.py',
        project / 'modules' / 'first' / 'handlers.py',
        project / 'resources' / 'middlewares' / 'main_middleware.py',
    )


@pytest.mark.parametrize('async_mode', ['false', 'true'])
def test_init_db(project, async_mode):
    assert_ok(manage(project, '--create-module', 'first'))

    assert_ok(manage(project, '--init-db', f'async={async_mode}'))

    assert_compiles(project / 'core' / 'database' / 'db.py')


def test_create_model(project):
    assert_ok(manage(project, '--create-module', 'first'))
    assert_ok(manage(project, '--init-db'))

    result = manage(project, '--create-model', 'user', 'id:int:primary', 'name:text:null', 'created_at:datetime:utc')

    assert_ok(result)
    model = project / 'resources' / 'models' / 'tables' / 'user_model.py'
    assert_compiles(model)
    assert 'default=lambda: datetime.now(UTC)' in model.read_text(encoding='utf-8')


@pytest.mark.parametrize(
    ('field', 'error'),
    [('name:varchar:null', 'UnknownColumnType'), ('name:text:uniq', 'UnknownColumnOption')],
)
def test_create_model_rejects_unknown_type_and_option(project, field, error):
    assert_ok(manage(project, '--create-module', 'first'))
    assert_ok(manage(project, '--init-db'))

    result = manage(project, '--create-model', 'user', 'id:int:primary', field)

    assert result.returncode != 0
    assert error in result.stderr


def run_python(project: Path, code: str, cwd: Path) -> subprocess.CompletedProcess:
    # Run code against the generated project from another cwd, like a real deployment
    env = {**os.environ, 'PYTHONPATH': str(project)}
    return subprocess.run([sys.executable, '-c', code], cwd=cwd, env=env, capture_output=True, text=True, timeout=60)


def test_generated_app_starts_with_config_from_env_file(project, tmp_path):
    assert_ok(manage(project, '--create-module', 'first'))
    assert_ok(manage(project, '--create-app'))
    (project / '.env').write_text('BOT_TOKEN=42:TEST\nPARSE_MODE=MarkdownV2\n', encoding='utf-8')

    # No network: only Bot creation, locales and handlers installation
    result = run_python(
        project, 'import asyncio, app; asyncio.run(app.startup_func(app.dp)); print(app.bot.default.parse_mode)', tmp_path
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == 'MarkdownV2'
    assert 'Deprecat' not in result.stderr, result.stderr


DB_CHECK = '''
import asyncio
from sqlalchemy import select, update
import core.database.db as db
from resources.models.tables.note_model import NoteModel

async def main():
    if {is_async}:
        async with db.Engine.begin() as conn:
            await conn.run_sync(db.Base.metadata.create_all)
        async with db.AsyncSessionContext() as session:
            session.add(NoteModel(id=1, body='x'))
        await db.Base.execute(update(NoteModel).values(body='y'))
        rows = (await db.Base.execute(select(NoteModel))).scalars().all()
    else:
        db.Base.metadata.create_all(db.Engine)
        with db.SessionContext() as session:
            session.add(NoteModel(id=1, body='x'))
        db.Base.execute(update(NoteModel).values(body='y'))
        rows = db.Base.execute(select(NoteModel)).scalars().all()
    print([(r.body, r.created_at is not None) for r in rows])

asyncio.run(main())
'''


@pytest.mark.parametrize('async_mode', [False, True])
def test_generated_db_layer_writes_and_reads(project, tmp_path, async_mode):
    if async_mode:
        pytest.importorskip('aiosqlite')
    driver = 'sqlite+aiosqlite' if async_mode else 'sqlite'
    assert_ok(manage(project, '--create-module', 'first'))
    (project / '.env').write_text(f'DB_CONNECT={driver}:///{tmp_path / "test.db"}\n', encoding='utf-8')
    assert_ok(manage(project, '--init-db', f'async={str(async_mode).lower()}'))
    assert_ok(manage(project, '--create-model', 'note', 'id:int:primary', 'body:text:null', 'created_at:datetime:utc'))

    result = run_python(project, DB_CHECK.format(is_async=async_mode), tmp_path)

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "[('y', True)]"
