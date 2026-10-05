# FX3 프로젝트 작업 규칙

- 대화와 작업 보고는 한국어로 한다.
- 공식 프로젝트명은 `FreeLang FX3`다.
- AI가 `.fx3`를 생성·수정하기 전에 [AI-ENTRY.md](AI-ENTRY.md)를 앞에 둔다. Core 문법을 바꾸지 않는다.
- 사람 가독성은 목표가 아니다. AI 가독성을 우선한다. 의미 있는 이름은 유지한다.
- FX/FX1에서 가져오는 것은 [MINIMUM_FROM_FX.md](MINIMUM_FROM_FX.md)에 적힌 최소 형식뿐이다. 런타임, 앱, builtin 목록을 복사하지 않는다.
- FX2 소스를 가져오지 않는다.
- AFJ, AIA와 문법·런타임을 섞지 않는다.
- 부족한 기능은 JS/TS로 언어 본체를 대체하지 않는다. 부족한 층을 문서에 적는다.
- 문법 후보는 Hard Gate를 통과하기 전에 채택하지 않는다. `J`, `U`, `L`, `R`은 미확정이다.
- `.fx3`가 내려가는 `.fl`을 바꿀 때는 [LOWERING_CONTRACT.md](LOWERING_CONTRACT.md)와 fixture 01을 같이 고친다. 한 소스의 canonical `.fl`은 하나다.
- 검증은 실제 내리기와 실행 결과로 남긴다. 도구가 없으면 PASS라고 적지 않는다.
- Track 1 순서: lexer/parser → lowering/IR → capability → FX runtime → self-hosting. 한 층 PASS를 언어 완성으로 보고하지 않는다.
- P1–P4 게이트: `check_lex` · `check_parse` · `check_lower` · `check_ir` · `check_capability`.
- P5 CLI: `./bin/fx3` 또는 `python3 tools/fx3_cli.py` — `check`/`lower`/`ir`/`cap`/`run`/`test`/`package verify`. 문서 [docs/FX3-CLI.md](docs/FX3-CLI.md). CLI 스모크: `python3 tools/check_cli.py`.
- `fx3 run`은 위임 실행만이다 (`RUN=DELEGATED`). 계약 [docs/FX3-RUN.md](docs/FX3-RUN.md). 기본 `--engine=eval` (`eval_fl_ext` over `eval_fl_min`), 옵션 `native` (`fl-build.sh --no-net`). `RUNTIME_OWNED=NONE`.
- 위임 POC 레일: [poc/README.md](poc/README.md) · 한계 [docs/FX3-DELEGATED-LIMITS.md](docs/FX3-DELEGATED-LIMITS.md) · 게이트 `python3 tools/check_poc.py all`.

- Core fixture 레거시 내리기 회귀: `python3 tools/lower.py --check` (`tools/lower.py`는 수정하지 않는다).
- 새 AST lowering 본체는 `tools/fx3_lower.py`다. 동일 AST는 동일 `.fl` 바이트여야 한다. `run`도 이 경로만 쓴다.
- IR/ABI 계약은 [docs/IR-ABI-CONTRACT.md](docs/IR-ABI-CONTRACT.md)와 `tools/fx3_ir.py`다. P3는 계약 잠금이며 실행기가 아니다.
- Capability는 [docs/CAPABILITY-CONTRACT.md](docs/CAPABILITY-CONTRACT.md)와 `tools/fx3_capability.py`다. 기본 deny. P4는 판정만이며 대상 파일 I/O·실행이 아니다. `run`은 capability를 자동으로 켜지 않는다.
- P4 계약 리뷰: [docs/CAPABILITY-REVIEW.md](docs/CAPABILITY-REVIEW.md). IR `capability_request`·전용(owned) runtime은 보류.
- 「쓸 만한」1차 = CLI 게이트 + 위임 `run`. 전용 FX3 VM PASS로 보고하지 않는다.
- 비밀값, 토큰, 개인 키를 문서에 남기지 않는다.
