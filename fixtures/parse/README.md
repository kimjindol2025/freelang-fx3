# FX3 parser fixtures (Track 1 / P1)

lexer token stream → AST만 검증한다. lowering·runtime이 아니다.

```text
valid/     AST PASS + 위치·형태 스모크
invalid/   오류 코드 + line/column REJECT (≥5)
```

게이트:

```bash
python3 tools/check_parse.py
```

golden fixture 01–04(`examples/*.fx3`)도 같은 게이트에서 파싱한다.
