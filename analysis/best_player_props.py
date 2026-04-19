#!/usr/bin/env python3
"""
CORRECTED: Ranking home run props by actual value.
Key insight: Compare to PLAYER'S individual rates, not position averages.
"""

print("⚾️  HOME RUN PROPS - CORRECTED VALUE RANKING")
print("=" * 100)
print()

# Player data with market prices
props = {
    "Victor Scott": {"market": 0.03, "team": "BOS", "role": "Backup OF", "baseline": 0.015},
    "José Fermín": {"market": 0.03, "team": "STL", "role": "Backup C", "baseline": 0.02},
    "Willson Contreras": {"market": 0.13, "team": "STL", "role": "Star C", "baseline": 0.10},
    "Jarren Duran": {"market": 0.11, "team": "BOS", "role": "Star OF", "baseline": 0.08},
    "Jordan Walker": {"market": 0.11, "team": "STL", "role": "Star OF", "baseline": 0.08},
    "Roman Anthony": {"market": 0.12, "team": "BOS", "role": "Star OF", "baseline": 0.09},
    "Wilyer Abreu": {"market": 0.12, "team": "BOS", "role": "Star OF", "baseline": 0.09},
    "Trevor Story": {"market": 0.10, "team": "BOS", "role": "Star IF", "baseline": 0.08},
    "Nolan Gorman": {"market": 0.09, "team": "STL", "role": "Star IF", "baseline": 0.07},
    "Ivan Herrera": {"market": 0.09, "team": "STL", "role": "Above-avg C", "baseline": 0.06},
    "Ceddanne Rafaela": {"market": 0.07, "team": "BOS", "role": "Backup IF", "baseline": 0.03},
    "Ramón Urías": {"market": 0.07, "team": "STL", "role": "Backup IF", "baseline": 0.03},
    "Pedro Pagés": {"market": 0.07, "team": "STL", "role": "Backup C", "baseline": 0.03},
    "Carlos Narváez": {"market": 0.06, "team": "STL", "role": "Backup C", "baseline": 0.03},
    "Caleb Durbin": {"market": 0.05, "team": "BOS", "role": "Backup OF", "baseline": 0.02},
    "JJ Wetherholt": {"market": 0.05, "team": "STL", "role": "Backup IF", "baseline": 0.02},
    "Thomas Saggese": {"market": 0.05, "team": "STL", "role": "Backup IF", "baseline": 0.02},
    "Marcelo Mayer": {"market": 0.07, "team": "BOS", "role": "Star SS", "baseline": 0.06},
}

# Analyze each
scores = []
for player, data in props.items():
    market = data["market"]
    baseline = data["baseline"]
    
    # Calculate if market is cheap/expensive vs baseline
    overpriced_pct = (market - baseline) / baseline * 100
    
    # EV if baseline is correct
    ev = baseline - market
    roi = ev / market * 100
    
    scores.append({
        "player": player,
        "market": market,
        "baseline": baseline,
        "overpriced_pct": overpriced_pct,
        "ev": ev,
        "roi": roi,
        "role": data["role"],
        "team": data["team"],
    })

# Sort by ROI (best to worst)
scores.sort(key=lambda x: x["roi"], reverse=True)

print("RANKING (By Expected Value if baseline is correct):")
print("-" * 100)
print(f"{'Rank':<5} {'Player':<20} {'Role':<20} {'Market':<8} {'Baseline':<10} {'vs Fair':<12} {'ROI':<10}")
print("-" * 100)

for rank, s in enumerate(scores, 1):
    overpriced_label = ""
    if s["roi"] > 50:
        indicator = "✅"
    elif s["roi"] > 0:
        indicator = "✓"
    elif s["roi"] > -20:
        indicator = "="
    else:
        indicator = "❌"
    
    print(f"{rank:<5} {s['player']:<20} {s['role']:<20} {s['market']:>6.1%}  {s['baseline']:>8.1%}  {s['overpriced_pct']:>10.0f}%  {s['roi']:>8.0f}%  {indicator}")

print()
print("=" * 100)
print()

# Categorize
undervalued = [s for s in scores if s["roi"] > 50]
fair = [s for s in scores if -20 <= s["roi"] <= 50]
overvalued = [s for s in scores if s["roi"] < -20]

print("📊 CATEGORIZED:")
print()

if undervalued:
    print(f"✅ UNDERVALUED ({len(undervalued)}):")
    for s in undervalued:
        print(f"   • {s['player']:20s} @ {s['market']:.1%} (vs {s['baseline']:.1%} baseline)")
        print(f"      Role: {s['role']}")
        print(f"      Expected ROI: {s['roi']:+.0f}%")
    print()

if fair:
    print(f"= FAIRLY VALUED ({len(fair)}):")
    for s in fair:
        print(f"   • {s['player']:20s} @ {s['market']:.1%} (vs {s['baseline']:.1%} baseline) - {s['roi']:+.0f}% ROI")
    print()

if overvalued:
    print(f"❌ OVERVALUED ({len(overvalued)}):")
    for s in overvalued:
        print(f"   • {s['player']:20s} @ {s['market']:.1%} (vs {s['baseline']:.1%} baseline) - {s['roi']:+.0f}% ROI")
    print()

print("=" * 100)
print()
print("🎯 TOP 3 BEST OPPORTUNITIES:")
print()

for rank, s in enumerate(scores[:3], 1):
    if s["roi"] > 0:
        print(f"{rank}. {s['player']:20s} ({s['role']})")
        print(f"   Market: {s['market']:.1%} | Fair value: {s['baseline']:.1%}")
        print(f"   Why: {s['player']} is {s['team']} {s['role'].lower()}")
        print(f"   ROI if correct: +{s['roi']:.0f}%")
        print()

print("=" * 100)
print()
print("KEY INSIGHT:")
print()
print("The baseline estimates above are GUESSES based on role/team.")
print()
print("To find real edges, you NEED:")
print("  1. This season's actual rate for each player (vs my baseline)")
print("  2. Recent form (hot/cold streaks)")
print("  3. Today's opposing pitcher (strength vs power)")
print("  4. Starting lineup confirmation")
print()
print("If Victor Scott has 0 HR in 50+ ABs, then 3% is OVERPRICED.")
print("If Contreras is on a 3-HR-in-10-games streak, then 13% is UNDERPRICED.")
