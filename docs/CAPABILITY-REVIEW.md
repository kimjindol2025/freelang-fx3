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
실제 I/O: 없음
IR 실행: 없음
runtime/executor: 없음
다음 작업: 본 리뷰의 OPEN 항목을 별도 안건으로 확정
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
| 요청마다 `root` 문자열 필수 (허용 cap) | LOCKED | 없으면 `invalid_argument` |
| root는 상대경로 | LOCKED | 절대/`..`/`\` 등 → escape 경로 |
| 저장소 전역 단일 canonical root 상수 | OPEN | 예: 항상 `fixtures` vs 호출자 제공. **판정기는 요청 `root`만 본다** |
| root를 실디렉터리로 resolve | OUT | 실 I/O 전 금지 |

**리뷰 권고:** v1은 “요청 `root` = 허용 경계”로 유지. 전역 canonical root는 CLI/패키지 단계에서 따로 잠근다.

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
| 확장자 allowlist | PROPOSED | `source.read` → `.fx3`만? `ir.inspect` → `.ir.json`만? |
| 최대 바이트 (`max_bytes` 인자 또는 계약 상수) | PROPOSED | 실읽기 전 메타 검사. 순수 판정만이면 요청 필드 `max_bytes` 상한 검증 가능 |
| 인코딩 UTF-8만 | PROPOSED | 실읽기 시 `encoding_invalid`. 판정 단계에서는 요청에 `encoding` 키가 있으면 화이트리스트만 |
| 현재 args | LOCKED | `{path}`만. 추가 키는 지금 `invalid_argument` |

**OPEN 값 (다음 안건에서 숫자·목록 확정):**

```text
source.read  extensions = ?   (.fx3 권고)
ir.inspect   extensions = ?   (.ir.json 권고)
max_bytes    = ?              (예: 256KiB 권고, 미확정)
encoding     = utf-8 only     (권고)
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

### 2.2 리뷰 제안 집합

```text
deny_by_default
unknown_capability
invalid_argument
path_escape
symlink_blocked      # PROPOSED — 실 I/O 후
sensitive_path       # PROPOSED — 이름/접두 민감 경로
size_exceeded        # PROPOSED — 크기 상한
encoding_invalid     # PROPOSED — 실읽기/선언 인코딩
```

### 2.3 매핑 권고

| 제안 reason | v1 처리 | 비고 |
|-------------|---------|------|
| `deny_by_default` | LOCKED | 하드 deny 목록·누락 cap |
| `unknown_capability` | LOCKED | |
| `invalid_argument` | LOCKED | |
| `path_escape` | LOCKED | `..`/절대/`\`/root 밖 |
| `symlink_blocked` | PROPOSED | 실 I/O 전 미사용 |
| `sensitive_path` | PROPOSED | 예: `.git/`, `*.pem`, `id_rsa` 이름 규칙 — **목록 OPEN** |
| `size_exceeded` | PROPOSED | 상한 OPEN |
| `encoding_invalid` | PROPOSED | 실 I/O 또는 명시 encoding 인자 |

**유지 권고 (제안 목록에 없어도 v1 유지):**

- `explicit_allow` — allow 시 필요
- `invalid_location` — 요청 location 검증
- `empty_capability` — 빈 이름 (또는 `invalid_argument`로 흡수 — OPEN)

**리뷰 결론:** reason 세분화는 **스키마 bump (`fx3-capability@2`) 후보**. v1 fixture를 깨지 말고, 채택 시 별도 안건으로 게이트·fixture를 갱신한다. 이번 리뷰에서는 코드를 바꾸지 않는다.

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
| write / delete / rename 금지 | LOCKED(+PROPOSED) | `source.write`·`filesystem.delete` LOCKED. `rename` 이름 **PROPOSED** (`filesystem.rename` 항상 deny) |
| `process.exec` 금지 | LOCKED | |
| `network.request` 금지 | LOCKED | |
| `runtime.execute` 금지 | LOCKED | |
| wildcard·재귀 범위 금지 | PROPOSED | path에 `*`, `**`, `?` 또는 args.`recursive=true` → deny |
| 출력 크기 제한 | PROPOSED | 실 I/O/실행 출력 상한. 판정 필드 또는 runtime 상수 — OPEN |
| capability 조합 상승 금지 | PROPOSED | read 허용이 write/exec를 암시하지 않음 — 원칙 LOCKED. 명시적 “grant set 상승” API는 없음(유지) |

**리뷰 권고 (실 I/O 게이트 진입 조건):**

```text
1. rename/wildcard/recursive deny가 계약에 문자로 들어간 뒤
2. symlink_blocked 실검 경로가 정의된 뒤
3. max_bytes / encoding / extension allowlist 숫자가 잠긴 뒤
4. 그 다음에야 읽기 스모크 (여전히 write/exec/network 없음)
```

P5 runtime/executor와 혼동하지 말 것. 위는 **capability I/O 허용 폭을 좁히는 사전 조건**이다.

---

## 5. 종합

### 이미 PASS인 것

- deny-first 기본
- 허용 cap 2종 + 경로 문자열 탈출 차단
- 알 수 없는 인자 거부
- 하드 deny 목록 (write/exec/network/runtime.execute/delete)
- 결정적 JSON · location null 허용
- IR/`fx3_ir.py` 비연결

### OPEN → 다음 안건 후보 (P5 아님)

1. extension allowlist · `max_bytes` · encoding 화이트리스트 수치 확정  
2. reason v2 (`symlink_blocked`, `sensitive_path`, `size_exceeded`, `encoding_invalid`) 채택 여부 · 스키마 bump  
3. `filesystem.rename` · wildcard/recursive deny를 v1 문서에 추가할지  
4. sensitive path 이름 목록  
5. (나중) 실 I/O 읽기 스모크 설계 — executor 없이 capability 계층만

### 명시적 비목표

```text
P5 runtime/executor
IR capability_request 삽입
실 파일 읽기/쓰기
process/network
self-hosting
fx3 CLI
```
