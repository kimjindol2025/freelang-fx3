fn profile_band(profile: &ScoredProfile) -> String {
    if profile.score >= 70 { profile.name.clone() } else { "unrated".to_string() }
}
