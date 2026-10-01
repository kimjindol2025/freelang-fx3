# fixture 01–04 읽기 표결

```text
AGENDA=READ_FIXTURE_01_04
STATUS=OPEN
CORE_CUT=NO
FIXTURE_05=NO
DATE=2026-10-01
```

패킷: [PACKET.md](PACKET.md)

문항: 저장 한 줄 · `show`로 `;`만 나눈 표시 · lower≡golden `.fl` — **읽기 판정 OK인가?**

| 사용자 | 역할 | 표 | 날짜 | 메모 |
|--------|------|----|------|------|
| 1 | 그록빌더 | READ_OK | 2026-10-01 | 패킷·SEMI_DISPLAY·WHITESPACE_SAME_FL 기준. 문법 추가 없음 |
| 2 | 그록 | READ_OK | 2026-10-01 | 01–04 유지. SEMI_DISPLAY만. Core 안 깎음 |
| 3 | 지피티 | — | — | |

허용: `READ_OK` · `HOLD` · `REJECT`

```text
TALLY=2_OF_3
AWAITING=USER_3_GPT
CLOSED_IF=three votes recorded (REJECT=0 preferred)
```
