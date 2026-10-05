# FreeLang FX3 현재 상태

기준일: 2026-09-29

```text
PROJECT=PREPARED
IMPLEMENT=NO
SOURCE_COPY=NO
FX3_SURFACE=.fx3
CANONICAL_LOWERING=.fl
RUNTIME=NONE
RUNTIME_OWNED=NONE
RUN=DELEGATED
RUN_ENGINE_DEFAULT=eval
RUN_ENGINE_NATIVE=OPTIONAL
PARSER=AST_SKELETON
PARSER_AST=PASS
LOWER_AST=PASS
IR_ABI=LOCKED_V1
CAPABILITY=LOCKED_DENY_FIRST_V1
TRACK1=OPEN
TRACK1_P0=CORE_LOCKED
TRACK1_P1=PARSER_AST_PASS
TRACK1_P2=LOWER_AST_PASS
TRACK1_P3=IR_ABI_PASS
TRACK1_P4=CAPABILITY_PASS
TRACK1_P5=CLI_PASS
TRACK1_RUN=DELEGATED_PASS

REMOTE=https://github.com/kimjindol2025/freelang-fx3
LOWERING_CONTRACT=LOCKED
CORE=LOCKED
USER_01=CONTINUE
CORE_DENSITY=GOOD
SEMANTIC_NAMES=KEEP
VAR_SIGIL=KEEP
EXPR_END=;
HOT_ALIAS=OPTIONAL_ONLY
MAIN_REQUEST=MAKE_RULES_EXCEPTIONLESS
FORMATTER=SPLIT_ON_SEMI_ONLY
DENSITY_CEILING=FIXTURE_01
FIXTURE_02=GOLDEN
NEXT_PROOF=SEMI_DISPLAY_DONE
LOWERER=BYTE_CHECK_01_04_PASS
LOWERING_01_04=PASS
INVALID_BINDING=REJECTED
CORE_V0_FINAL=PASS
SEMANTIC_EXECUTION=NARROW_PASS
USER_2_MIN_IMPL=AGREE
USER_3_MIN_IMPL=AGREE
BYTE_CHECK=CLOSED_PASS
BYTE_MATCH=PASS
FX_EXECUTION=NOT_OPENED
STAGE_MIN_IMPL=CLOSED
USER_1=AGREE
USER_2=AGREE
USER_3=AGREE
NO_SURFACE_RUNTIME=YES
BINDING=LEADING_ONLY
TOPLEVEL_SEMI=REQUIRED
STRUCTURE=DRAFT
CORE_ALIAS_SPLIT=YES
GOLDEN_FIXTURES=04
FIXTURE_01=KEEP
FIXTURE_02=KEEP
FIXTURE_03=KEEP
FIXTURE_04=INDEX
MAP_BLOCK_DISTINCTION=CLEAR
SEMICOLON_FORMATTING=GOOD
SEMICOLON=STRONG_KEEP
QUESTION_MARK=KEEP
FX3_AS_LANGUAGE=CORE_V1_LOCKED
GROK_USER=FIVE_RULES
NO_NEW_RUNTIME=YES
NO_PRETTIER=YES
NO_SHORTER=YES
FX3_CORE_01=KEEP
NEXT_USER_TEST=READ_FIXTURE_01_04_PASS
GROK_FIXTURE_04=KEEP
GROK_NEXT=LOWER_FOUR
INDEX_KEY=ANY_EXPR
NO_FIXTURE_05=YES
APP_MIGRATION=NOT_YET
SYMBOL_CLUSTER=?~ WATCH
ABBREVIATION=UNFIXED
FX2_IMPORT=NO
REFERENCE_PIN=freelang-v11-fx@202c998
AI_ENTRY=AI-ENTRY.md
AI_ENTRY_PURPOSE=FIRST_PASS_CONTRACT
AI_METRICS=bench/metrics
AI_METRICS_TOKENIZER=USAGE_EVENTS_ONLY
DIALECT_FX3_CORE=DIALECT-FX3-CORE.md
DIALECT_OTHERS=NOT_OPENED
AI_USE_SUCCESS=AI-USE-SUCCESS.md
AI_USE_SUCCESS_LOCK=AI_USE_SUCCESS_V0
DIRECTION=AI_USE_FIRST
U1_SMOKE=bench/results/u1-smoke-20260929
U1_SMOKE_VERDICT=PASS_6_OF_6
U2_SMOKE=bench/results/u2-smoke-20260929
U2_SMOKE_VERDICT=PASS_3_OF_3
U3_SMOKE=bench/results/u3-smoke-20260929
U3_SMOKE_VERDICT=PASS_6_OF_6_ENTRY_SAME
U1_WEAK=bench/results/u1-weak-20260929
U1_WEAK_VERDICT=PASS_6_OF_6
OTHER_MODEL_REPLAY=bench/results/other-model-20260929
OTHER_MODEL=gpt-5.6-luna
OTHER_MODEL_VERDICT=PASS_U1_5_OF_6_U2_3_OF_3_U3_6_OF_6
U1_OPS_HOLE=bench/results/u1-ops-20260930
U1_OPS_HOLE_VERDICT=PASS_5_OF_6
SESSION_CLOSE=2026-09-30
FLOOR=PASS
DELIMITER_TRAILING_SEMI=CLOSED_PASS
DELIMITER_ROOT_CAUSE=IDENT_HYPHEN_BEFORE_DOLLAR
OPS_HOLE_AFTER_FIX=6_OF_6
SEMANTIC_MIN=PASS
FX_NATIVE_ELF=PASS
FX_NATIVE_HARNESS=tools/check_semantic_native.sh
FX_BUILD_FIX=freelang-v11-fx/fl-build.sh_CGC_DISCOVERY
HANDOFF=RUN_DELEGATED=PASS (eval default + optional native). RUNTIME_OWNED=NONE. NEXT=NEW_ROAD_ONLY
NEXT_AGENDA_ONLY=NEW_ROAD_ONLY
ROAD_USABLE_CLI=PASS
ROAD_DELEGATED_RUN=PASS
ROAD_STEP=S7_PASS
ROAD_SUCCESS=fx3_check_lower_ir_cap_run_test
CLI=PASS
CLI_CMD=./bin/fx3
CLI_GATE_CMD=python3 tools/check_cli.py
RUN_DOC=docs/FX3-RUN.md
RUN=DELEGATED
RUN_ENGINE_DEFAULT=eval
RUN_ENGINE_NATIVE=OPTIONAL
RUNTIME_OWNED=NONE
MAX_OUTPUT_BYTES=262144
CAPABILITY_COMBO_ESCALATION=LOCKED_DENY
RUNTIME=NONE
CAPABILITY_REVIEW=docs/CAPABILITY-REVIEW.md
CAPABILITY_REVIEW_STATUS=RECORDED
CAPABILITY_IMPLEMENTATION=PASS
IR_CAPABILITY_LINK=DEFERRED
LEX_GATE=PASS
LEX_GATE_CMD=python3 tools/check_lex.py
PARSE_GATE=PASS
PARSE_GATE_CMD=python3 tools/check_parse.py
LOWER_GATE=PASS
LOWER_GATE_CMD=python3 tools/check_lower.py
P3_IR_GATE=PASS
P3_IR_GATE_CMD=python3 tools/check_ir.py
CAPABILITY_GATE=PASS
CAPABILITY_GATE_CMD=python3 tools/check_capability.py
CAPABILITY_DOC=docs/CAPABILITY-CONTRACT.md
CAPABILITY_SCHEMA=fx3-capability@1
DENY_FIRST=PASS
IR_ABI_DOC=docs/IR-ABI-CONTRACT.md
ABI_SCHEMA=fx3-ir@1
DETERMINISM=PASS
LOCATION_PRESERVATION=PASS
IR_EXECUTOR=NONE
CAPABILITY_IO=NONE
LANGUAGE_WRAP=CLOSED
LANGUAGE_WRAP_REPORT=bench/results/language-wrap-20261004/
AI_RETEST=PASS
AI_RETEST_REPORT=bench/results/ai-retest-20261004/
APP_GAP_OBSERVE=PASS
APP_GAP_OBSERVE_REPORT=bench/results/app-gap-observe-20261004/
APP_GAP_NARROW_01=PASS
APP_GAP_NARROW_01_REPORT=bench/results/app-gap-narrow-01-20261004/
CORPUS_APP_GAP_NARROW=PASS
STDLIB_HELPER_PLUS1=PASS
STDLIB_HELPER_PLUS1_REPORT=bench/results/stdlib-helper-plus1-20261004/
STDLIB_RESULT_VAL_OR=PASS
JSON_PASSTHROUGH_PAIR=PASS
JSON_PASSTHROUGH_PAIR_REPORT=bench/results/json-passthrough-pair-20261004/
CORE_V0_SCOPE_COMPLETE=YES
CORE_V1_PASS_CONDITIONS=DOCUMENTED
CORE_V1_PREP_CONDITION_2=READY
CORE_V1_VOTE=CLOSED
CORE_V1_VOTE_FILE=CORE-V1-VOTE.md
CORE_V1_VOTE_TALLY=3_OF_3
CORE_V1_VOTE_SEATS=1:gpt 2:grok-web 3:grok-build
DEFERRED_CYCLE3_PLUS=YES
STDLIB_NESTED_GET=PASS
STDLIB_GET_IN_OR=PASS
OUTPUT_TOKENS=MEASURED
OUTPUT_TOKENS_REPORT=bench/results/output-tokens-20261001/
FX_EXECUTION=NATIVE_OPENED
CORPUS_STDLIB=PASS
CORPUS_APP=GAP_ONLY
CORPUS_APP_PURE=PASS
CORPUS_TOKEN_MASS=PASS
ROADMAP6_EXEC=PASS
ROADMAP7_DENSITY=PASS
ROADMAP8=STOP_NO_CUT
SEMI_DISPLAY=PASS
WHITESPACE_SAME_FL=PASS
READ_FIXTURE_01_04=PASS
LANG_GATE=PASS
LANG_CYCLE2=CLOSED
LANG_CYCLE3=CLOSED
CORE_V1_PREP=READY
CORE_V1_FINAL=PASS
DEFERRED_SURFACES=DOCUMENTED_NOT_GATE
CORPUS_SELFHOST=NOT_STARTED
CORE_V0_PREP=READY
CORE_V0_VOTE=CLOSED
CORE_V0_VOTE_TALLY=3_OF_3
CORE_V0_FINAL=PASS
MAIN_GOAL=FX3
```

사용자는 셋이다. **v1 표결 자리(확정):** 1=지피티 · 2=그록웹 · 3=그록빌드(이 세션). 중계자는 사용자가 아니다. 최소 구현 단계는 닫혔다. 전체 플랜은 [PLAN.md](PLAN.md) 제안이다.

앞방향 성공 판정은 [AI-USE-SUCCESS.md](AI-USE-SUCCESS.md)에 고정했다. 리서치·사용자 리뷰는 참고다. 파이썬 대비 속도·계보 자랑은 지금 성공 조건이 아니다. U1·U2·U3가 이긴다.

## 세션 · 2026-10-01 — delimiter 닫고 semantic_min

주 목표를 FX3로 전환했다.

U1 ops case-03 실패의 실제 원인은 trailing `;`가 아니라 **ident가 `-`를 `$` 앞까지 먹어 `$first-$second`가 깨진 것**이었다. `tools/lower.py` ident 규칙을 고쳤다: `-`는 뒤에 이름 문자가 있을 때만 이름에 포함한다.

검증:

```bash
python3 tools/lower.py --check          # fixture 01–04 PASS
python3 tools/check_delimiter.py        # ops 6/6 + `$a-$b` PASS
python3 tools/check_semantic_min.py     # SEMANTIC_MIN=PASS
```

의미 검증:

```bash
python3 tools/check_semantic_min.py          # SEMANTIC_MIN=PASS
bash tools/check_semantic_native.sh          # FX_NATIVE=PASS (freelang-v11-fx --no-net)
```

`freelang-v11-fx/fl-build.sh`가 `CGC_BIN`을 환경·로컬 후보에서 찾도록 고쳤다. 전용 FX3 런타임은 없다.

## 코퍼스 조각 · 2026-10-01

`corpus/stdlib`에 `identity` / `req-body` / `str-coerce` 표현.
`python3 tools/check_corpus.py` → `CORPUS_STDLIB=PASS`. app·self-host는 아직.
상세: [corpus/CORPUS-2026-10-01.md](corpus/CORPUS-2026-10-01.md)

## Core v0 · 2026-10-01 CLOSED

표결: [CORE-V0-VOTE.md](CORE-V0-VOTE.md) · **3/3 AGREE_CLOSE** · `CORE_V0_FINAL=PASS`
준비: [CORE-V0-PREP.md](CORE-V0-PREP.md) · app GAP: [corpus/APP-GAP.md](corpus/APP-GAP.md)

잠금: fixture 01–04 · delimiter · semantic_min/native(좁은 폭) · stdlib 조각 · U1/U2/U3
밖: app GAP · self-host · fn/loop 확장 · fixture 05 · Hot Alias · v1 아님

v0 당시 기록: 사용자1=그록빌더(에이전트) · 사용자2=그록 · 사용자3=지피티
v1 확정 자리: 1=지피티 · 2=그록웹 · 3=그록빌드

## app 순수 헬퍼 · 2026-10-01

- `$n-1` ident 수정 (하이픈 뒤 숫자는 뺄셈)
- `corpus/app/fib` ← `fx-queue/server.fl` (if·산술·재귀만)
- `python3 tools/check_corpus.py` → `CORPUS_APP_PURE=PASS`
- GAP(`server_json`/`mariadb`/`fn`/`loop`)는 여전히 밖

## 코퍼스 질량 · 로드맵 5 · 2026-10-01

- `python3 tools/corpus_token_mass.py` → `CORPUS_TOKEN_MASS=PASS`
- 쌍 8건: FX3/FX 바이트비 **0.6504**, 프록시 단위비 **0.8758**
- `OUTPUT_TOKENS=NOT_MEASURED` (토크나이저 미설치·usage 없음)
- FX 트리 수정 없음 · 결과: `bench/results/corpus-mass-20261001/`

## 로드맵 6 · 실행 일치 · 2026-10-01

- 폭: `corpus/stdlib` + fixture 01–04 만. app/self-host 표현 없음. 표면 변경 없음
- `python3 tools/check_roadmap6_exec.py` → `ROADMAP6_EXEC=PASS`
- 내린 `.fl` ≡ 원본 `.fl` (정규화) 후 동일 인자로 실행 결과 일치 (fixture는 동일 스텁)

## 로드맵 7 · 밀도 경쟁 · 2026-10-01

- 폭: stdlib + fixture 01–04 (로드맵6 통과분만)
- `python3 tools/check_roadmap7_density.py` → `ROADMAP7_DENSITY=PASS`
- FX3 바이트 승 **7/7**. Core 표면 변경 없음
- 진 표기 Core 미채택: Hot Alias · 극단 압축 · fixture 05 · app/self-host
- 결과: `bench/results/density-20261001/`

## 로드맵 8 · 2026-10-01 · STOP_NO_CUT

- 밀도 승자 = 잠긴 Core → 표면을 더 깎지 않음
- Hot Alias·극단 압축·fixture 05 미채택 유지
- `bench/results/roadmap8-20261001/` · `ROADMAP_CYCLE=1_TO_8_CLOSED`
- Core v1 선언 아님. 다음은 새 안건만

## 세미콜론 표시 · 2026-10-01

- 안건: 저장 한 줄 · 볼 때만 `;` 줄바꿈 · 줄바꿈 비문법 · 같은 `.fx3`→같은 `.fl`
- 폭: fixture 01–04 + stdlib. Core 삭감·fixture05·Hot Alias·app·v1 없음
- `python3 tools/check_semi_display.py` → `SEMI_DISPLAY=PASS`
- 표시기: `tools/show.py`

## 언어 주기2 · 2026-10-01 · CLOSED

플랜: FX3_LANG_CYCLE_2 (Core 미삭 · fixture05/Hot Alias/v1 없음)

| 단계 | 결과 |
|------|------|
| L1 공백·줄바꿈 불변 | `WHITESPACE_SAME_FL=PASS` |
| L2 fixture 읽기 | **PASS 3/3 READ_OK** (`READ-VOTE.md` CLOSED). 새 기능 승인 아님 |
| L3 stdlib 헬퍼 | `req-param` · `req-query` |
| L4 언어 게이트 | `bash tools/check_language_gate.sh` → `LANG_GATE=PASS` |
| L5 | `LANG_CYCLE2=CLOSED` · `CORE_V1=NOT_YET` |

## 언어 주기3 · 2026-10-01 · CLOSED

| 단계 | 결과 |
|------|------|
| M1 Core v1 PREP | [CORE-V1-PREP.md](CORE-V1-PREP.md) · `CORE_V1_FINAL=PASS` · 표결 CLOSED |
| M2 보류 표면 | `bench/results/deferred-surfaces-20261001/` · 관문 아님 |
| M3 stdlib | `get-or` (+1; first-or는 eval 한계로 SKIP) |
| M4 LANG_GATE | 재실행 PASS |
| M5 | `LANG_CYCLE3=CLOSED` |

## 전부 안건 · A1–A2 · 2026-10-01

| 안건 | 결과 |
|------|------|
| A1 Core v1 체크리스트 | [CORE-V1-PREP.md](CORE-V1-PREP.md) · PASS 조건 문서화 · 표결로 `CORE_V1_FINAL=PASS` |
| A2 deferred 관찰 보강 | `bench/results/deferred-surfaces-20261001/REPORT.md` · `?` 이름 · `get-in-2` 하이픈숫자 · first-or/last-item · `DEFERRED_AS_CORE_GATE=NO` |
| A3 stdlib 헬퍼 | `nested-get` · `get-in-or` · `CORPUS_STDLIB=PASS` · `SEMI_DISPLAY=PASS` · `LANG_GATE=PASS` · `CORPUS_APP=GAP_ONLY` |
| A4 OUTPUT_TOKENS | `MEASURED` · ai-events usage · FX3 mean **429.2** (9 trials) · `bench/results/output-tokens-20261001/` · 토크나이저 미설치 |

FX3 전부 후보 A1–A4 닫힘.

## 언어 마무리 · Core v0 · 2026-10-04

- 안건: 잠긴 Core v0 범위의 언어 설계·검증 마무리 (v1 선언 아님)
- 재검증: `LANG_GATE=PASS` · `FX_NATIVE=PASS`
- 문서: [CORE-V1-PREP.md](CORE-V1-PREP.md) 조건1·3 READY · 표결 미개설
- 증거: [bench/results/language-wrap-20261004/](bench/results/language-wrap-20261004/)
- stale handoff(`fl-git GitLab`) 정리 · `LANGUAGE_WRAP=CLOSED`
- OUTSIDE 유지: fixture 05 · Hot Alias · Core 삭감 · 전용 런타임 · app GAP 전면 · self-host (`CORE_V1_FINAL=PASS`여도 밖)

## AI 사용자 재시험 · CORE_V1_PREP #2 · 2026-10-04

- 경로: U1 `u1-smoke-20260929` · U2 `u2-smoke-20260929` · U3 `u3-smoke-20260929` (+ U1 ops)
- ENTRY: 재시험 구간 before=after (sha256 고정) · U3 당시 3204B 대비 현재 3373B는 누적 문서 증가(이번 안건 미팽창)
- 산출물 재검증: first/repaired/regen 15/15 lower≡expected PASS
- 증거: [bench/results/ai-retest-20261004/](bench/results/ai-retest-20261004/) · `AI_RETEST=PASS` · 조건2 READY
- 이후 표결 CLOSED → `CORE_V1_FINAL=PASS` (현재 표면 잠금 · 언어 전체 완성 아님)

## Core v1 표결 · CLOSED · 2026-10-04

- 안건: [CORE-V1-VOTE.md](CORE-V1-VOTE.md)
- 자리: **1=지피티 · 2=그록웹 · 3=그록빌드**
- 집계: **3/3 AGREE_CLOSE** · REJECT=0 · `CLOSE_IF` 충족 → `CORE_V1_FINAL=PASS`
- 범위: 현재 표면만 잠금 · 언어 완성 아님 · OUTSIDE 유지

## App GAP 관측 보강 · 2026-10-04

- 안건: 표현 없이 관측만 (`EXPRESS=NO`) · Core 삭감·전용 런타임·fixture05·Hot Alias 없음
- FX pin `1d217f5` · `.fl` 9개 · GAP 심볼 43 · [corpus/APP-GAP.md](corpus/APP-GAP.md) 갱신
- 보강: `server_html`/`redirect`/`ws_*`/`form_parse`/`math_*`/`sqlite_*`/`catch` 등
- 증거: [bench/results/app-gap-observe-20261004/](bench/results/app-gap-observe-20261004/)
- `CORPUS_APP=GAP_ONLY` · `OUTSIDE_CORE_V1=YES` 유지

## APP_GAP_NARROW_01 · json 최소 표현 · 2026-10-04

- 선택: **json** (`server_*`/`sqlite` 비선택)
- 예제: `corpus/app-gap/json-ok-obj` · `json_stringify({ok:true})` lower≡ref PASS
- `server_json` 등 HTTP/DB는 계속 GAP · 전면 앱 이식 없음
- 증거: [bench/results/app-gap-narrow-01-20261004/](bench/results/app-gap-narrow-01-20261004/) · `CORPUS_APP_GAP_NARROW=PASS`

## stdlib helper +1 · result-val-or · 2026-10-04

- Core v1 표면만: `get` / `null?` / `if` · `fn`/`loop`·app GAP·fixture05·Hot Alias·런타임 미개방
- 코퍼스: `corpus/stdlib/result-val-or.{fx3,fl}` · lower·semantic_min·native PASS
- 증거: [bench/results/stdlib-helper-plus1-20261004/](bench/results/stdlib-helper-plus1-20261004/)

## JSON 이름 호출 쌍 · 2026-10-04

- `json-stringify` / `json-try-parse` 이름 그대로 호출만 · `server_*`/`mariadb`/`fn`/`loop` 없음
- lower≡ref PASS · host EXEC SKIP
- 증거: [bench/results/json-passthrough-pair-20261004/](bench/results/json-passthrough-pair-20261004/)

## Track 1 · P1 lexer 골격 · 2026-10-05

Track 1 지시(parser → IR → capability → FX runtime → self-hosting)를 열었다.

- P0 Core 고정: fixture 01–04 · delimiter · 기존 잠금 유지 (문법 변경 없음)
- P1 첫 조각: **lexer + line/column + 오류 코드**만
- 파일: `tools/fx3_lex.py` · `tools/check_lex.py` · `fixtures/lex/{valid,invalid}/`
- `python3 tools/check_lex.py` → `LEX_GATE=PASS`
- `python3 tools/lower.py --check` → 회귀 PASS (lower.py 미변경)
- 아직 없음: parser AST · 전용 IR · capability runtime · `fx3` CLI · self-hosting
- 다음: P1 parser AST (binding/괄호/delimiter 거부 + 위치 진단)

## Track 1 · P1 parser AST · 2026-10-05

- 입력: `fx3_lex` token stream · 출력: 위치 보존 AST
- 범위: F / params / leading binding / call / op / map / `?`·`~` / `@` get / 괄호·delimiter
- 파일: `tools/fx3_parse.py` · `tools/check_parse.py` · `fixtures/parse/{valid,invalid}/`
- invalid 5: binding-after-expr · unclosed-paren · expected-F · toplevel-missing-semi · empty-body
- `python3 tools/check_parse.py` → `PARSE_GATE=PASS`
- `python3 tools/check_lex.py` · `python3 tools/lower.py --check` 회귀 PASS · `lower.py` 미변경
- 다음: P2 lowering compiler (AST → 결정적 `.fl`, fixture 회귀)

## Track 1 · P2 AST lowering · 2026-10-05

- 입력: located AST · 출력: 결정적 `.fl` UTF-8 바이트
- 파일: `tools/fx3_lower.py` · `tools/check_lower.py` · `fixtures/lower/{valid,invalid}/`
- golden 01–04 byte-match · binding/nested-call/conditional/map-order · repeated lower 동일
- unsupported/invalid AST → `E_UNSUPPORTED_NODE` + line/column
- `python3 tools/check_lower.py` → `LOWER_GATE=PASS` · `DETERMINISM=PASS`
- `check_parse` / `check_lex` / `lower.py --check` / `check_corpus` 회귀 PASS · `tools/lower.py` 미변경
- 다음: P3 공통 IR/ABI (계약만)

## Track 1 · P3 IR/ABI 계약 · 2026-10-05

- **계약 잠금만**. 실행기·capability·native·CLI·self-hosting 없음
- 문서: [docs/IR-ABI-CONTRACT.md](docs/IR-ABI-CONTRACT.md) · `abi=fx3-ir` · `version=1`
- 파일: `tools/fx3_ir.py` · `tools/check_ir.py` · `fixtures/ir/{valid,invalid}/`
- 노드: program/function/binding/variable/literal/call/operator/conditional/null_check/get/map/map_entry/result
- 모든 노드 `loc` · 결정적 JSON 직렬화 · unsupported/`loop` 등 → `E_UNSUPPORTED_NODE`
- `python3 tools/check_ir.py` → `P3_IR_GATE=PASS`
- lexer/parser/lower/legacy-lower/corpus 회귀 PASS · Core·`lower.py` 미변경 · parser 미변경
- 다음: P4 capability 판정 계약 (deny-first)

## Track 1 · P4 capability deny-first · 2026-10-05

- **판정만**. 실제 I/O·IR 실행·runtime·CLI 없음
- 문서: [docs/CAPABILITY-CONTRACT.md](docs/CAPABILITY-CONTRACT.md) · `fx3-capability@1`
- 파일: `tools/fx3_capability.py` · `tools/check_capability.py` · `fixtures/capability/{allow,deny}/`
- 허용 가능: `source.read` · `ir.inspect` (root 안 상대경로 + 인자 계약)
- 항상 deny: `source.write` · `process.exec` · `network.request` · `runtime.execute` · `filesystem.delete`
- `python3 tools/check_capability.py` → `CAPABILITY_GATE=PASS` · `DENY_FIRST=PASS`
- `fx3_ir.py` / lexer / parser / lower* 미변경
- 다음: **P4 계약 검토 안건** (P5 runtime/executor로 자동 진행하지 않음)

## Track 1 · P4 capability 계약 리뷰 · 2026-10-05

- 산출: [docs/CAPABILITY-REVIEW.md](docs/CAPABILITY-REVIEW.md)
- LOCKED: deny-first · 파일 경계 · 서버 고정 canonical root · `filesystem.rename` 항상 deny
- DEFERRED: IR `capability_request` · 실 디스크 I/O · runtime/executor · reason v2

## Track 1 · P4 capability 구현 정렬 · 2026-10-05

- `tools/fx3_capability.py` · `tools/check_capability.py` · `fixtures/capability/**`
- 서버 `canonical_root` · 요청 `root` → `invalid_argument` · 확장자 · in-memory `MAX_BYTES`/UTF-8 · `filesystem.rename` ALWAYS_DENY(args 미접근)
- `python3 tools/check_capability.py` → IMPLEMENTATION/ROOT/FILE_BOUNDARY/RENAME/FIXTURE/DETERMINISM PASS
- 디스크 write/rename/delete·runtime·IR 변경 없음 · schema `fx3-capability@1`
- 다음: wildcard/recursive 문서 또는 reason v2 검토 (실행기 아님)

## Track 1 · P4 wildcard/recursive deny · 2026-10-06

- path에 `*` / `**` / `?` → `invalid_argument` (글롭 미실행)
- `recursive` args·최상위 → `invalid_argument`
- fixture `21`–`24` · `check_capability` 반영
- schema `fx3-capability@1` 유지 · runtime/I/O 없음
- 다음: 출력 상한 또는 조합 상승 명시 (P5 아님)

## Track 1 · P5 CLI 게이트 · 2026-10-06

- 성공 기준 A: `fx3 check/lower/ir/cap/test/package verify` (전용 runtime 없음)
- 파일: `tools/fx3_cli.py` · `bin/fx3` · `tools/check_cli.py` · `docs/FX3-CLI.md`
- S0 wildcard 커밋 · S1 MAX_OUTPUT_BYTES/조합상승 문서 · S2–S7 CLI
- `python3 tools/check_cli.py` → CLI_GATE=PASS
- RUNTIME=NONE · IR executor 없음 · capability 대상 파일 I/O 없음
- 다음 길은 새 안건만 (읽기 I/O 스모크 또는 IR exec — 자동 진행 없음)

## Track 1 · delegated fx3 run · 2026-10-06

- 계약: [docs/FX3-RUN.md](docs/FX3-RUN.md) · `RUN=DELEGATED` · `RUNTIME_OWNED=NONE`
- CLI: `fx3 run FILE --call '(fn args…)' [--engine=eval|native]`
- 기본 eval → `tools/eval_fl_min.py` · native → `fl-build.sh --no-net` (없으면 BLOCKED exit 2)
- Lower 정본: `fx3_lower` · `tools/lower.py` 미사용
- 스모크 fixture: `fixtures/run/sum.fx3`
- `python3 tools/check_cli.py` → CLI_GATE=PASS (run 포함)
- 비범위: owned VM · IR exec · capability 실 I/O · self-host · push
- 다음: NEW_ROAD_ONLY (자동 진행 없음)

## POC · manifest validator · 2026-10-06

- Source: `src/manifest-validator.fx3` · docs: `poc/manifest-validator/`
- Delegated eval+native PASS (behavioral 6 + determinism + usage)
- `eval_fl_ext` stdlib shims · native `==`→`=` call adapter
- `RUNTIME_OWNED=NONE` · `IO_CHANGE=NO` · `IR_EXEC=NO` · COMMIT=NO · PUSH=NO

## Review · manifest-validator fixtures · 2026-10-06

- fixtures 01–10 under `poc/manifest-validator/fixtures/` (call/expect/meta)
- `bash poc/manifest-validator/scripts/verify.sh` → POC_MANIFEST_VALIDATOR=PASS cases=10
- eval≡native · determinism · usage exit 2 · static no I/O
- regression CLI/lex/parse/lower/ir/capability PASS · COMMIT=NO · PUSH=NO

## POC #2 · config-lint · 2026-10-06

- Source: `src/config-lint.fx3` (`lint-config`) · `poc/config-lint/`
- Fixtures 01–11 · boolean/port/env rules · eval≡native
- `bash poc/config-lint/scripts/verify.sh` → POC_CONFIG_LINT=PASS cases=11
- Manifest-validator regression still PASS · COMMIT=NO · PUSH=NO

## Harden · delegated POC rail · 2026-10-06

- `tools/check_poc.py` shared gate · `poc/*/poc.json` · thin verify.sh wrappers
- `docs/FX3-DELEGATED-LIMITS.md` · `poc/README.md`
- `python3 tools/check_poc.py all` → both POCs PASS
