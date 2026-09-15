from pathlib import Path

import pytest

from ktb_git.bootstrap import ensure_project, validate_remote_url
from ktb_git.errors import KtbError
from ktb_git.runner import Completed, FakeRunner
from ktb_git.wizard import FakeWizard


def test_validate_remote_url() -> None:
    assert validate_remote_url("https://github.com/owner/repo.git") == "https://github.com/owner/repo.git"
    assert validate_remote_url("git@github.com:owner/repo.git") == "git@github.com:owner/repo.git"
    with pytest.raises(KtbError):
        validate_remote_url("not a url")


def test_existing_origin_skips_prompt(tmp_path: Path) -> None:
    runner = FakeRunner()
    runner.script(
        ["git", "rev-parse", "--show-toplevel"],
        Completed([], 0, f"{tmp_path}\n", ""),
    )
    runner.script(
        ["git", "remote", "get-url", "origin"],
        Completed([], 0, "https://github.com/owner/repo.git\n", ""),
    )
    wizard = FakeWizard({})

    ensure_project(runner, wizard, need_remote=True, need_gh=True)

    assert ["git", "remote", "add"] not in [call[:3] for call in runner.calls]
    assert not wizard.calls


def test_missing_origin_adds_url(tmp_path: Path) -> None:
    runner = FakeRunner()
    runner.script(
        ["git", "rev-parse", "--show-toplevel"],
        Completed([], 0, f"{tmp_path}\n", ""),
    )
    runner.script(
        ["git", "remote", "get-url", "origin"],
        Completed([], 1, "", "not found"),
    )
    wizard = FakeWizard(
        {
            "remote_mode": ["url"],
            "origin_url": ["https://github.com/owner/repo.git"],
        }
    )

    ensure_project(runner, wizard, need_remote=True, need_gh=True)

    assert ["git", "remote", "add", "origin", "https://github.com/owner/repo.git"] in runner.calls


def test_not_a_repo_inits_then_adds_origin() -> None:
    runner = FakeRunner()
    runner.script(
        ["git", "rev-parse", "--show-toplevel"],
        Completed([], 128, "", "not a git repo"),
    )
    runner.script(
        ["git", "remote", "get-url", "origin"],
        Completed([], 1, "", "not found"),
    )
    wizard = FakeWizard(
        {
            "git_init": [True],
            "remote_mode": ["url"],
            "origin_url": ["https://github.com/owner/new.git"],
        }
    )

    ensure_project(runner, wizard, need_remote=True, need_gh=True)

    assert ["git", "init"] in runner.calls
    assert ["git", "remote", "add", "origin", "https://github.com/owner/new.git"] in runner.calls
