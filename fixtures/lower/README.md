# FX3 lowering fixtures (Track 1 / P2)

located AST → 결정적 `.fl` 바이트만 검증한다. runtime/IR이 아니다.

```text
valid/     AST lower ≡ expected .fl (+ 스모크 expect)
invalid/   unsupported / multi-form 거부 + 위치
```

게이트:

```bash
python3 tools/check_lower.py
```

golden fixture 01–04(`examples/*.{fx3,fl}`)도 같은 게이트에서 byte-match한다.
기존 `tools/lower.py`는 수정하지 않는다.
