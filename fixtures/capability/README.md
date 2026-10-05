# FX3 capability fixtures (Track 1 / P4)

deny-first **판정만** 검증한다. 디스크 write/rename·프로세스·네트워크·IR 실행이 아니다.

```text
allow/*.request.json + *.decision.json
deny/*.request.json  + *.decision.json
deny/*.content.hex | *.content_len.txt   # in-memory size/UTF-8 only
```

서버 고정 `canonical_root`는 테스트에서 `/canonical/root`다. 요청에 `root` 없음.

계약: [docs/CAPABILITY-CONTRACT.md](../../docs/CAPABILITY-CONTRACT.md)

```bash
python3 tools/check_capability.py
```
