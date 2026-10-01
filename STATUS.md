# FreeLang FX3 현재 상태

기준일: 2026-09-29

```text
PROJECT=PREPARED
IMPLEMENT=NO
SOURCE_COPY=NO
FX3_SURFACE=.fx3
CANONICAL_LOWERING=.fl
RUNTIME=NONE
PARSER=NONE
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
FX3_AS_LANGUAGE=TOO_EARLY
GROK_USER=FIVE_RULES
NO_NEW_RUNTIME=YES
NO_PRETTIER=YES
NO_SHORTER=YES
FX3_CORE_01=KEEP
NEXT_USER_TEST=READ_FIXTURE_04
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
HANDOFF=SEMI_DISPLAY PASS (fixture01-04+stdlib). Core 미삭. 다음=새 안건만
NEXT_AGENDA_ONLY=NEW_AGENDA_ONLY
FX_EXECUTION=NATIVE_OPENED
CORPUS_STDLIB=PASS
CORPUS_APP=GAP_ONLY
CORPUS_APP_PURE=PASS
CORPUS_TOKEN_MASS=PASS
ROADMAP6_EXEC=PASS
ROADMAP7_DENSITY=PASS
ROADMAP8=STOP_NO_CUT
SEMI_DISPLAY=PASS
CORPUS_SELFHOST=NOT_STARTED
CORE_V0_PREP=READY
CORE_V0_VOTE=CLOSED
CORE_V0_VOTE_TALLY=3_OF_3
CORE_V0_FINAL=PASS
MAIN_GOAL=FX3
```

사용자는 셋이다. 사용자 1은 그록빌더, 2는 그록, 3은 지피티다. 중계자는 사용자가 아니다. 최소 구현 단계는 닫혔다. 전체 플랜은 [PLAN.md](PLAN.md) 제안이다.

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

사용자1=그록빌더(이 에이전트) · 사용자2=그록 · 사용자3=지피티

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
