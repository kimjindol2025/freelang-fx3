# FX3 준비 다음 순서

준비와 내리기 계약은 잠겼다. 아래 순서를 건너뛰지 않는다.

1. 문법 v0와 `FX3_LOWERING_CONTRACT_LOCK`을 정본으로 유지한다. 축약어는 확정하지 않는다.
2. fixture 01과 02를 `;`에서만 나눠 보여 준다. 저장 파일은 한 줄 그대로다. 실행기는 만들지 않는다.
3. 세 사용자가 fixture 01부터 04를 읽고 판정한다. 다섯 번째 문장은 만들지 않는다. 앱 이전, 기능 추가, 실행기는 이 단계가 아니다.
4. `FX3_MINIMAL_LOWERER_STAGE1`. 폭은 [MIN-IMPL.md](MIN-IMPL.md)다. fixture 01부터 04의 바이트 검사는 통과했다. runtime은 없다. Core v0 완전 확정은 아니다.
5. FX/FX1 코퍼스에서 LLM 토큰 질량을 잰다. FX 코드를 수정하지 않는다.
6. 앱, stdlib, self-host 세 부류에서 실행 결과가 원본 `.fl`과 같은지 본다.
7. 통과한 후보만 밀도 경쟁을 한다. 진 표기는 버린다.
8. 그 다음에야 FX3 표면을 더 깎는다.

FX 런타임을 이 저장소로 복사하는 단계는 없다. FX2를 합치는 단계도 없다. 표면 전용 런타임을 새로 만드는 단계도 없다. 내린 `.fl`은 기존 FX에서 돈다.

## P5 CLI 게이트 (2026-10-06)

쓸 만한 1차 길 PASS: `./bin/fx3 check|lower|ir|cap|test|package verify`.
전용 runtime 없음. 검증·내리기·capability 판정만. 상세 [docs/FX3-CLI.md](docs/FX3-CLI.md).

## Delegated small-tools tier close (2026-10-07)

`manifest-validator`, `config-lint`, `task-list-normalize`와 공통 `check_poc` 레일을
닫았다. 같은 map/list 업무 POC를 반복하지 않는다.

선택: **C (정지)**. 제품은 FreeLangScript/AFJ/FX, FX3는 위임 작은 도구만 유지.
A(vector literal)·B(capability read I/O)는 새 안건·새 gate로만 재개한다.
상세: [docs/FX3-DELEGATED-SMALL-TOOLS-CLOSE.md](docs/FX3-DELEGATED-SMALL-TOOLS-CLOSE.md).
