from __future__ import annotations

import re

from ktb_git import github, gitops
from ktb_git.errors import KtbError
from ktb_git.runner import Runner
from ktb_git.wizard import Choice, Wizard

_REMOTE_URL_RE = re.compile(
    r"^(https://[^\s]+|git@[^\s]+:[^\s]+|ssh://[^\s]+)$",
    re.IGNORECASE,
)


def validate_remote_url(url: str) -> str:
    cleaned = url.strip()
    if not cleaned or not _REMOTE_URL_RE.fullmatch(cleaned):
        raise KtbError("Git 원격 URL을 입력하세요. 예: https://github.com/owner/repo.git")
    return cleaned


def resolve_base_ref(runner: Runner, preferred: str) -> str:
    if gitops.ref_exists(runner, preferred):
        return preferred
    local = preferred.removeprefix("origin/")
    if gitops.ref_exists(runner, local):
        print(f"원격 {preferred}가 없어 로컬 {local}을 기준으로 합니다.")
        return local
    if gitops.ref_exists(runner, "HEAD"):
        print(f"원격 {preferred}가 없어 현재 HEAD에서 분기합니다.")
        return "HEAD"
    raise KtbError(f"{preferred}도 로컬 베이스도 없습니다. 커밋을 만든 뒤 다시 시도하세요.")


def ensure_project(
    runner: Runner,
    wizard: Wizard,
    *,
    need_remote: bool,
    need_gh: bool,
    dry_run: bool = False,
) -> None:
    if not gitops.is_repo(runner):
        if not wizard.confirm("git_init", "Git 저장소가 아닙니다. 여기서 git init 할까요?", default=True):
            raise KtbError("Git 저장소 안에서 실행하세요.")
        gitops.init_repo(runner, dry_run=dry_run)
        print("git init 완료")
    if need_gh or need_remote:
        github.ensure_gh(runner)
    if not need_remote:
        return
    existing = gitops.origin_url(runner)
    if existing:
        print(f"origin 연결됨: {existing}")
        return
    mode = wizard.select(
        "remote_mode",
        "원격 저장소가 없습니다. 어떻게 연결할까요?",
        [
            Choice("Git URL 입력", "url"),
            Choice("gh로 GitHub 저장소 만들기", "create"),
        ],
        default="url",
    )
    if mode == "create":
        name = wizard.text("repo_name", "GitHub 저장소 이름 (owner/repo 또는 repo):").strip()
        while not name:
            print("저장소 이름은 비울 수 없습니다.")
            name = wizard.text("repo_name", "GitHub 저장소 이름 (owner/repo 또는 repo):").strip()
        private = wizard.confirm("repo_private", "비공개 저장소로 만들까요?", default=True)
        github.create_remote_repo(runner, name, private=private, dry_run=dry_run)
        print("GitHub 저장소를 만들고 origin에 연결했습니다.")
        return
    while True:
        raw = wizard.text(
            "origin_url",
            "Git 원격 URL:",
            default="",
        ).strip()
        try:
            url = validate_remote_url(raw)
            break
        except KtbError as exc:
            print(exc)
    gitops.add_origin(runner, url, dry_run=dry_run)
    print(f"origin 연결: {url}")
