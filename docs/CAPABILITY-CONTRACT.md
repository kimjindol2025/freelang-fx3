# FX3 Capability Contract (deny-first)

```text
SCHEMA=fx3-capability@1
STATUS=LOCKED_JUDGMENT_ONLY
EXECUTOR=NONE
RUNTIME=NONE
IO=NONE
DEFAULT=DENY
PURPOSE=CONTRACT_ONLY
```

기준일: 2026-10-05

이번 단계는 **capability 선언·검증·거부 판정**만 잠근다.
파일을 읽거나 쓰지 않는다. 프로세스를 실행하지 않는다. 네트워크에 연결하지 않는다.
IR 실행기·FX native·CLI·self-hosting은 범위 밖이다.

`tools/fx3_ir.py`는 수정하지 않는다. capability 요청은 IR 실행과 분리된 **순수 판정 입력**이다.

## 1. 정책

1. 기본값은 항상 **deny**
2. capability가 없거나 빈 문자열이면 deny
3. 알 수 없는 capability는 deny
4. 이름이 맞아도 인자가 계약과 다르면 deny
5. 경로가 허용 root 밖이면 deny
6. 절대경로·`..`·백슬래시·널 바이트 등 탈출 형태는 deny
7. read / write / exec / network는 **서로 독립** capability
8. 이 버전에서 `write`·`exec`·`network`·`runtime.execute`·`filesystem.delete`는 **항상 deny**
9. 허용은 테스트용 순수 판정뿐 (`source.read`, `ir.inspect` + 유효 인자)
10. 판정 결과는 결정적 JSON 바이트

심볼릭 링크 실해석은 하지 않는다. 경로 **문자열 형태**만으로 탈출을 거부한다.

## 2. 요청 schema

```json
{
  "capability": "source.read",
  "args": {"path": "relative/file.fx3"},
  "root": "fixtures",
  "location": {"line": 1, "column": 1}
}
```

| 필드 | 규칙 |
|------|------|
| `capability` | 문자열. 필수. 빈 문자열 deny |
| `args` | 객체. 없으면 `{}`. 알 수 없는 키 deny |
| `root` | 상대 허용 루트 문자열. path가 필요한 capability에서 필수 |
| `location` | `{line,column}` 또는 생략/`null`. 잘못된 값이면 deny(`invalid_location`) |

위치 생략/`null`은 **오류가 아니다**. 결과 `location`은 `null`.

## 3. 판정 결과 schema

```json
{
  "capability": "source.read",
  "decision": "allow",
  "location": {"column": 1, "line": 1},
  "path": "relative/path",
  "reason": "explicit_allow",
  "schema": "fx3-capability@1"
}
```

필드 집합 고정. 직렬화는 `sort_keys=True`, `separators=(",", ":")`, UTF-8, trailing newline 없음.

| decision | 의미 |
|----------|------|
| `allow` | 이번 단계 테스트용 명시 허용 |
| `deny` | 거부 |

| reason | 언제 |
|--------|------|
| `explicit_allow` | 허용 목록 + 인자 유효 |
| `deny_by_default` | 기본 거부 / 하드 거부 목록 |
| `unknown_capability` | 미등록 이름 |
| `invalid_argument` | 인자 타입·키·누락 |
| `path_escape` | 절대경로·`..`·`\`·root 밖 |
| `invalid_location` | location 형태 오류 |
| `empty_capability` | 빈 이름 |

`path`는 요청에 경로가 있으면 정규화 전 요청 문자열을 넣고, 없으면 `null`.

## 4. Capability 목록

### 이번 단계 허용 가능 (조건 충족 시)

| name | args | 비고 |
|------|------|------|
| `source.read` | `path` (상대 문자열, root 안) | 실제 파일 읽기 없음 |
| `ir.inspect` | `path` (상대 문자열, root 안) | 실제 IR 로드 없음 |

### 항상 거부

```text
source.write
process.exec
network.request
runtime.execute
filesystem.delete
```

### 그 외 모든 이름

`unknown_capability` → deny

## 5. 경로 규칙

허용 path는 다음을 **모두** 만족해야 한다.

- 문자열
- 비어 있지 않음
- 절대경로 아님 (`/` 또는 Windows 드라이브 `X:` 형태 시작 금지)
- `\` 포함 금지
- `..` 세그먼트 금지
- NUL (`\0`) 금지
- `root`와 `posixpath.normpath`로 결합했을 때 root 밖으로 나가지 않음

`root` 자체도 상대경로여야 하며 같은 탈출 규칙을 적용한다.

## 6. 결정성

- 같은 요청 dict → 같은 JSON 바이트
- 배열이 요청에 있어도 판정 입력은 단일 요청 객체다
- fixture에서 capability 나열 순서가 달라도 **각 요청 독립 판정**이므로 개별 결과는 변하지 않는다

## 7. 비범위

- IR/`.fl` 실행
- 실제 filesystem / process / network
- `fx3` CLI
- self-hosting
- Core 문법·lexer·parser·lower·`fx3_ir.py` 변경

## 8. 게이트

```bash
python3 tools/check_capability.py
```
