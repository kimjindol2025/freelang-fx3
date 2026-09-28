# FreeLang FX3

FX 계열의 다음 언어 프로젝트다. FX/FX1 저장소를 복사한 포크가 아니다.

> 사람 가독성은 목표가 아니다. AI 가독성을 우선한다.

한 줄:

**사람이 보기 좋은 코드가 아니라, AI가 가장 안정적으로 읽고 쓰는 고밀도 코드.**

## 계보

```text
FX / FX1   /home/kim/kim/platform/freelang-v11-fx
           실전 사용, native, self-host. 의미의 기준.

FX2        freelang-v11-fx2
           runtime / library / interface 확장.
           이 프로젝트는 FX2를 가져오지 않는다.

FX3        이 프로젝트
           살아남은 최소 의미만 AI 표면으로 다시 쓴다.
```

별도 이름의 `fx1` 저장소는 없다. 이 준비에서 FX/FX1은 `freelang-v11-fx` 한 트리다.

## 현재 상태

구현 없는 언어 설계 프로젝트다.

```text
PROJECT=PREPARED
IMPLEMENT=NO
SOURCE_COPY=NO
FX3_SURFACE=.fx3
CANONICAL_LOWERING=.fl
RUNTIME=NONE
PARSER=NONE
REMOTE=https://github.com/kimjindol2025/freelang-fx3
LOWERING_CONTRACT=LOCKED
```

## 문서

- [LANGUAGE_IDENTITY.md](LANGUAGE_IDENTITY.md) — 이름과 정체성
- [CORE.md](CORE.md) — FX3 Core. 이름은 보존하고 반복 구조만 압축한다
- [USER-STUDY.md](USER-STUDY.md) — 사용자 판정 기록. Core 규칙과 섞지 않는다
- [STRUCTURE.md](STRUCTURE.md) — Core 밖의 맵, 벡터, `try`, `loop` 초안
- [GRAMMAR-V0.md](GRAMMAR-V0.md) — Compact 표면 초안
- [LOWERING_CONTRACT.md](LOWERING_CONTRACT.md) — 잠긴 최소 내리기. Core의 일부
- [MINIMUM_FROM_FX.md](MINIMUM_FROM_FX.md) — FX/FX1에서 가져온 최소와 가져오지 않은 것
- [STATUS.md](STATUS.md) — 준비 판정
- [ROADMAP.md](ROADMAP.md) — 준비 다음 순서
- [AGENTS.md](AGENTS.md) — 작업 규칙

## 표본

golden fixture 01: [examples/handle-rate-single.fx3](examples/handle-rate-single.fx3) → [examples/handle-rate-single.fl](examples/handle-rate-single.fl)

golden fixture 02: [examples/check-and-log.fx3](examples/check-and-log.fx3) → [examples/check-and-log.fl](examples/check-and-log.fl)

golden fixture 03: [examples/make-result.fx3](examples/make-result.fx3) → [examples/make-result.fl](examples/make-result.fl)

03은 한 줄 안의 맵이다. `{key:value,...}`는 맵이고 `{expr;expr}`는 블록이다.

golden fixture 04: [examples/first-id.fx3](examples/first-id.fx3) → [examples/first-id.fl](examples/first-id.fl)

04는 `@$rows[0].id`다. 내리는 도구는 아직 없다. 지금을 완성된 언어로 보지 않는다.
