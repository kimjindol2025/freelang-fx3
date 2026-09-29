# U1 작은 실측

```text
AGENDA=U1_SMOKE
LOCK=AI_USE_SUCCESS_V0
THRESHOLD=FIRST_VALID_GE_4_OF_6
PACK=CASE_01_06
PYTHON_WALL_CLOCK=NO
REPAIR=NO
MODEL=GROK_BUILD_SESSION
```

[AI-USE-SUCCESS.md](../../AI-USE-SUCCESS.md)의 **U1만** 잰다. U2·U3는 열지 않는다.

## 규칙

1. 생성 전 [AI-ENTRY.md](../../AI-ENTRY.md) 최소 조각을 붙인다.
2. 과제 문구는 `bench/tasks/case-0N.md`의 `TASK_PROMPT`만 본다. `EXPECTED_*` 파일은 채점 전에 읽지 않는다.
3. 첫 시도 한 파일만 낸다. 수리는 하지 않는다.
4. `python3 tools/lower.py first.fx3` 통과 후 기대 `.fl`과 바이트 비교한다.
5. 파이썬·Rust 시간 비교는 하지 않는다.

## PASS

6과제 중 첫 시도 유효(lower PASS ∧ `.fl` 바이트 일치)가 **≥ 4/6**이면 이 묶음 U1 잠정 PASS다.
