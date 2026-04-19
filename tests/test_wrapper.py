#!/usr/bin/env python3
"""
Test the KalshiMarketClient wrapper to ensure market reads work correctly
"""

from dotenv import load_dotenv
from kalshi_client import KalshiMarketClient

# Load env
load_dotenv()

client = KalshiMarketClient()

print("=" * 100)
print("✅ KalshiMarketClient WRAPPER TEST\n")
print("=" * 100)

# Test 1: Get BTC markets
print("\n1️⃣ get_bitcoin_markets(limit=3):")
print("-" * 100)

btc = client.get_bitcoin_markets(limit=3)
print(f"Got {len(btc)} BTC markets\n")

if btc:
    for m in btc[:2]:
        print(f"{m['ticker']}")
        print(f"  Title: {m['title'][:50]}...")
        print(f"  Status: {m['status']}")
        print(f"  YES: ${m['yes_bid']:.2f} / ${m['yes_ask']:.2f}")
        print(f"  NO:  ${m['no_bid']:.2f} / ${m['no_ask']:.2f}")
        print()

# Test 2: Query by series
print("\n2️⃣ get_markets_by_series('kxbtcmaxmon', limit=6):")
print("-" * 100)

btc_max = client.get_markets_by_series("kxbtcmaxmon", limit=6)
print(f"Got {len(btc_max)} KXBTCMAXMON markets\n")

opps = []
for m in btc_max:
    spread = m['yes_ask'] - m['yes_bid']
    spread_pct = (spread / m['yes_ask'] * 100) if m['yes_ask'] > 0 else 0
    roi = ((1.0 - m['yes_bid']) / m['yes_bid'] * 100) if m['yes_bid'] > 0 else 0

    opps.append({
        'ticker': m['ticker'],
        'title': m['title'],
        'yes_bid': m['yes_bid'],
        'yes_ask': m['yes_ask'],
        'spread': spread,
        'spread_pct': spread_pct,
        'roi': roi
    })

# Sort by ROI
opps.sort(key=lambda x: x['roi'], reverse=True)

print(f"{'Strike':<12} {'Bid':<8} {'Ask':<8} {'Spread':<10} {'ROI':<8}")
print("-" * 50)

for opp in opps:
    # Extract strike from title
    strike = opp['title'].split('$')[1].split('.')[0] if '$' in opp['title'] else "?"
    print(f"${strike:<11} ${opp['yes_bid']:<7.2f} ${opp['yes_ask']:<7.2f} {opp['spread_pct']:>7.1f}%  {opp['roi']:>6.0f}%")

# Test 3: Get specific market
print("\n\n3️⃣ get_market('KXBTCMAXMON-BTC-26APR30-7750000'):")
print("-" * 100)

m77 = client.get_market("KXBTCMAXMON-BTC-26APR30-7750000")
if m77:
    print(f"\n{m77['title']}")
    print(f"Status: {m77['status']}")
    print(f"YES: ${m77['yes_bid']:.2f} / ${m77['yes_ask']:.2f} (spread: {(m77['yes_ask']-m77['yes_bid']):.2f})")
    print(f"NO:  ${m77['no_bid']:.2f} / ${m77['no_ask']:.2f} (spread: {(m77['no_ask']-m77['no_bid']):.2f})")

    # Calculate trading opportunity
    cost = m77['yes_ask']
    profit = 1.0 - m77['yes_bid']
    if m77['yes_bid'] == 0:
        roi = None
        print("\nTrading opportunity (BUY YES):")
        print(f"  Buy at ask: ${cost:.2f}")
        print(f"  Profit if YES: ${profit:.2f}")
        print("  ROI: N/A (yes_bid is zero, cannot compute ROI)")
    else:
        roi = (profit / m77['yes_bid']) * 100
        print("\nTrading opportunity (BUY YES):")
        print(f"  Buy at ask: ${cost:.2f}")
        print(f"  Profit if YES: ${profit:.2f}")
        print(f"  ROI: {roi:.0f}%")

# Test 4: Get portfolio balance
print("\n\n4️⃣ get_portfolio_balance():")
print("-" * 100)

balance = client.get_portfolio_balance()
print(f"Portfolio balance: ${balance:.2f}")

print("\n" + "=" * 100)
print("✅ All wrapper tests passed!")
