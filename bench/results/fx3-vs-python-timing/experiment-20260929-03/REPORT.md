# FX3·Python 시간 원인 조사 보고서

## 판정

STATUS=PASS. 새 교차 순서 표본 6/6이 첫 시도에 4/4 테스트를 통과했고, 원본 로그·코드·단계별 시간·해시를 재검증했다.

이번 표본에서 FX3가 더 오래 걸린 주된 측정 구간은 AI 호출·생성이다. FX3 도구(lowering·실행·테스트)도 Python보다 느렸지만 중앙값 차이는 244ms로, 전체 활성 시간 차이 8,149ms를 설명하기에는 작다. 다만 AI 생성 시간이 FX3 언어 자체의 고정 비용인지, FX3 프롬프트의 문법 정보와 모델 응답 경로 때문인지, 제공자 변동인지까지는 로그만으로 확정할 수 없다.

## 기존 27.2초·15.5초의 한계

기존 FX3 guided 실험의 중앙값은 27,183ms, 기존 Python 실험의 중앙값은 15,506ms였다. 두 실험은 서로 다른 시점과 실험 디렉터리에서 실행되었으므로 그 숫자만으로 FX3 언어와 Python 언어의 인과 차이를 주장하지 않았다.

이번에는 같은 모델·과제·reasoning=high 조건으로 순서를 FX3→Python, Python→FX3, FX3→Python으로 교차했다. 각 scratch 디렉터리는 해당 프롬프트만 가진 독립 세션이었고, 이전 코드·결과는 제공하지 않았다.

## 새 교차 측정

| trial | 순서 | 언어 | AI 생성 | lowering | 실행 | 테스트 | 단계 합계 | wall window | 첫 시도 |
|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| fx3-p1 | 1 | FX3 | 30,738 | 131 | 144 | 30 | 31,043 | 48,423 | PASS |
| python-p1 | 1 | Python | 28,779 | - | 123 | 24 | 28,926 | 43,683 | PASS |
| python-p2 | 2 | Python | 17,857 | - | 88 | 29 | 17,974 | 33,674 | PASS |
| fx3-p2 | 2 | FX3 | 28,777 | 96 | 256 | 24 | 29,153 | 58,845 | PASS |
| fx3-p3 | 3 | FX3 | 26,576 | 94 | 248 | 19 | 26,937 | 47,990 | PASS |
| python-p3 | 3 | Python | 20,890 | - | 94 | 20 | 21,004 | 39,207 | PASS |

단위는 ms이다. 전체 활성 시간 중앙값은 FX3 29,153ms, Python 21,004ms로 FX3가 8,149ms(약 38.8%) 길었다. AI 생성 중앙값은 FX3 28,777ms, Python 20,890ms로 차이가 7,887ms였다. 도구 구간 중앙값(lowering+실행+테스트)은 FX3 361ms, Python 117ms로 차이가 244ms였다. 따라서 활성 시간 차이의 약 96.8%가 AI 생성 구간의 차이다.

쌍별 AI 생성 차이는 pair 1에서 +1,959ms, pair 2에서 +10,920ms, pair 3에서 +5,686ms로 모두 FX3가 길었다. 순서를 바꿔도 FX3가 짧아지는 일은 이 3쌍에서 관찰되지 않았다. 그러나 쌍별 변동 폭이 크므로 제공자·모델 응답 변동을 완전히 배제할 수 없다.

## AI 호출 원자료에서 보이는 차이

FX3 프롬프트는 870바이트, Python 프롬프트는 577바이트였다. 완료 이벤트의 중앙값은 FX3가 output 497 / reasoning 344 토큰, Python이 output 217 / reasoning 76 토큰이었다. FX3 호출에서 모델이 더 많은 reasoning/output을 생성한 사실은 AI 구간이 긴 것과 일치한다. 이것은 “이번 조건에서 FX3 프롬프트의 모델 응답이 더 오래 걸렸다”는 근거이지만, 문법 설명 자체의 토큰 영향과 일시적인 모델 서비스 변동 중 어느 하나만으로 단정할 근거는 부족하다.

## 단계 합계·전체 구간 검증

각 행의 단계 합계는 AI 생성+lowering(해당 시)+실행+테스트로 재계산했고 `metrics.csv`와 일치했다. wall window는 AI 시작부터 테스트 종료까지이며, 단계 사이의 파일 복사·명령 준비 같은 계측하지 않은 공백을 포함한다. 그 공백은 FX3에서 17,380/29,692/21,053ms, Python에서 14,757/15,700/18,203ms였으므로 원인 판정에는 단계 합계를 사용했다.

FX3 pair 2의 최초 호출은 실행 파일 경로 오류로 AI 결과는 생성됐지만 호출 시간 파일이 남지 않았다. 그 호출은 `excluded/fx3-p2-unmetered/`에 보존하고 집계에서 제외했으며, 동일한 독립 프롬프트·모델 조건으로 시간 계측을 갖춘 재호출을 `fx3-p2`로 집계했다. 따라서 누락된 시간을 추정해 결과에 섞지 않았다.

## 기능 검증

6개 trial 모두 동일한 4개 입력에서 실제 출력 `4500`, `5000`, `9999`, `0`을 냈고, 각 `first-test.result`가 PASS이며 종료 코드는 0이었다. FX3는 `lower.py` 종료 코드 0 뒤 FreeLang 실행을 수행했고, Python은 독립 파일을 실제 Python evaluator로 실행했다. 첫 시도 정답률은 FX3 3/3, Python 3/3이다.

## 결론

“왜 이번에는 FX3가 더 오래 걸렸나?”에 대한 원자료 기반 답은 **이번 조건에서 AI 호출·생성 단계가 FX3 쪽에서 중앙값 약 7.9초 더 길었기 때문**이다. lowering·실행·테스트의 추가 비용은 약 0.24초에 그쳤다. 따라서 이번 결과는 FX3 도구 체인이 12초 차이를 만든다는 설명을 지지하지 않는다. AI 생성 지연의 더 세부적인 원인(프롬프트 길이·문법 안내에 따른 reasoning 증가 대 서비스 변동)은 이번 3쌍만으로 확정하지 않으며, 원인 미확정으로 남긴다.

이번 조사에서는 새 검사기·포매터·언어 구현을 만들거나 변경하지 않았다. 72회 Rust 기록과도 섞지 않았다.

## 증거·상태

- 측정값: [metrics.csv](./metrics.csv)
- 교차 순서·실행 조건: [logs/order.tsv](./logs/order.tsv), [logs/commands.tsv](./logs/commands.tsv)
- 원본 프롬프트: [requirements/fx3-guided.txt](./requirements/fx3-guided.txt), [requirements/python.txt](./requirements/python.txt)
- trial별 AI 로그·코드·lowering·실행·테스트 로그: `trials/`
- 전체 증거 해시: [logs/evidence-sha256.tsv](./logs/evidence-sha256.tsv)

FREELANG_AFJ=NOT_APPLICABLE
FREELANG_AFJ_DB=NOT_APPLICABLE
FREELANG_FRONT=NOT_APPLICABLE
OTHER_LANGUAGE=USED
OTHER_LANGUAGE_REASON=비교 기준인 Python 독립 세션과 evaluator를 실행함

변경된 소스 파일: 없음. 실험 증거만 추가했다.
syntax check·테스트·runtime: 6/6 trial, 각 4/4 PASS.
임시 프로세스·포트: 장기 프로세스와 포트 없음.
commit=NOT_COMMITTED
push=NOT_PERFORMED
