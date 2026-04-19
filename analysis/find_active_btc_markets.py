#!/usr/bin/env python3
"""
Find ALL actively-trading Bitcoin markets on Kalshi
Focus on ACTIVE markets only (not INITIALIZED)
"""

from pykalshi import KalshiClient
from pykalshi.models import MarketStatus
from dotenv import load_dotenv

load_dotenv()
client = KalshiClient()

print("🔍 Finding ALL Active Bitcoin Markets\n", flush=True)

# List all Bitcoin series to search
bitcoin_series = [
    "KXBTC",
    "KXBTCD", 
    "KXBTCMAXMON",
    "KXBTC15M",
    "KXBTCH",  # Hourly?
    "KXBTCW",  # Weekly?
]

all_active_markets = []

for series in bitcoin_series:
    try:
        print(f"Searching {series}...", flush=True)
        markets = client.get_markets(series_ticker=series, limit=500)
        
        # Filter for ACTIVE status
        active = [m for m in markets if m and "ACTIVE" in str(m.status)]
        
        if active:
            print(f"  ✅ Found {len(active)} ACTIVE markets", flush=True)
            all_active_markets.extend([(series, m) for m in active])
        else:
            print(f"  ❌ No ACTIVE markets (found {len(markets)} total, all are INITIALIZED)", flush=True)
    
    except Exception as e:
        print(f"  Error: {e}", flush=True)

print(f"\n" + "=" * 80, flush=True)
print(f"TOTAL ACTIVE MARKETS FOUND: {len(all_active_markets)}\n", flush=True)

if all_active_markets:
    # Group by series
    by_series = {}
    for series, market in all_active_markets:
        if series not in by_series:
            by_series[series] = []
        by_series[series].append(market)
    
    for series in sorted(by_series.keys()):
        markets = by_series[series]
        print(f"\n📊 {series} ({len(markets)} markets):", flush=True)
        print(f"{'Ticker':<50} {'YES Bid':>10} {'YES Ask':>10} {'Spread%':>8}", flush=True)
        print("-" * 80, flush=True)
        
        # Sort by spread
        markets_with_spread = []
        for m in markets:
            if m.yes_bid_dollars and m.yes_ask_dollars:
                yes_bid = float(m.yes_bid_dollars) if isinstance(m.yes_bid_dollars, str) else m.yes_bid_dollars
                yes_ask = float(m.yes_ask_dollars) if isinstance(m.yes_ask_dollars, str) else m.yes_ask_dollars
                spread_pct = ((yes_ask - yes_bid) / ((yes_bid + yes_ask) / 2) * 100) if (yes_bid + yes_ask) > 0 else 0
                markets_with_spread.append((m, yes_bid, yes_ask, spread_pct))
        
        markets_with_spread.sort(key=lambda x: x[3])
        
        for m, yes_bid, yes_ask, spread_pct in markets_with_spread[:20]:
            print(f"{m.ticker:<50} ${yes_bid:>9.4f} ${yes_ask:>9.4f} {spread_pct:>7.1f}%", flush=True)

else:
    print("❌ No actively-trading Bitcoin markets found!", flush=True)
    print("\nAll short-term markets (daily, hourly, 15-min) are in INITIALIZED status.", flush=True)
    print("Check back later when trading begins.", flush=True)
