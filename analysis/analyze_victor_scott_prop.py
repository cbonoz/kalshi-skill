#!/usr/bin/env python3
"""
Deep analysis of Victor Scott home run prop: 1+ HRs needed, starting lineup only.

Key conditions:
- Victor Scott must be in STARTING LINEUP (pinch-hit at-bats don't count)
- If scratched/not in lineup: resolves to fair market price (refunded)
- Only counts if plays and records plate appearance
- Market: 3% YES, 99% NO
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

print("⚾️ VICTOR SCOTT HOME RUN PROP - Deep Analysis")
print("=" * 80)
print()

# Victor Scott details
print("PLAYER: Victor Scott")
print("TEAM: Boston Red Sox")
print("POSITION: Outfield")
print("GAME: Boston Red Sox vs St. Louis Cardinals")
print("DATE: April 11, 2026 @ 7:15 PM EDT")
print()

print("MARKET CONDITIONS:")
print("-" * 80)
print("✓ Resolution: YES if 1+ home runs")
print("✓ Requirements:")
print("  - Must be in STARTING LINEUP (not pinch-hit)")
print("  - Must record at least one plate appearance")
print("  - If scratched: resolves to fair market price (refunded)")
print()

print("CURRENT PRICING:")
print("-" * 80)
print("YES (market implied): 3%")
print("NO (market implied):  99%")
print("Total:                102% (2% market fee)")
print()

print("FAIR VALUE PROBABILITY (backing out market fee):")
yes_bid = 0.03
no_bid = 0.99
fair_yes = yes_bid / (yes_bid + no_bid)
fair_no = no_bid / (yes_bid + no_bid)

print(f"YES (fair):  {fair_yes:.2%}")
print(f"NO (fair):   {fair_no:.2%}")
print()

# Typical home run rates for different player types
print("TYPICAL HOME RUN RATES (per game, if plays):")
print("-" * 80)
print("• MLB Average (all positions):      ~2-3%")
print("• Outfielders (good):               ~4-6%")
print("• Young prospects:                  ~1-3% (limited track record)")
print()

print("VICTOR SCOTT PROFILE:")
print("-" * 80)
print("Age: ~22 years old (2026)")
print("Role: Young prospect/backup outfielder for Boston")
print("Status: Limited MLB experience as of April 2026")
print("Career HR rate: Likely 1-2% given youth and prospects' typical rates")
print()

print("KEY CALCULATION:")
print("-" * 80)
print()
print("The 3% price breaks down as:")
print()
print("P(YES) = P(in starting lineup) × P(HR | plays) + P(scratched) × 0%")
print()
print("If Victor Scott is highly likely to START:")
print("  3% = P(in start) × P(HR | plays)")
print("  3% = 0.95 × P(HR | plays)  [if 95% chance he starts]")
print("  P(HR | plays) ≈ 3.2%  ← This is what market is pricing")
print()
print("If Victor Scott face SIGNIFICANT scratch risk:")
print("  3% = P(in start) × P(HR | plays)")
print("  3% = 0.70 × P(HR | plays)  [if only 70% chance he starts]")
print("  P(HR | plays) ≈ 4.3%  ← This is what market is pricing")
print()

print("VALUE ASSESSMENT:")
print("=" * 80)
print()
print("🔴 BEARISH CASE (Why 3% might be OVERPRICED):")
print("  • Victor Scott is a young prospect with limited power track record")
print("  • Career HR rate probably 1-2%, not 3-4%")
print("  • Even if plays every day, wouldn't expect 3%+ HRs per game")
print("  • Market might be pricing in the POSSIBILITY he could go deep")
print("  • But statistically, his true rate is likely lower than 3%")
print()

print("🟢 BULLISH CASE (Why 3% might be UNDERPRICED):")
print("  • Boston Red Sox have power hitters in lineup (could inspire confidence)")
print("  • Fenway Park is home field (favorable for left-handed HRs)")
print("  • Cardinals pitching might be weak right now")
print("  • If Scott has recent hot streak, market might be slow to adjust")
print("  • Only needs 1 HR in 1 game (small sample = higher variance)")
print()

print("DECISION FRAMEWORK:")
print("-" * 80)
print()
print("BUY (Victor Scott @ 3%) IF:")
print("  ✓ You have recent game logs showing he's been hitting well")
print("  ✓ You know St. Louis is throwing a weak RHP (if Scott bats RH)")
print("  ✓ Fenway is a good park for his swing (all-or-nothing swinger)")
print("  ✓ He's confirmed in the starting lineup today")
print()

print("DON'T BUY IF:")
print("  ✗ He's a typical prospect with <2% career HR rate")
print("  ✗ No recent hot streak or power surge")
print("  ✗ Unknown lineup status (too much scratch risk)")
print("  ✗ You're just looking for cheap options (3% probability IS cheap)")
print()

print("COMPARISON TO OTHER PROPS:")
print("-" * 80)
print("Victor Scott @ 3%  vs:")
print("  • José Fermín @ 3%  (C for STL - less power, typically)")
print("  • Caleb Durbin @ 5%  (OF for BOS - similar profile)")
print("  • Jarren Duran @ 11% (OF for BOS - established player)")
print()

print("REALISTIC PROBABILITY ESTIMATES:")
print("=" * 80)
print()

# Scenario analysis
scenarios = [
    {
        "name": "Optimistic (Scott is hot/Fenway boost)",
        "lineup_prob": 0.95,
        "hr_rate": 0.035,  # 3.5% per game
    },
    {
        "name": "Base case (typical young prospect)",
        "lineup_prob": 0.90,
        "hr_rate": 0.015,  # 1.5% per game
    },
    {
        "name": "Pessimistic (cold/injury risk)",
        "lineup_prob": 0.75,
        "hr_rate": 0.010,  # 1.0% per game
    },
]

market_price = 0.03

for scenario in scenarios:
    true_prob = scenario["lineup_prob"] * scenario["hr_rate"]
    ev = (true_prob) - market_price  # Win $0.97 if YES (prob × $1), lose $0.03 if NO
    ev_pct = ev / market_price * 100
    
    print(f"{scenario['name']:40s}")
    print(f"  P(HR) = {scenario['lineup_prob']:.0%} lineup × {scenario['hr_rate']:.2%} rate = {true_prob:.2%}")
    print(f"  Expected Value = {true_prob:.2%} - {market_price:.2%} = {ev:+.2%}")
    print(f"  ROI: {ev_pct:+.0f}%")
    if ev > 0:
        print(f"  ✅ PROFITABLE (but {true_prob:.1%} true prob needed)")
    else:
        print(f"  ❌ NEGATIVE EV (-{abs(ev_pct):.0f}% ROI)")
    print()

print("=" * 80)
print()
print("BOTTOM LINE:")
print()
print("Victor Scott @ 3% is a VERY CHEAP BET, but the question is:")
print("Is it TOO cheap (undervalued) or just cheap (correctly priced)?")
print()
print("Market is saying: ~3% chance of 1+ HR if he plays")
print()
print("Reality check:")
print("  • If he's a true 1-2% prospect: THIS IS OVERPRICED (bad bet)")
print("  • If he's a 3-4% power threat: THIS IS FAIR to UNDERPRICED")
print("  • If he's a 5%+ hot streak guy: THIS IS UNDERPRICED (good bet)")
print()
print("ACTION: Check if Victor Scott is confirmed STARTING today")
print("        Check his last 10 games for home run frequency")
print("        Check St. Louis starter's HR/9 allowed")
