fn score_band(data: &Metrics) -> &'static str {
    if data.a + data.b + data.c >= 100 { "high" } else { "low" }
}
