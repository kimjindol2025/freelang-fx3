# FX3 공정

나중에 정리할 것을 처음부터 줄인다. 이 문서는 공정이다. Core 문법이 아니다.

## 1. 언어 정본

| 파일 | 역할 |
|---|---|
| `CORE.md` | 확정된 Core 밀도. 사용자 연구 기록이 아니다 |
| `GRAMMAR-V0.md` | 현재 문법 |
| `LOWERING_CONTRACT.md` | `.fx3` → `.fl` 의미 |

역할을 섞지 않는다. 판정 기록은 `USER-STUDY.md`다.

지금 Core는 밀도 잠금이다. `CORE_V1=LOCKED`와 같은 말이 아니다.

## 2. 변경 절차

```text
새 문법 아이디어
  → Core에 바로 넣지 않음
  → 읽기 표본
  → 3사용자 의견
  → 안건
  → 합의
  → golden
  → 구현
```

반대 의견도 기록한다. 중계자는 사용자가 아니다.

## 3. 불변식

- 의미 있는 이름은 유지한다
- `$` 변수 표식은 유지한다
- 공백과 줄바꿈은 문법이 아니다
- `;` 만 식의 경계다
- 같은 `.fx3`는 항상 같은 `.fl` 바이트다
- FX 실행 의미를 이 저장소에서 바꾸지 않는다

## 4. 구현 순서

1. 문법
2. lowerer
3. invalid syntax checker
4. formatter (`;`에서만 나눔. 저장은 한 줄)
5. 기존 FX 실행 검증
6. 실제 코드 적용

별도 FX3 runtime은 필요성이 증명되기 전까지 만들지 않는다.

## 5. 검증

이후 문법 기능마다 아래를 같이 남긴다.

- `.fx3`
- expected `.fl`
- invalid fixture
- lowering PASS
- 이후 semantic PASS

지금 01~04에 invalid를 한꺼번에 새로 깔 안건은 이 문서가 아니다.

## 6. 버전

Core에 들어간 것을 계속 뜯지 않는다. 큰 방향이 달라지면 FX3를 망가뜨리지 말고 다음 세대로 넘긴다. 실험 alias는 Core와 분리한다.

한 줄:

```text
문법 후보 → 3사용자 검토 → Golden → Lowerer → FX 실행 비교 → 실제 코드 → Core 확정
```
