# ktb-git

KTB Git-Flow 컨벤션(이슈 → 브랜치 → Conventional Commit → `dev` PR)을 지키는 도구입니다.

팀 프로젝트 저장소에 패키지로 넣지 않습니다. 에이전트 스킬로 쓰거나, 필요할 때만 로컬 CLI로 실행합니다.

## 에이전트 스킬 (권장)

Grok / Claude가 커밋·브랜치·PR을 대신할 때 이 스킬을 로드합니다.

```sh
git clone https://github.com/hrunj1230/ktb-git.git ~/Documents/ktb-git
mkdir -p ~/.grok/skills ~/.claude/skills
ln -sfn ~/Documents/ktb-git/skills/ktb-git ~/.grok/skills/ktb-git
ln -sfn ~/Documents/ktb-git/skills/ktb-git ~/.claude/skills/ktb-git
```

이후 프로젝트에서 "브랜치 파줘", "커밋해줘", "dev로 PR 올려줘"라고 하면 컨벤션을 따릅니다.

## 터미널 CLI (선택)

에이전트 없이 터미널에서 마법사를 쓰려면:

```sh
uv tool install git+https://github.com/hrunj1230/ktb-git
gh auth login
ktb init
ktb
```

프로젝트 디렉터리에 의존성을 추가하지 마세요.

## 규칙 요약

| 작업 | 형식 |
|---|---|
| 이슈 | `[feat][가넷] 로그인 구현` |
| 브랜치 | `feat/garnet-login` (`dev`에서, PR도 `dev`) |
| hotfix | `hotfix/garnet-login` (`main`에서, PR도 `main`) |
| 커밋 | `feat: 로그인 기능` / Breaking은 `feat!: ...` |
| PR | `[#12] 로그인 기능 구현` |

커밋 전: `uv run ruff check --fix . && uv run ruff format .`  
PR 전: `uv run ruff format --check . && uv run ruff check .`
