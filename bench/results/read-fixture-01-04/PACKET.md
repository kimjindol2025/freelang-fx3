# fixture 01–04 읽기 패킷

```text
READ_PACKET=fixture_01_04
CORE_CUT=NO
FIXTURE_05=NO
```

## case-01

### 저장 (한 줄)

```fx3
F fetch-rate[$req]{$currency=str_upper(@$req.params.currency);$body=http-get-body(RATE_URL);?~$body{json-err("missing rate")}{json-ok($body)}}
```

### 표시 (`show` · `;`만 나눔)

```fx3
F fetch-rate[$req]{$currency=str_upper(@$req.params.currency);
$body=http-get-body(RATE_URL);
?~$body{json-err("missing rate")}{json-ok($body)}}
```

### lower ≡ golden `.fl`: **YES**

## case-02

### 저장 (한 줄)

```fx3
F welcome-profile[$req]{$body=load-profile($req);$name=str_upper(@$body.user.name);?~$name{missing-name()}{welcome($name)}}
```

### 표시 (`show` · `;`만 나눔)

```fx3
F welcome-profile[$req]{$body=load-profile($req);
$name=str_upper(@$body.user.name);
?~$name{missing-name()}{welcome($name)}}
```

### lower ≡ golden `.fl`: **YES**

## case-03

### 저장 (한 줄)

```fx3
F route-payload[$req]{$payload=read-payload($req);$kind=@$payload.meta.kind;?@$payload.ok{accept($kind)}{reject($kind)}}
```

### 표시 (`show` · `;`만 나눔)

```fx3
F route-payload[$req]{$payload=read-payload($req);
$kind=@$payload.meta.kind;
?@$payload.ok{accept($kind)}{reject($kind)}}
```

### lower ≡ golden `.fl`: **YES**

## case-04

### 저장 (한 줄)

```fx3
F audit-score[$x]{start-audit($x);?$x>=80{mark-pass($x)}{mark-review($x)};finish-audit($x)}
```

### 표시 (`show` · `;`만 나눔)

```fx3
F audit-score[$x]{start-audit($x);
?$x>=80{mark-pass($x)}{mark-review($x)};
finish-audit($x)}
```

### lower ≡ golden `.fl`: **YES**
