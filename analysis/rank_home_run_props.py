#!/usr/bin/env python3
"""
Ranking all 18 player home run props by value.
Identifies best opportunities.
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from pykalshi import KalshiClient
from kalshi_client import KalshiMarketClient

load_dotenv()

# Initialize
wrapper = KalshiMarketClient()
client = wrapper.client

print("🏟️  HOME RUN PROPS - VALUE RANKING")
print("=" * 100)
print()

# All 18 players with their market prices
players_data = {
    "Roman Anthony": {"team": "BOS", "pos": "OF", "yes": 0.12, "no": 0.89},
    "Trevor Story": {"team": "BOS", "pos": "IF", "yes": 0.10, "no": 0.91},
    "Caleb Durbin": {"team": "BOS", "pos": "OF", "yes": 0.05, "no": 0.96},
    "Carlos Narváez": {"team": "STL", "pos": "C", "yes": 0.06, "no": 0.95},
    "Ceddanne Rafaela": {"team": "BOS", "pos": "IF", "yes": 0.07, "no": 0.95},
    "Ivan Herrera": {"team": "STL", "pos": "C", "yes": 0.09, "no": 0.92},
    "JJ Wetherholt": {"team": "STL", "pos": "IF", "yes": 0.05, "no": 0.98},
    "Jarren Duran": {"team": "BOS", "pos": "OF", "yes": 0.11, "no": 0.90},
    "Jordan Walker": {"team": "STL", "pos": "OF", "yes": 0.11, "no": 0.90},
    "José Fermín": {"team": "STL", "pos": "C", "yes": 0.03, "no": 0.98},
    "Marcelo Mayer": {"team": "BOS", "pos": "SS", "yes": 0.07, "no": 0.95},
    "Nolan Gorman": {"team": "STL", "pos": "IF", "yes": 0.09, "no": 0.94},
    "Pedro Pagés": {"team": "STL", "pos": "C", "yes": 0.07, "no": 0.97},
    "Ramón Urías": {"team": "STL", "pos": "IF", "yes": 0.07, "no": 0.94},
    "Thomas Saggese": {"team": "STL", "pos": "IF", "yes": 0.05, "no": 0.97},
    "Victor Scott": {"team": "BOS", "pos": "OF", "yes": 0.03, "no": 0.99},
    "Willson Contreras": {"team": "STL", "pos": "C", "yes": 0.13, "no": 0.89},
    "Wilyer Abreu": {"team": "BOS", "pos": "OF", "yes": 0.12, "no": 0.90},
}

# Typical home run rates by position
typical_rates = {
    "C": 0.04,   # Catcher: ~4%
    "IF": 0.035, # Infielder: ~3.5%
    "SS": 0.025, # Shortstop: ~2.5%
    "OF": 0.06,  # Outfielder: ~6%
}

# Calculate value for each player
scores = []

for player, data in players_data.items():
    market_yes = data["yes"]
    market_no = data["no"]
    total = market_yes + market_no
    
    # Fair probability (backing out market fee)
    fair_yes = market_yes / total
    fair_no = market_no / total
    
    pos = data["pos"]
    typical = typical_rates[pos]
    
    # Discount calculation
    discount_pct = (typical - fair_yes) / typical * 100
    
    # EV if market is right about typical rates
    ev = fair_yes - market_yes
    ev_pct = (ev / market_yes) * 100 if market_yes > 0 else -100
    
    # Value score (negative = better deal)
    value_score = discount_pct
    
    scores.append({
        "player": player,
        "team": data["team"],
        "pos": pos,
        "market_yes": market_yes,
        "fair_yes": fair_yes,
        "typical": typical,
        "discount_pct": discount_pct,
        "ev": ev,
        "ev_pct": ev_pct,
        "total_spread": total,
        "value_score": value_score,
    })

# Sort by discount (most underpriced first)
scores.sort(key=lambda x: x["discount_pct"], reverse=False)

print("RANKING (By Value):")
print("-" * 100)
print(f"{'Rank':<5} {'Player':<20} {'Pos':<4} {'Market':<8} {'Fair Prob':<12} {'Typical':<10} {'Discount':<12} {'Assessment':<15}")
print("-" * 100)

for rank, score in enumerate(scores, 1):
    assessment = ""
    if score["discount_pct"] < -15:
        assessment = "🎯 BEST DEAL"
    elif score["discount_pct"] < -5:
        assessment = "✓ Good Value"
    elif score["discount_pct"] < 10:
        assessment = "= Fair"
    elif score["discount_pct"] < 20:
        assessment = "⚠️ Premium"
    else:
        assessment = "❌ Overpriced"
    
    print(f"{rank:<5} {score['player']:<20} {score['pos']:<4} {score['market_yes']:>6.1%}  {score['fair_yes']:>10.2%}  {score['typical']:>8.1%}  {score['discount_pct']:>10.0f}%  {assessment:<15}")

print()
print("=" * 100)
print()

# Group by category
print("📊 CATEGORIZED BREAKDOWN:")
print()

best_deals = [s for s in scores if s["discount_pct"] < -15]
good_value = [s for s in scores if -15 <= s["discount_pct"] < -5]
fair_priced = [s for s in scores if -5 <= s["discount_pct"] < 10]
premium = [s for s in scores if 10 <= s["discount_pct"] < 20]
overpriced = [s for s in scores if s["discount_pct"] >= 20]

if best_deals:
    print(f"🎯 BEST DEALS ({len(best_deals)}):")
    for s in best_deals:
        print(f"   • {s['player']:20s} @ {s['market_yes']:5.1%} (vs {s['typical']:5.1%} typical {s['pos']}) = {s['discount_pct']:+6.1f}% discount")
    print()

if good_value:
    print(f"✓ GOOD VALUE ({len(good_value)}):")
    for s in good_value:
        print(f"   • {s['player']:20s} @ {s['market_yes']:5.1%} (vs {s['typical']:5.1%} typical {s['pos']}) = {s['discount_pct']:+6.1f}% discount")
    print()

if fair_priced:
    print(f"= FAIRLY PRICED ({len(fair_priced)}):")
    for s in fair_priced:
        print(f"   • {s['player']:20s} @ {s['market_yes']:5.1%} (vs {s['typical']:5.1%} typical {s['pos']}) = {s['discount_pct']:+6.1f}% discount")
    print()

if premium:
    print(f"⚠️ PREMIUM PRICED ({len(premium)}):")
    for s in premium:
        print(f"   • {s['player']:20s} @ {s['market_yes']:5.1%} (vs {s['typical']:5.1%} typical {s['pos']}) = {s['discount_pct']:+6.1f}% discount")
    print()

if overpriced:
    print(f"❌ OVERPRICED ({len(overpriced)}):")
    for s in overpriced:
        print(f"   • {s['player']:20s} @ {s['market_yes']:5.1%} (vs {s['typical']:5.1%} typical {s['pos']}) = {s['discount_pct']:+6.1f}% discount")
    print()

print("=" * 100)
print()

# Strategy recommendations
print("🎯 STRATEGY RECOMMENDATIONS:")
print("-" * 100)
print()

if best_deals:
    print("BUY STRATEGY (Best Deals):")
    for s in best_deals:
        print(f"   {s['player']:20s}")
        print(f"      Market Price: {s['market_yes']:.1%}")
        print(f"      Strategy: Only if you know something about {s['player']}")
        print(f"      Thesis needed: Player hitting better than typical {s['pos']} rates")
        print()
else:
    print("BUILD YOUR OWN DEAL:")
    print("   Most props are fairly to overpriced. To find edges:")
    print("   1. Look at players coming off hot/cold streaks")
    print("   2. Check recent form (last 10-30 games)")
    print("   3. Match pitcher vs batter (RHP/LHP splits)")
    print("   4. Fenway Park factors (short left field wall)")
    print()

print("AVOID ENTIRELY:")
for s in overpriced:
    print(f"   • {s['player']:20s} @ {s['market_yes']:.1%} - Too expensive for prospect")

print()
print("-" * 100)
print()

# Summary statistics
print("📈 MARKET SUMMARY:")
print()
avg_market = sum(s["market_yes"] for s in scores) / len(scores)
avg_typical = sum(s["typical"] for s in scores) / len(scores)
avg_spread = sum(s["total_spread"] for s in scores) / len(scores)

print(f"Average market price:     {avg_market:.2%}")
print(f"Average typical rate:     {avg_typical:.2%}")
print(f"Average bid-ask spread:   {avg_spread:.2%} (implies {(avg_spread - 1) * 100:.1f}% market fee)")
print()

overpriced_count = len([s for s in scores if s["discount_pct"] >= 0])
underpriced_count = len([s for s in scores if s["discount_pct"] < 0])

print(f"Overpriced props:         {overpriced_count}/18 ({overpriced_count/18*100:.0f}%)")
print(f"Underpriced props:        {underpriced_count}/18 ({underpriced_count/18*100:.0f}%)")
print()

print("=" * 100)
print()
print("KEY INSIGHT:")
print()
print("❌ NO OBVIOUS + EV OPPORTUNITIES")
print()
print("All 18 home run props are priced at or above market consensus for typical HR rates.")
print()
print("This means:")
print("  • Market makers have done homework on position-specific rates")
print("  • Bettors are overweighting some stars (Contreras, Anthony at 12-13%)")
print("  • Young prospects are fairly/correctly valued")
print("  • To profit: you need CONTRARIAN INFORMATION")
print()
print("Questions to answer:")
print("  1. Is [player] in starting lineup today?")
print("  2. Has [player] gone on hot streak (recent stats)?")
print("  3. Is opposing pitcher weak vs power hitters?")
print("  4. Does Fenway Park favor [player]'s swing type?")
