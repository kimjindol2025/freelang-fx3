# FX3 프로젝트 작업 규칙

- 대화와 작업 보고는 한국어로 한다.
- 공식 프로젝트명은 `FreeLang FX3`다.
- AI가 `.fx3`를 생성·수정하기 전에 [AI-ENTRY.md](AI-ENTRY.md)를 앞에 둔다. Core 문법을 바꾸지 않는다.
- 사람 가독성은 목표가 아니다. AI 가독성을 우선한다. 의미 있는 이름은 유지한다.
- FX/FX1에서 가져오는 것은 [MINIMUM_FROM_FX.md](MINIMUM_FROM_FX.md)에 적힌 최소 형식뿐이다. 런타임, 앱, builtin 목록을 복사하지 않는다.
- FX2 소스를 가져오지 않는다.
- AFJ, AIA와 문법·런타임을 섞지 않는다.
- 부족한 기능은 JS/TS로 언어 본체를 대체하지 않는다. 부족한 층을 문서에 적는다.
- 문법 후보는 Hard Gate를 통과하기 전에 채택하지 않는다. `J`, `U`, `L`, `R`은 미확정이다.
- `.fx3`가 내려가는 `.fl`을 바꿀 때는 [LOWERING_CONTRACT.md](LOWERING_CONTRACT.md)와 fixture 01을 같이 고친다. 한 소스의 canonical `.fl`은 하나다.
- 검증은 실제 내리기와 실행 결과로 남긴다. 도구가 없으면 PASS라고 적지 않는다.
- 비밀값, 토큰, 개인 키를 문서에 남기지 않는다.
