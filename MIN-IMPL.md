# 최소 구현

```text
AGENDA=MIN_IMPL
WIDTH=LOWER_01_04_EXACT_BYTES
RUNTIME=NO
FIXTURE_05=NO
CORE_V0_FINAL=NO
```

폭은 이것뿐이다.

- 입력은 `examples/`의 fixture 01부터 04 `.fx3`다.
- 출력은 같은 이름의 golden `.fl`과 바이트가 같아야 한다.
- 도구는 `tools/lower.py`다. 표면 런타임이 아니다.
- 통과해도 Core v0 완전 확정이 아니다.
- 이 단계의 바이트 검사는 셋의 동의로 닫혔다. 다음 문장이 오기 전에 폭을 넓히지 않는다. FX 실행은 열지 않는다.

넣지 않는 것:

- fixture 05
- 동적 인덱스와 반복 `?~`의 새 표본
- `U`, `J` 같은 alias
- FX 실행
- 앱 이전

검사:

```text
python3 tools/lower.py --check
```
