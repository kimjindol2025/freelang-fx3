# FreeLang FX3 언어 정체성

```text
FAMILY=FreeLang
OFFICIAL=FreeLang FX3
COLLOQUIAL=FX3
SURFACE=Compact FX
LOWER_TARGET=FX .fl
STATUS=prepared-not-implemented
```

## 명칭

- 공식 문서 제목: `FreeLang FX3`
- 짧은 이름: `FX3`
- 저장소·폴더 이름: `freelang-fx3`
- AI가 읽고 쓰는 표면: Compact FX. 파일 확장자 `.fx3`
- 의미의 복구 표현: FX `.fl`

## 철학

> **사람 가독성은 목표가 아니다. AI 가독성을 우선한다.**

> **의미 있는 이름은 보존하고, 반복되는 구조만 압축한다.**

이 문장이 FX3 Core다. 사용자 정본은 [CORE.md](CORE.md)의 Grok 사용자 입장이다.

매일 쓰는 기준은 다섯 개다.

1. 한 갈래로만 읽힌다. 식의 끝은 `;`다.
2. 이름은 남긴다. 다시 열 때 사전이 필요하면 진 것이다.
3. 구조만 접는다. `F`, `?`, `@`, `$`.
4. 고친 자리는 그 자리로 끝난다.
5. 같은 표면은 같은 `.fl` 바이트로 내려간다. 실행은 기존 FX다. 표면의 런타임은 만들지 않는다.

더 예쁘게 만들지 않고, 더 짧게도 만들지 않는다.

```text
newline ≠ syntax
whitespace ≠ syntax
; = EXPR_END
```

## 관계

| 항목 | 관계 |
|------|------|
| FX / FX1 `freelang-v11-fx` | 의미 기준. 최소 형식만 참조한다 |
| FX2 `freelang-v11-fx2` | 확장 세대. 가져오지 않는다 |
| AFJ | 다른 언어. 문법과 런타임을 섞지 않는다 |
| AIA | 다른 언어. 구현을 가져오지 않는다 |

FX3는 FX 실행 의미를 새 표면으로 다시 쓰는 언어다. FX 앱, C 런타임, FX2 라이브러리를 이어 받는 저장소가 아니다.
