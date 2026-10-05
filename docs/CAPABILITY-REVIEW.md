# FX3 P4 Capability Contract Review

```text
REVIEW=2026-10-05
SCHEMA_UNDER_REVIEW=fx3-capability@1
CONTRACT=docs/CAPABILITY-CONTRACT.md
CODE=tools/fx3_capability.py
GATE=python3 tools/check_capability.py
IO=NONE
IR_LINK=DEFERRED
RUNTIME=NONE
NEXT=NOT_P5
```

이 문서는 **P4 계약 리뷰**다. 구현 변경·실 I/O·IR `capability_request` 삽입·runtime/executor는 하지 않는다.

현재 판정:

```text
P4 계약 잠금: PASS
deny-first 설계: PASS
파일 경계 (확장자·UTF-8 strict·MAX_BYTES): LOCKED (문서)
root confinement (서버 고정 canonical root): LOCKED (문서, 요청 root 금지)
실제 I/O: 없음
IR 실행: 없음
runtime/executor: 없음
코드 정렬 (2026-10-05): PASS — 고정 canonical_root · 요청 root deny · 확장자 · MAX_BYTES/UTF-8(content) · rename ALWAYS_DENY
실 디스크 I/O / runtime / executor: 없음
filesystem.rename 항상 deny: LOCKED (문서+코드)
wildcard/recursive deny: LOCKED (문서+코드)
다음: 출력 크기 상한 · 조합 상승 명시 · reason v2 후보 (P5 아님)
```
범례:

| 표기 | 의미 |
|------|------|
| LOCKED | v1 계약·게이트에 이미 있음 |
| PROPOSED | 리뷰에서 채택 후보. 코드 미반영 |
| OPEN | 값·경계를 아직 고르지 않음 |
| DEFERRED | 의도적으로 나중 (IR 연결·실 I/O) |
| OUT | 이번 Track 범위 밖 |

---

## 1. `source.read` / `ir.inspect` 인자·root 규칙

### 1.1 canonical root

| 항목 | 상태 | 기록 |
|------|------|------|
| **canonical root = 서버 설정 고정 workspace root** | **LOCKED** | 요청자가 지정·변경 불가 |
| 요청 path | LOCKED | 고정 root 기준 **상대경로만** |
| 요청에 `root` 필드 | **LOCKED deny** | 있으면 `invalid_argument` |
| `서버 root + 상대 path → canonical 검증` | LOCKED | 계약 정본 문구 |
| 실디렉터리 resolve / realpath | OUT/DEFERRED | 실 I/O 전 금지 |
| 코드가 요청 `root`를 거부 | **PASS** | `decide(..., canonical_root=서버고정)` · 요청 `root` → `invalid_argument` |

정본 문구 ([CAPABILITY-CONTRACT.md](CAPABILITY-CONTRACT.md) §5):

```text
canonical root:
서버가 설정한 고정 root만 사용한다.
요청자는 root를 지정하거나 변경할 수 없다.
요청 path는 고정 root 기준 상대경로로만 해석한다.
```

**폐기:** `canonical root = 요청 root` 해석. 위험하므로 계약에서 제거했다.

### 1.2 상대경로만 허용

| 항목 | 상태 |
|------|------|
| path 상대만 | LOCKED |
| `/…`, `X:…` 절대 거부 | LOCKED → `path_escape` |
| 빈 path 거부 | LOCKED → `invalid_argument` |

### 1.3 `..`, 절대경로, symlink

| 항목 | 상태 | 기록 |
|------|------|------|
| `..` 세그먼트 거부 | LOCKED | `path_escape` |
| 절대경로 거부 | LOCKED | `path_escape` |
| 백슬래시 거부 | LOCKED | `path_escape` |
| NUL 거부 | LOCKED | `path_escape` |
| root 밖 normpath 거부 | LOCKED | `path_escape` |
| symlink 실해석 차단 | DEFERRED | 실 FS 없음. 문자열만 검사 |
| `symlink_blocked` reason | PROPOSED | 실 I/O 단계에서 `os.path.realpath` 비교 후 사용. **지금은 코드에 넣지 않음** |

**리뷰 권고:** symlink는 “실 I/O 게이트”의 필수 deny. 순수 판정 v1에 가짜 allow를 만들지 말 것.

### 1.4 파일 크기·인코딩·확장자 제한

| 항목 | 상태 | 기록 |
|------|------|------|
| 확장자 allowlist | **LOCKED** | 전체 `.fx3`·`.ir.json`만 |
| capability별 확장자 | **LOCKED** | `source.read`→`.fx3` / `ir.inspect`→`.ir.json` (혼용 deny) |
| `MAX_BYTES` | **LOCKED** | **262144** (정본 한 곳: CONTRACT §6). 요청으로 상향 불가 |
| 인코딩 | **LOCKED** | UTF-8 **strict**, replacement 금지 → 실패 시 `encoding_invalid` |
| args | LOCKED | `{path}`만. `max_bytes`/`encoding` 키 자체도 deny (`invalid_argument`) |
| 코드 구현 | DEFERRED | 계약만 LOCKED. 게이트·runtime 미반영 |

```text
source.read  extensions = .fx3
ir.inspect   extensions = .ir.json
MAX_BYTES    = 262144
encoding     = UTF-8 strict
```
### 1.5 알 수 없는 인자 거부

| 항목 | 상태 |
|------|------|
| args 키 집합이 계약과 다르면 deny | LOCKED → `invalid_argument` |
| 타입 불일치 deny | LOCKED |

---

## 2. reason 코드 세분화

### 2.1 현재 v1 (LOCKED)

```text
explicit_allow
deny_by_default
unknown_capability
invalid_argument
path_escape
invalid_location
empty_capability
```

### 2.2 파일 경계 reason (v1 스키마 유지, 코드 미구현)

계약에 LOCKED. **스키마 이름은 여전히 `fx3-capability@1`.** reason v2 bump 아님.

```text
extension_blocked   # LOCKED 계약 어휘 — 코드 미구현
size_exceeded       # LOCKED 계약 어휘 — MAX_BYTES=262144
encoding_invalid    # LOCKED 계약 어휘 — UTF-8 strict
```

### 2.3 reason v2 **후보** (파일 경계와 구분)

```text
symlink_blocked     # PROPOSED — 실 I/O realpath
sensitive_path      # PROPOSED — 민감 이름 목록 OPEN
```

| reason | 구분 | 비고 |
|--------|------|------|
| `deny_by_default` 등 §2.1 | v1 구현됨 | 코드 게이트 |
| `extension_blocked` / `size_exceeded` / `encoding_invalid` | v1 계약 어휘 | 문서 LOCKED, 코드 없음 |
| `symlink_blocked` / `sensitive_path` | v2 후보 | 파일 경계 안건 밖 |

**리뷰 결론:** 파일 경계 reason은 문서에만 잠근다. `@2` 승격·코드·fixture 변경은 하지 않는다.

---

## 3. IR 연결 — 보류

| 항목 | 상태 |
|------|------|
| capability 판정 ↔ IR 분리 | LOCKED (안전) |
| IR에 `capability_request` 노드 삽입 | DEFERRED |
| `fx3_ir.py` 변경 | OUT (지금 금지 유지) |
| 실행기 전 필요성 문서 검토 | 본 절 |

**필요성 (문서만):**

- FX backend가 deny-first로 부작용을 막으려면, 실행 직전 **요청 객체**가 필요하다.
- 그 요청을 IR에 심을지, 실행 프레임 메타로 둘지, CLI가 별도 grant 파일을 줄지는 **실행기 설계 때** 고른다.
- 지금 IR에 넣으면 스키마·golden IR·미구현 executor가 한꺼번에 흔들린다.

**리뷰 결론:** `capability_request` IR 삽입 **하지 않음**. 필요성만 위 문단으로 기록.

---

## 4. 실 I/O 전 추가 deny 규칙

| 규칙 | 상태 | 비고 |
|------|------|------|
| write / delete 금지 | LOCKED | `source.write`·`filesystem.delete` |
| **`filesystem.rename` 항상 deny** | **LOCKED** | reason=`deny_by_default` (v1). source/dest 미검사·미실행. 코드·fixture **GAP** |
| `process.exec` 금지 | LOCKED | |
| `network.request` 금지 | LOCKED | |
| `runtime.execute` 금지 | LOCKED | |
| **wildcard·재귀 범위 금지** | **LOCKED** | path `*`/`**`/`?` → `invalid_argument`. `recursive` 인자·최상위 → `invalid_argument`. 글롭 실행 없음 |
| **출력 크기 제한** | **LOCKED (문서)** | `MAX_OUTPUT_BYTES=262144` · 입력 `MAX_BYTES`와 별명. 코드 emit는 I/O 길 |
| **capability 조합 상승 금지** | **LOCKED (문서)** | 독립 cap · 단조 감소 · 묶음 grant 키 deny. CONTRACT §6.1 |

### 4.1 `filesystem.rename` (문서 잠금 상세)

| 항목 | 상태 |
|------|------|
| capability 이름 `filesystem.rename` | LOCKED 항상 deny |
| reason | `deny_by_default` (기존 v1 어휘. `@2`/신규 reason 없음) |
| source / destination 인자 | 실행·경로 해석하지 않음 (이름만으로 deny) |
| 요청 `root` | 계속 deny (`invalid_argument`) — root 계약 UNCHANGED |
| 고정 canonical root · 상대 path | UNCHANGED |
| 스키마 | `fx3-capability@1` UNCHANGED |
| 코드 `ALWAYS_DENY` 반영 | **PASS** | `filesystem.rename` 포함 · args 미접근 |
| 실제 rename I/O | OUT / 금지 |

**리뷰 권고 (실 I/O 게이트 진입 조건):**

```text
1. rename 항상 deny LOCKED
2. wildcard/recursive deny LOCKED (본 작업)
3. symlink_blocked 실검 경로가 정의된 뒤
4. 출력 상한·조합 상승 문구가 잠긴 뒤
5. 그 다음에야 읽기 스모크 (여전히 write/exec/network/rename/glob 없음)
```

P5 runtime/executor와 혼동하지 말 것. 위는 **capability I/O 허용 폭을 좁히는 사전 조건**이다.

---

## 5. 종합

### 이미 PASS·LOCKED인 것

- deny-first 기본
- 허용 cap 2종 + 경로 문자열 탈출 차단
- 알 수 없는 인자 거부
- 하드 deny 목록 (write/exec/network/runtime.execute/delete)
- 결정적 JSON · location null 허용
- IR/`fx3_ir.py` 비연결
- **파일 경계 문서 LOCKED:** `.fx3`/`.ir.json` · capability별 확장자 · `MAX_BYTES=262144` · UTF-8 strict
- **root confinement LOCKED:** 서버 고정 canonical root · 요청 `root` 금지 · 상대 path만
- **`filesystem.rename` LOCKED_ALWAYS_DENY** (문서+코드)
- **wildcard/recursive LOCKED** (path `*`/`?` · `recursive` 인자)

### OPEN → 다음 안건 후보

1. **P5 CLI 게이트** (쓸 만한 1차 길 — 진행 중)
2. reason v2 후보만 (`symlink_blocked` / `sensitive_path`)
3. (나중) 실 I/O 읽기 스모크 — executor 없이 capability 계층만

### 명시적 비목표

```text
P5 전용 runtime/executor (CLI 게이트와 다름)
IR capability_request 삽입
실 파일 읽기/쓰기 (요청 JSON 제외)
process/network
self-hosting
```

CLI 게이트(`fx3 check|lower|ir|cap|test`)는 쓸 만한 1차 길에 **포함**된다 → [FX3-CLI.md](FX3-CLI.md).

---

## 6. 적대적 검수 · 2026-10-05

```text
CAPABILITY_ADVERSARIAL_REVIEW=PASS
ADV_EXIT=0
CAP_EXIT=0
IO=NO (디스크 write/rename/delete 미실행)
```

| 영역 | 판정 | 근거 |
|------|------|------|
| 요청 `root` 주입 | PASS | `root` 키 존재 → `invalid_argument` (값 무시) |
| 절대/`../`/`.`/빈/`\`/드라이브/NUL | PASS | `path_escape` 또는 `invalid_argument` |
| kwargs `canonical_root` | PASS | keyword-only · 요청 필드로 덮어쓰기 불가 |
| 위치 인자로 root 전달 | PASS | `TypeError` (허용 경로 아님) |
| 확장자·대소문자·이중 확장자 | PASS | `.FX3` deny · `.fx3.bak` deny · `.bak.fx3` allow(접미사 계약) |
| UTF-8 / 262144 / 262145 | PASS | exact allow · +1 `size_exceeded` |
| rename + ALWAYS_DENY | PASS | args 미접근 · `path=null` |
| 결정성·무예외·키 계약 | PASS | 동일 바이트 · garbage 입력도 dict 판정 |
| symlink 실해석 | N/A(계약) | 문자열만 · 실 FS follow 없음 (DEFERRED) |

잔여 관찰 (FAIL 아님):

1. ~~요청 최상위 `canonical_root` 무시~~ → **거부 정렬 완료** (`invalid_argument`). `root`·未知 최상위도 동일.
2. `DEFAULT_CANONICAL_ROOT`는 테스트/도구 기본값이다. 배포 코드는 서버 설정을 **반드시** keyword-only kwargs로 넣어야 한다.
3. symlink·실디스크 검사는 여전히 DEFERRED.

### 6.1 canonical_root 입력 거부 정렬 · 2026-10-05

| 항목 | 상태 |
|------|------|
| 요청 `canonical_root` | deny `invalid_argument` |
| 요청 `root` | deny `invalid_argument` |
| 未知 최상위 키 | deny `invalid_argument` |
| 서버 keyword-only `canonical_root=` | allow 경로 유지 |
| 위치 인자 canonical root | TypeError (keyword-only) |

명령 기록은 게이트 재실행 결과를 따른다.
