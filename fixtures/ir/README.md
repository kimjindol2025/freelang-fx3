# FX3 IR fixtures (Track 1 / P3)

AST → 결정적 IR/ABI JSON만 검증한다. 실행기·capability·runtime이 아니다.

```text
valid/*.ir.json   golden IR bytes (fixture 01–04)
invalid/          schema/reserved/loc 거부
```

계약: [docs/IR-ABI-CONTRACT.md](../../docs/IR-ABI-CONTRACT.md)

```bash
python3 tools/check_ir.py
```
