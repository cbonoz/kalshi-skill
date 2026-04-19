#!/usr/bin/env python3
"""
Deep analysis of S&P 500 markets for April 13 at 4 PM (H1600)
"""

from pykalshi import KalshiClient
from dotenv import load_dotenv

load_dotenv()
client = KalshiClient()

print("🔍 S&P 500 Markets - April 13 at 4 PM (H1600)\n", flush=True)

try:
    # Get all KXINXU markets for Apr13 H1600
    markets = client.get_markets(series_ticker="KXINXU", limit=500)
    
    # Filter for April 13 at 4 PM
    apr13_4pm = [m for m in markets if m.ticker and "APR13H1600" in m.ticker]
    
    print(f"Found {len(apr13_4pm)} S&P 500 strike levels for April 13 at 4 PM\n", flush=True)
    
    # Parse and analyze
    market_data = []
    for m in apr13_4pm:
        if m.yes_bid_dollars is not None and m.yes_ask_dollars is not None:
            # Extract strike price
            parts = m.ticker.split('-')
            strike_str = parts[-1] if len(parts) > 0 else ""
            
            try:
                strike = float(strike_str.replace('T', '').replace('B', ''))
            except:
                continue
            
            yes_bid = float(m.yes_bid_dollars) if isinstance(m.yes_bid_dollars, str) else m.yes_bid_dollars
            yes_ask = float(m.yes_ask_dollars) if isinstance(m.yes_ask_dollars, str) else m.yes_ask_dollars
            no_bid = float(m.no_bid_dollars) if isinstance(m.no_bid_dollars, str) else (1 - yes_ask if yes_ask < 1 else 0)
            no_ask = float(m.no_ask_dollars) if isinstance(m.no_ask_dollars, str) else (1 - yes_bid if yes_bid < 1 else 0)
            
            yes_mid = (yes_bid + yes_ask) / 2 if yes_bid > 0 or yes_ask > 0 else 0
            
            if yes_mid > 0:
                market_data.append({
                    "ticker": m.ticker,
                    "strike": strike,
                    "yes_bid": yes_bid,
                    "yes_ask": yes_ask,
                    "yes_mid": yes_mid,
                    "yes_prob": yes_mid * 100,
                })
    
    # Sort by strike price
    market_data.sort(key=lambda x: x["strike"], reverse=True)
    
    print("S&P 500 STRIKE LADDER (April 13 at 4 PM):", flush=True)
    print("=" * 80, flush=True)
    print(f"{'Index Level':>12} {'YES Bid':>10} {'YES Ask':>10} {'Prob%':>8} {'Liquidity':>12}", flush=True)
    print("-" * 80, flush=True)
    
    # Find median strike (closest to 50%)
    median_idx = None
    for idx, m in enumerate(market_data):
        if abs(m['yes_prob'] - 50) < 5:
            median_idx = idx
            break
    
    # Show markets around median
    for idx, m in enumerate(market_data):
        # Show some context around the median
        if median_idx and abs(idx - median_idx) <= 15:
            prob_marker = ""
            if abs(m['yes_prob'] - 50) < 5:
                prob_marker = " ←← MEDIAN"
            elif m['yes_prob'] > 90:
                prob_marker = " (LIKELY)"
            elif m['yes_prob'] < 10:
                prob_marker = " (UNLIKELY)"
            
            # Liquidity indicator
            if m['yes_bid'] > 0 and m['yes_ask'] < 1:
                liquidity = "GOOD"
            elif m['yes_ask'] > 0:
                liquidity = "LIMITED"
            else:
                liquidity = "NONE"
            
            print(f"{m['strike']:>12,.0f} ${m['yes_bid']:>9.4f} ${m['yes_ask']:>9.4f} {m['yes_prob']:>7.1f}% {liquidity:>12}{prob_marker}", flush=True)
        elif idx < 5 or idx > len(market_data) - 5:
            # Show first and last few
            print(f"{m['strike']:>12,.0f} ${m['yes_bid']:>9.4f} ${m['yes_ask']:>9.4f} {m['yes_prob']:>7.1f}%", flush=True)
        elif idx == 5:
            print("    ... (more markets) ...", flush=True)
    
    print("\n" + "=" * 80, flush=True)
    
    # Market consensus
    if median_idx:
        median_price = market_data[median_idx]['strike']
        print(f"\n💡 MARKET CONSENSUS:", flush=True)
        print(f"   Median expected S&P 500 level: {median_price:,.0f}", flush=True)
        print(f"   Current S&P 500 (trading at 50-50): {median_price:,.0f}", flush=True)
    
    # Find best liquidity/spreads
    print(f"\n📊 BEST LIQUIDITY MARKETS:", flush=True)
    with_spreads = [
        (m, m['yes_ask'] - m['yes_bid']) 
        for m in market_data 
        if m['yes_bid'] > 0 and m['yes_ask'] > 0
    ]
    with_spreads.sort(key=lambda x: x[1])
    
    for m, spread in with_spreads[:10]:
        if m['yes_bid'] > 0:
            spread_pct = (spread / m['yes_mid'] * 100) if m['yes_mid'] > 0 else 0
            print(f"   {m['strike']:>8,.0f}: Spread ${spread:.4f} ({spread_pct:.1f}%), Mid prob {m['yes_prob']:.1f}%", flush=True)

except Exception as e:
    print(f"❌ Error: {e}", flush=True)
    import traceback
    traceback.print_exc()
