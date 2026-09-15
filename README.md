# ktb-git

KTB Git-Flow 컨벤션(이슈 → 브랜치 → Conventional Commit → `dev` PR)을 지키는 도구입니다.

팀 프로젝트 저장소에 패키지로 넣지 않습니다. 에이전트 스킬로 쓰거나, 필요할 때만 로컬 CLI로 실행합니다.

## 에이전트 스킬 (권장)

팀 저장소에 패키지를 설치하지 않습니다. 각자 에이전트가 읽는 스킬 폴더에 `SKILL.md`만 두면 됩니다.

| 에이전트 | 넣는 위치 |
|---|---|
| Grok | `~/.grok/skills/ktb-git/SKILL.md` |
| Claude Code | `~/.claude/skills/ktb-git/SKILL.md` |
| Cursor | `~/.cursor/skills/ktb-git/SKILL.md` |

### 개인 등록

쓰는 에이전트만 연결하면 됩니다. 심볼릭 링크라 나중에 `git pull`하면 스킬도 같이 갱신됩니다.

```sh
git clone https://github.com/hrunj1230/ktb-git.git ~/Documents/ktb-git
mkdir -p ~/.grok/skills ~/.claude/skills ~/.cursor/skills
ln -sfn ~/Documents/ktb-git/skills/ktb-git ~/.grok/skills/ktb-git
ln -sfn ~/Documents/ktb-git/skills/ktb-git ~/.claude/skills/ktb-git
ln -sfn ~/Documents/ktb-git/skills/ktb-git ~/.cursor/skills/ktb-git
```

에이전트 세션을 한 번 다시 시작합니다. Grok이면 `/skills`에 `ktb-git`이 보이면 된 겁니다. `/ktb-git`으로 직접 호출하거나, "브랜치 파줘", "커밋해줘", "dev로 PR 올려줘"라고 하면 컨벤션을 따릅니다.

### 프로젝트에 넣고 싶다면

레포 안에 스킬만 두면 클론한 사람 전원에게 적용됩니다.

```text
<팀레포>/.grok/skills/ktb-git/SKILL.md
```

Claude Code는 `.claude/skills/ktb-git/`, Cursor는 `.cursor/skills/ktb-git/` 입니다.

`grok plugin install hrunj1230/ktb-git` 은 아직 해당 없습니다. 플러그인 형식(`plugin.json`)으로 올리지 않았습니다.

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
