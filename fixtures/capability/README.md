# FX3 capability fixtures (Track 1 / P4)

deny-first **판정만** 검증한다. 파일·프로세스·네트워크·IR 실행이 아니다.

```text
allow/*.request.json + *.decision.json
deny/*.request.json  + *.decision.json
```

계약: [docs/CAPABILITY-CONTRACT.md](../../docs/CAPABILITY-CONTRACT.md)

```bash
python3 tools/check_capability.py
```
