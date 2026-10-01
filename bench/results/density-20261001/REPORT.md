# 로드맵 7 · 밀도 경쟁

```text
ROADMAP7_DENSITY=PASS
SCOPE=stdlib+fixture_01_04
PAIRED=7
FX3_BYTE_WINS=7
FX_BYTE_WINS=0
CORE_SURFACE_CHANGED=NO
HOT_ALIAS_ADOPTED=NO
EXTREME_COMPRESS_ADOPTED=NO
LOSING_NOTATION=DISCARDED_FROM_CORE
NEXT=ROADMAP_8_SURFACE_CUT_OR_STOP
```

표: `bench/results/density-20261001/density.tsv`
진 표기: `bench/results/density-20261001/discarded.tsv`

## 규칙

- 통과 후보만: 로드맵 6 EXEC PASS 범위 (stdlib + fixture 01–04).
- 지표: UTF-8 바이트(주), PROXY_UNITS(보조). 모델 토큰 아님.
- FX3 Core 표기가 FX `.fl`보다 바이트가 작으면 `WIN_FX3`.
- Hot Alias·극단 압축·fixture 05는 **Core에 넣지 않고 버린다** (기록만).
- 표면을 더 깎지 않는다 (로드맵 8).

## 결과 요지

- 7/7 쌍에서 FX3가 바이트 승.
- Core 채택 표기 변경 없음. 이긴 것은 **이미 잠긴 Core 표면**이다.
