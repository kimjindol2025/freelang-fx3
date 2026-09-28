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

> **사람 가독성은 버리고, AI 가독성만 남긴다.**

> **의미 있는 이름은 보존하고, 반복되는 구조만 압축한다.**

이 문장이 FX3 Core다. 정본은 [CORE.md](CORE.md)다.

구조, 이름, Hot Alias는 세 층이다. Alias가 실패하면 Alias만 버린다.

줄 수, 들여쓰기, 예쁜 키워드, 긴 함수명은 부차적이다. 남는 기준은 다섯 가지다.

- 경계가 명확함
- 해석이 한 갈래
- 생성 오류가 적음
- 수정 위치가 국소적임
- `.fl`로 정확히 복원됨

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
