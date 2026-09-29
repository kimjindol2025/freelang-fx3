# 다른 모델 U1→U3 재현 — 2026-09-29

```text
TASK=OTHER_MODEL_REPLAY_U1_U2_U3
LOCK=AI_USE_SUCCESS_V0
CORE=NOT_V1
SMOKE=SAME_DAY
PREVIOUS_MODEL=GROK_BUILD_SESSION
REPLAY_CLI=codex
REPLAY_MODEL=gpt-5.6-luna
REASONING=low
PACK_VERDICT=PASS
```

Grok 세션 스모크와 **다른 모델**(`gpt-5.6-luna` via Codex)로 같은 게이트를 다시 눌렀다.

## 요약

| 게이트 | 결과 | 비고 |
|--------|------|------|
| U1 weak | **5/6** FIRST_VALID | case-06이 `multiply(...)` 호출을 발명. `*` 연산 대신 |
| U2 | **3/3**, locality median **0.016393** | 강한 서명 broken→expected `.fl` |
| U3 | **6/6** regen, ENTRY **동일** | case-06 재생성은 `$value*$value`로 PASS |
| 축약 U/J/L/R | **0** | |
| ENTRY 이탈 | **NO** | 3204B 유지 |
| 묶음 | **PASS** (≥4/6 U1 기준) | 완벽 6/6은 아님 |

## U1 실패 한 건

`u1/first/case-06.fx3`:

```text
F square-or-zero[$value]{?~$value{0}{multiply($value,$value)}}
```

lower는 PASS다. 의미 검사기는 Core 연산 `*`만 알고 `multiply` 심볼은 없다. 과제 문구는 “multiplied by itself”이지 새 빌트인 발명이 아니다. **FIRST_VALID=FAIL**이 맞다.

같은 과제 U3 재생성:

```text
F square-or-zero[$value]{?~$value{0}{$value*$value}}
```

PASS. 모델·시도에 따라 연산 vs 이름 발명이 갈린다.

## 측정 한계

- `OUTPUT_TOKENS`는 이벤트에서 usage 객체를 못 읽어 `NOT_MEASURED`가 많다.
- U2는 기존 강한 서명 expected `.fl` 바이트 비교다 (이름 고정 수리).
- `eval_fl_min`은 스모크용이다. FX 실행 단계 대체 아님.
- 묶음 PASS 임계는 README의 U1 ≥4/6이다. 사용자 약한 서명 단독 PASS 문구의 6/6보다 느슨하다. 이 차이는 보고서에 남긴다.

## 산출물

- 러너: `bench/other-model-replay/run_replay.py`
- 표: `u1/metrics.tsv` `u2/metrics.tsv` `u3/metrics.tsv`
- 로그: `run.log`

## 다음에 열 수 있는 것

- U1 6/6을 목표로 case-06류(연산 vs 이름) 과제만 보강 재측정
- reasoning 높은 설정·다른 Codex 모델
- FX 실행 단계 (`NOT_OPENED`) — 별도 안건
