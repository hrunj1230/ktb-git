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

## 흐름

1. **start** — 새 이슈 또는 열린 이슈 선택 → 브랜치 종류 확정(fix/hotfix만 이슈 분류를 따르고 나머지는 feat, 사용자가 바꿀 수 있음) → fetch 후 베이스 체크아웃 → `git checkout -b` → ktbIssue 저장. push 하지 않음.
2. **commit** — 변경 없으면 중단. main에서 커밋 거부. ruff 수정 후 스테이징 → 메시지 미리보기 → `git commit -F`. push 하지 않음.
3. **ship** — main/dev에서 거부. 베이스보다 앞선 커밋 없으면 거부. ruff 검사 실패면 중단. `git push -u origin HEAD`. 기존 PR 있으면 URL만. 없으면 `gh pr create --base <dev|main>`.

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
