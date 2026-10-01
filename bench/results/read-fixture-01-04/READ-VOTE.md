# fixture 01–04 읽기 표결

```text
AGENDA=READ_FIXTURE_01_04
STATUS=CLOSED
RESULT=PASS
CORE_CUT=NO
FIXTURE_05=NO
DATE=2026-10-01
TALLY=3_OF_3
READ_OK=3
HOLD=0
REJECT=0
```

패킷: [PACKET.md](PACKET.md)

문항: 저장 한 줄 · `show`로 `;`만 나눈 표시 · lower≡golden `.fl` — **읽기 판정 OK인가?**

이 표결은 **새 언어 기능 승인이 아니다.** fixture 01–04의 기존 의미를 어떻게 읽을지 확정한다.

| 사용자 | 역할 | 표 | 날짜 | 메모 |
|--------|------|----|------|------|
| 1 | 그록빌더 | READ_OK | 2026-10-01 | 패킷·SEMI_DISPLAY·WHITESPACE_SAME_FL 기준. 문법 추가 없음 |
| 2 | 그록 | READ_OK | 2026-10-01 | 01–04 유지. SEMI_DISPLAY만. Core 안 깎음 |
| 3 | 지피티 | READ_OK | 2026-10-01 | 저장 1줄 / SEMI_DISPLAY만 / lower ≡ golden .fl. fixture 01–04 한정. 문법 추가·fixture 05·Core 삭감 없음. (패킷 원문은 요약 범위 기준 판정) |

허용: `READ_OK` · `HOLD` · `REJECT`

## 닫힘

```text
CLOSED_IF=three votes recorded AND REJECT=0
APPLIED=2026-10-01
READ_FIXTURE_01_04=PASS
NEW_LANGUAGE_FEATURE=NO
```
