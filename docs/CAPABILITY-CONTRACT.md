# FX3 Capability Contract (deny-first)

```text
SCHEMA=fx3-capability@1
STATUS=LOCKED_JUDGMENT_ONLY
FILE_BOUNDARY=LOCKED
EXECUTOR=NONE
RUNTIME=NONE
IO=NONE
DEFAULT=DENY
PURPOSE=CONTRACT_ONLY
MAX_BYTES=262144
```

기준일: 2026-10-05
파일 경계 잠금: 2026-10-05

이번 단계는 **capability 선언·검증·거부 판정**만 잠근다.
파일을 읽거나 쓰지 않는다. 프로세스를 실행하지 않는다. 네트워크에 연결하지 않는다.
IR 실행기·FX native·CLI·self-hosting은 범위 밖이다.

`tools/fx3_ir.py`는 수정하지 않는다. capability 요청은 IR 실행과 분리된 **순수 판정 입력**이다.

파일 확장자·인코딩·`max_bytes`·wildcard/recursive 규칙은 **계약·판정 코드로 LOCKED**다.
스키마는 `fx3-capability@1`을 유지한다 (reason v2 승격 없음). 디스크 I/O·runtime은 없다.

## 1. 정책

1. 기본값은 항상 **deny**
2. capability가 없거나 빈 문자열이면 deny
3. 알 수 없는 capability는 deny
4. 이름이 맞아도 인자가 계약과 다르면 deny
5. 경로는 **서버 고정 canonical root** 밖이면 deny (요청자가 root를 정하지 않음)
6. 절대경로·`..`·백슬래시·널 바이트 등 탈출 형태는 deny
7. read / write / exec / network는 **서로 독립** capability
8. 이 버전에서 `write`·`exec`·`network`·`runtime.execute`·`filesystem.delete`·`filesystem.rename`은 **항상 deny**
9. 허용은 테스트용 순수 판정뿐 (`source.read`, `ir.inspect` + 유효 인자)
10. 판정 결과는 결정적 JSON 바이트

심볼릭 링크 실해석은 하지 않는다. 경로 **문자열 형태**만으로 탈출을 거부한다.

## 2. 요청 schema

```json
{
  "capability": "source.read",
  "args": {"path": "relative/file.fx3"},
  "location": {"line": 1, "column": 1}
}
```

| 필드 | 규칙 |
|------|------|
| `capability` | 문자열. 필수. 빈 문자열 deny |
| `args` | 객체. 없으면 `{}`. **허용 키만**. 알 수 없는 키 deny (`invalid_argument`) |
| `location` | `{line,column}` 또는 생략/`null`. 잘못된 값이면 deny(`invalid_location`) |

**허용 최상위 키:** `capability` · `args` · `location` 뿐.

| 거부 최상위 키 | reason |
|----------------|--------|
| `root` | `invalid_argument` |
| `canonical_root` | `invalid_argument` (서버 kwargs만 허용; 요청 필드로 덮어쓰기 불가) |
| 그 외 未知 키 | `invalid_argument` |

위치 생략/`null`은 **오류가 아니다**. 결과 `location`은 `null`.

요청자가 `root`·`canonical_root`·`max_bytes`·`encoding`·`recursive` 등 **추가 필드·한도 변경 인자를 올리는 것은 금지**다.

## 3. 판정 결과 schema

```json
{
  "schema": "fx3-capability@1",
  "decision": "allow|deny",
  "capability": "source.read|ir.inspect",
  "reason": "explicit_allow|unknown_capability|invalid_argument|path_escape|extension_blocked|size_exceeded|encoding_invalid|deny_by_default",
  "path": "relative/path|null",
  "location": {"line": 1, "column": 1}
}
```

필드 집합 고정. 직렬화는 `sort_keys=True`, `separators=(",", ":")`, UTF-8, trailing newline 없음.
스키마 이름은 `fx3-capability@1` 유지 (v2 승격 없음).

| decision | 의미 |
|----------|------|
| `allow` | 허용 cap + 경로 + 파일 경계 계약 충족 |
| `deny` | 거부 |

### reason — 구현됨 (코드 게이트)

| reason | 언제 |
|--------|------|
| `explicit_allow` | 허용 목록 + 인자·경로 유효 (현재 게이트) |
| `deny_by_default` | 기본 거부 / 하드 거부 목록 |
| `unknown_capability` | 미등록 이름 |
| `invalid_argument` | 인자 타입·키·누락 |
| `path_escape` | 절대경로·`..`·`\`·고정 canonical root 밖 |
| `invalid_location` | location 형태 오류 |
| `empty_capability` | 빈 이름 |

### reason — 파일 경계 계약 어휘 (LOCKED, 코드 미구현)

| reason | 언제 (계약) |
|--------|-------------|
| `extension_blocked` | capability와 확장자 불일치 또는 비허용 확장자 |
| `size_exceeded` | 대상 크기가 `MAX_BYTES` 초과 |
| `encoding_invalid` | UTF-8 strict 디코딩 실패 |

위 세 값은 **계약 문서에 잠긴 deny reason**이다. runtime/코드/fixture에 아직 넣지 않는다.
`symlink_blocked` / `sensitive_path` 등은 reason v2 **후보**이며 본 파일 경계 잠금 범위가 아니다 → [CAPABILITY-REVIEW.md](CAPABILITY-REVIEW.md).

`path`는 요청에 경로가 있으면 정규화 전 요청 문자열을 넣고, 없으면 `null`.

## 4. Capability 목록과 허용 인자

### 허용 가능 (조건 충족 시)

| capability | 허용 args 키 | 확장자 | 실제 I/O |
|------------|--------------|--------|----------|
| `source.read` | `path`만 | `.fx3`만 | 없음 |
| `ir.inspect` | `path`만 | `.ir.json`만 | 없음 |

| 허용 | 거부 |
|------|------|
| `source.read` + `…/a.fx3` | `source.read` + `…/a.ir.json` (`extension_blocked`) |
| `ir.inspect` + `…/a.ir.json` | `ir.inspect` + `…/a.fx3` (`extension_blocked`) |
| args=`{"path":"…"}` | args에 `max_bytes`/`encoding`/기타 키 (`invalid_argument`) |
| 고정 root 기준 상대 path | 절대·`..`·`\`·고정 root 밖 (`path_escape`) |
| 단일 상대 path | path에 `*` / `**` / `?` (`invalid_argument`) |
| args=`{"path":…}`만 | `recursive`·글롭 옵션 (`invalid_argument`) |
| 최상위 허용 키만 | `root` / `canonical_root` / 未知 최상위 키 (`invalid_argument`) |

확장자 판정: path의 **최종 경로 이름**이 해당 접미사로 끝나는지 (대소문자 구분, 소문자 접미사만 허용).
예: `Foo.FX3` deny, `foo.fx3` allow 후보.

### 항상 거부

```text
source.write
process.exec
network.request
runtime.execute
filesystem.delete
filesystem.rename
```

| capability | 정책 | reason (v1) | 실행 |
|------------|------|-------------|------|
| `filesystem.rename` | **항상 deny** | `deny_by_default` | source/destination path를 검사·해석·rename 실행하지 않음 |

`filesystem.rename`은 인자·경로·확장자와 무관하게 거부한다.
고정 canonical root·상대경로 규칙·요청 `root` 금지 계약은 그대로이며, rename을 허용하기 위해 풀리지 않는다.

### 그 외 모든 이름

`unknown_capability` → deny

## 5. Canonical root와 경로 규칙

```text
canonical root:
서버가 설정한 고정 root만 사용한다.
요청자는 root를 지정하거나 변경할 수 없다.
요청 path는 고정 root 기준 상대경로로만 해석한다.
```

| 항목 | 규칙 |
|------|------|
| canonical root | **서버 설정**의 고정 workspace root (배포/프로세스 설정). 요청 JSON 필드가 아님 |
| 요청 `root` / `canonical_root` / 未知 최상위 | 있으면 **deny** (`invalid_argument`) |
| 요청 `path` | 고정 root에 대한 **상대경로**만 |
| 결합 | `canonical_path = normpath(join(canonical_root, path))` 후, 결과가 고정 root 안에 있어야 함 |
| 요청자 권한 | root·한도·경계를 바꿀 수 없음 |

검증 개념 (실 I/O 없이도 계약으로 LOCKED):

```text
서버 설정의 고정 workspace root
+ 요청된 상대경로
→ canonical path 검증
```

허용 path는 다음을 **모두** 만족해야 한다.

- 문자열, 비어 있지 않음
- 상대경로만 (절대 `/…` 또는 `X:…` 금지)
- `\` 금지, `..` 세그먼트 금지, NUL 금지
- 고정 canonical root 밖 금지 → `path_escape`
- wildcard / 재귀 글롭 금지: path에 `*`·`**`·`?` 포함 → `invalid_argument` (확장·매칭 실행 없음)
- `recursive` 등 범위 확장 인자 금지 → 최상위·args 未知 키로 `invalid_argument`

실디렉터리 resolve·`realpath`·symlink 따라가기는 **지금 하지 않는다** (IO=NONE). 문자열·논리 결합만 계약한다.

### Symlink 정책 (현 계약과 충돌 없이)

| 단계 | 정책 |
|------|------|
| 지금 (판정만) | 경로 **문자열**만 검사. symlink를 열어보거나 따라가지 않음 |
| 실 I/O 진입 시 | 고정 canonical root 밖으로 나가는 symlink는 반드시 deny (후보 reason `symlink_blocked`, v2) |
| 금지 | “문자열 검사만으로 symlink-safe”라고 주장하는 것 |
| 금지 | 요청 `root`로 경계를 옮기는 해석 |

## 6. 파일 경계 — 확장자·인코딩·크기

**단일 정의 (이 절이 정본):**

```text
MAX_BYTES = 262144
MAX_OUTPUT_BYTES = 262144
```

- `MAX_BYTES`: **입력** 대상(읽기·inspect content) 상한. 256 KiB.
- `MAX_OUTPUT_BYTES`: **출력** 상한(보고·직렬화 결과). 입력 상한과 **이름·역할이 다르다**. 값은 262144로 잠근다.
- 요청 인자로 어느 쪽도 올리거나 낮추지 못한다. 코드 emit/I/O는 이 문서 잠금만으로 강제하지 않으며, 실 I/O·실행기 길에서 적용한다.

| 규칙 | 값 | deny reason (계약) |
|------|----|-------------------|
| 허용 확장자 전체 | `.fx3`, `.ir.json` | 그 외 → `extension_blocked` |
| `source.read` | `.fx3`만 | 불일치 → `extension_blocked` |
| `ir.inspect` | `.ir.json`만 | 불일치 → `extension_blocked` |
| 인코딩 | UTF-8 **strict** | 디코딩 실패 → `encoding_invalid` |
| replacement character | 허용 안 함 | `encoding_invalid` |
| 크기 | `size > MAX_BYTES` | `size_exceeded` |
| 출력 크기 | `output > MAX_OUTPUT_BYTES` | 실 I/O·실행 길에서 deny (계약 LOCKED; 현 판정 게이트 미적용) |

인코딩·입력 크기 검사는 **in-memory content 또는 실 I/O**가 있을 때 적용한다.
`MAX_OUTPUT_BYTES`는 출력 경로가 생길 때까지 판정 모듈이 emit하지 않는다.

## 6.1 Capability 조합 상승 금지 (LOCKED)

```text
allow(source.read)  ≠  allow(source.write | process.exec | network.request | runtime.execute | filesystem.*)
```

- 각 capability는 **독립**이다. 하나 allow가 다른 권한을 암시하지 않는다.
- grant 집합은 **단조 감소만** 허용하는 것이 목표다: 세션/요청 중 권한을 넓히는 API를 두지 않는다.
- “조합 패키지”(예: read+write 묶음 승인)를 요청하는 최상위·args 키는 `invalid_argument`.
- 현 단계 허용 가능 집합은 여전히 `source.read` · `ir.inspect` 뿐이며, 하드 deny 목록은 항상 deny.

## 7. 결정성

- 같은 요청 dict → 같은 JSON 바이트
- 배열이 요청에 있어도 판정 입력은 단일 요청 객체다
- fixture에서 capability 나열 순서가 달라도 **각 요청 독립 판정**이므로 개별 결과는 변하지 않는다

## 8. 비범위 (아직 구현하지 않는 runtime/I/O)

- 실제 파일 읽기/쓰기/삭제/rename
- 실제 크기·인코딩·symlink 검사 코드
- IR/`.fl` 실행, IR에 `capability_request` 연결
- process / network / `runtime.execute`
- `fx3` CLI, self-hosting
- Core 문법·lexer·parser·lower·`fx3_ir.py` 변경
- reason v2 스키마 승격 (`symlink_blocked`, `sensitive_path` 등)
- 실제 디스크에서 파일을 열어 크기·인코딩을 읽는 것 (판정은 in-memory `content` 바이트만 허용)

## 9. 게이트

```bash
python3 tools/check_capability.py
```

게이트: `python3 tools/check_capability.py` → 구현 정렬 PASS.
고정 `canonical_root`(서버)·요청 `root` 거부·확장자·in-memory `MAX_BYTES`/UTF-8·`filesystem.rename` ALWAYS_DENY 반영.
디스크 I/O·runtime·executor는 여전히 없음.
