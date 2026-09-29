#[derive(Debug)]
struct Profile { name: String }
#[derive(Debug)]
struct Order { subtotal: i64, tax: i64 }
#[derive(Debug)]
struct Payload { ok: i64, code: String }
#[derive(Debug)]
struct EmailProfile { email: Option<String> }
#[derive(Debug)]
struct Row { code: String }
#[derive(Debug)]
struct ScoredProfile { name: String, score: i64 }
#[derive(Debug)]
struct Side { value: i64 }
#[derive(Debug)]
struct Sides { left: Side, right: Side }
#[derive(Debug)]
struct Metrics { a: i64, b: i64, c: i64 }

fn pick_name(profile: &Profile) -> String { profile.name.clone() }
fn add_points(score: i64, bonus: i64) -> i64 { score + bonus }
fn status_label(score: i64) -> &'static str { if score >= 60 { "pass" } else { "retry" } }
fn upper_city(city: &str) -> String { city.to_uppercase() }
fn order_total(order: &Order) -> i64 { order.subtotal + order.tax }
fn choose_code(payload: &Payload) -> String {
    if payload.ok >= 1 { payload.code.clone() } else { "rejected".to_string() }
}
fn fallback_email(profile: &EmailProfile) -> String {
    profile.email.clone().unwrap_or_else(|| "none".to_string())
}
fn indexed_code(rows: &[Row]) -> String { rows[1].code.clone() }
fn profile_band(profile: &ScoredProfile) -> String {
    if profile.score >= 70 { profile.name.clone() } else { "unrated".to_string() }
}
fn side_product(data: &Sides) -> i64 { data.left.value * data.right.value }
fn score_band(data: &Metrics) -> &'static str {
    if data.a + data.b + data.c >= 100 { "high" } else { "low" }
}
fn matrix_cell(matrix: &[Vec<i64>], i: usize) -> i64 { matrix[i][0] }

fn main() {
    assert_eq!(pick_name(&Profile { name: "Ada".into() }), "Ada");
    assert_eq!(add_points(7, 5), 12);
    assert_eq!(status_label(72), "pass");
    assert_eq!(upper_city("seoul"), "SEOUL");
    assert_eq!(order_total(&Order { subtotal: 100, tax: 18 }), 118);
    assert_eq!(choose_code(&Payload { ok: 1, code: "A7".into() }), "A7");
    assert_eq!(fallback_email(&EmailProfile { email: None }), "none");
    assert_eq!(indexed_code(&[Row { code: "A1".into() }, Row { code: "B2".into() }]), "B2");
    assert_eq!(profile_band(&ScoredProfile { name: "Mina".into(), score: 81 }), "Mina");
    assert_eq!(side_product(&Sides { left: Side { value: 6 }, right: Side { value: 7 } }), 42);
    assert_eq!(score_band(&Metrics { a: 40, b: 35, c: 30 }), "high");
    assert_eq!(matrix_cell(&vec![vec![10, 11], vec![20, 21]], 1), 20);
    println!("REFERENCE_RUST_PASS=12/12");
}
