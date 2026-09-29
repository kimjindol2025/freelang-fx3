# FX3·Python 실제 완성 시간 비교

```text
STATUS=PASS
TRIALS=6/6 complete
MODEL=gpt-5.6-luna
REASONING=high
RUST_RESULTS_MIXED=NO
COMMIT=NOT_COMMITTED
PUSH=NOT_PERFORMED
```

## 조건

주문 금액 계산기 요구사항과 동일한 4개 입력을 사용했다. FX3 3회와
Python 3회를 각각 깨끗한 git scratch 디렉터리와 독립 Codex 세션에서
시작했다. 이전 생성 코드·수정 내역·이전 실험 결과는 AI 세션에 제공하지
않았다.

FX3는 `.fx3` 생성 후 `tools/lower.py`와 FreeLang 실행기를 거쳤고, Python은
함수 모듈을 직접 실행했다. 각 trial의 첫 출력, 최종 출력, 원본 AI 이벤트,
명령, 종료 코드, 로그, 코드 해시는 `trials/`에 있다.

## trial 결과

| trial | 언어 | 첫 PASS | 최종 PASS | 수정 | 생성 ms | 수정 ms | lowering ms | 실행 ms | 테스트 ms | active 전체 ms | wall 전체 ms |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fx3-1 | FX3 | NO | YES | 2 | 27,350 | 88,553 | 183 | 451 | 36 | 116,573 | 225,364 |
| fx3-2 | FX3 | NO | YES | 2 | 27,710 | 101,047 | 130 | 164 | 25 | 129,076 | 217,230 |
| fx3-3 | FX3 | NO | YES | 2 | 24,497 | 74,405 | 146 | 172 | 38 | 99,258 | 182,915 |
| python-1 | Python | YES | YES | 0 | 15,349 | 0 | N/A | 130 | 27 | 15,506 | 37,702 |
| python-2 | Python | YES | YES | 0 | 25,791 | 0 | N/A | 104 | 26 | 25,921 | 43,942 |
| python-3 | Python | YES | YES | 0 | 14,047 | 0 | N/A | 128 | 31 | 14,206 | 29,480 |

`active 전체`는 생성 + 수정 + 최종 lowering + 실행 + 테스트의 측정 구간
합이다. `wall 전체`는 첫 AI 호출 시작부터 최종 테스트 PASS 종료까지다.

## 중앙값과 판정

| 지표 | FX3 | Python |
|---|---:|---:|
| 최종 정답률 | 3/3 (100%) | 3/3 (100%) |
| 첫 시도 정답률 | 0/3 (0%) | 3/3 (100%) |
| active 전체 중앙값 | 116,573ms | 15,506ms |
| wall 전체 중앙값 | 217,230ms | 37,702ms |

최종 정확성은 같지만 FX3 active 중앙값은 Python보다 약 7.52배 길다.
따라서 정확성을 유지하면서 FX3가 1% 이상 빠르다는 조건을 충족하지 않는다.

**다음 같은 작업에서 FX3 선택 = NO**

FX3는 세 번 모두 첫 출력에서 lowering 오류가 났고, 각각 두 번의 수정이
필요했다. Python은 세 번 모두 첫 출력으로 4/4 테스트를 통과했다. 이번
실험에서는 FX3를 선택할 시간상 근거가 없다.

## 증거 검증

최종 테스트는 6/6 exit 0이며 모든 출력은 `4500, 5000, 9999, 0`과 일치한다.
전체 실험 파일은 `logs/evidence-sha256.tsv`로 해시를 고정하고, 해시
전수 재검증 결과를 `logs/hash-check.txt`에 남긴다.
