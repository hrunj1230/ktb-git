---
name: ktb-git
description: >
  KTB Git-Flow 컨벤션으로 이슈, 브랜치, Conventional Commit, push, PR을 처리한다.
  Use when the user asks to create a branch, commit, open a PR, ship, start work,
  or mentions feat/fix/hotfix, conventional commits, or ktb. Also /ktb-git.
---

# ktb-git

팀 저장소에 이 도구를 설치하지 않는다. `git`과 `gh`로 컨벤션을 지킨다. 로컬에 `ktb` CLI가 있으면 그걸 써도 된다.

## 규칙

- 이슈 먼저, 그다음 브랜치. feat↔feat 직접 머지 금지. `main` 직접 push 금지.
- 브랜치: `feat|fix|hotfix/{nickname_slug}-{slug}`. feat/fix는 `origin/dev`에서, hotfix는 `origin/main`에서.
- PR base: feat/fix → `dev`, hotfix → `main`.
- 이슈 제목: `[분류][담당자] 작업 내용` (분류: feat fix chore refactor docs test hotfix)
- 커밋: `<type>[!]: <subject>` — subject 50자, 끝 마침표 없음. Breaking이면 body 필수, footer에 `BREAKING CHANGE:`.
- PR 제목: `[#이슈번호] 변경 사항 요약`. 본문은 아래 템플릿.
- 커밋 전: `uv run ruff check --fix . && uv run ruff format .`
- PR 전: `uv run ruff format --check . && uv run ruff check .` (실패하면 push/PR 하지 않음)
- `--skip-ruff`는 사용자가 명시할 때만.

닉네임: `~/.config/ktb/config.toml`의 `nickname`, `nickname_slug`. 없으면 한 번 묻고 저장. 한글 표시명이면 slug는 `[a-z0-9]+`를 직접 받는다.

이슈 번호는 `git config branch.<name>.ktbIssue`에 저장한다.

## 프로젝트 연결 (모든 작업 전)

이미 되어 있으면 확인하고 넘어간다. 스킬 설치와 프로젝트 remote는 별개다.

1. `git rev-parse --show-toplevel` 성공이면 git 저장소다. 실패면 사용자 확인 후 `git init`.
2. `git remote get-url origin` 성공이면 `origin 연결됨: <url>`을 보여 주고 다음으로.
3. origin이 없으면 사용자에게 고른다.
   - Git URL 입력: `https://github.com/owner/repo.git` 또는 `git@github.com:owner/repo.git`. 형식이 아니면 다시 묻는다. `git remote add origin <url>`.
   - 새로 만들기: 저장소 이름과 공개/비공개를 묻고 `gh repo create <name> --private|--public --source . --remote origin`.
4. start/ship이면 `gh auth status`. 실패 시 `gh auth login` 안내 후 중단.
5. start에서 `git fetch origin`이 실패해도(빈 원격) 중단하지 않는다. `origin/dev`(hotfix는 `origin/main`)가 있으면 그걸 베이스로 쓰고, 없으면 로컬 `dev`/`main`, 그것도 없으면 현재 HEAD에서 분기한다고 알린다.

## 흐름

1. **start** — 프로젝트 연결 확인 → 새 이슈 또는 열린 이슈 선택 → 브랜치 종류 확정(fix/hotfix만 이슈 분류를 따르고 나머지는 feat, 사용자가 바꿀 수 있음) → fetch 후 베이스 체크아웃 → `git checkout -b` → ktbIssue 저장. push 하지 않음.
2. **commit** — git 저장소만 있으면 된다(remote 불필요). 변경 없으면 중단. main에서 커밋 거부. ruff 수정 후 스테이징 → 메시지 미리보기 → `git commit -F`. push 하지 않음.
3. **ship** — 프로젝트 연결 확인 → main/dev에서 거부. 베이스보다 앞선 커밋 없으면 거부. ruff 검사 실패면 중단. `git push -u origin HEAD`. 기존 PR 있으면 URL만. 없으면 `gh pr create --base <dev|main>`.

## PR 본문

```markdown
## 🔗 관련 이슈
- closes #<이슈번호>

## ✨ 변경 내용
- ...

## ✅ 체크리스트
- [ ] 로컬에서 빌드/테스트 통과
- [ ] 관련 문서(README, API 문서 등) 업데이트
- [ ] Breaking Change 여부 확인 (있다면 아래에 명시)

## ⚠️ Breaking Change (선택)
- ...

## 📌 기타 참고 사항 (선택)
- ...
```

체크리스트의 빌드 항목은 ruff 검사가 통과하면 체크한다.

## CLI (선택)

에이전트가 없을 때 터미널 마법사:

```sh
uv tool install git+https://github.com/hrunj1230/ktb-git
ktb
```
