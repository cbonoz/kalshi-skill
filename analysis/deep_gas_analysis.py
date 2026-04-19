#!/usr/bin/env python3
"""
Detailed analysis of US gas price markets for April 13
"""

from pykalshi import KalshiClient
from dotenv import load_dotenv

load_dotenv()
client = KalshiClient()

print("🔍 US Gas Price Markets - April 13, 2026\n", flush=True)

try:
    # Get all KXAAAGASW markets
    markets = client.get_markets(series_ticker="KXAAAGASW", limit=500)
    
    # Filter for April 13
    apr13 = [m for m in markets if m.ticker and "APR13" in m.ticker]
    
    print(f"Found {len(apr13)} gas price markets for April 13\n", flush=True)
    
    # Parse and analyze
    market_data = []
    for m in apr13:
        if m.yes_bid_dollars and m.yes_ask_dollars:
            # Extract strike price
            parts = m.ticker.split('-')
            strike = parts[-1] if len(parts) > 0 else ""
            
            yes_bid = float(m.yes_bid_dollars) if isinstance(m.yes_bid_dollars, str) else m.yes_bid_dollars
            yes_ask = float(m.yes_ask_dollars) if isinstance(m.yes_ask_dollars, str) else m.yes_ask_dollars
            no_bid = float(m.no_bid_dollars) if isinstance(m.no_bid_dollars, str) else m.no_bid_dollars
            no_ask = float(m.no_ask_dollars) if isinstance(m.no_ask_dollars, str) else m.no_ask_dollars
            
            yes_mid = (yes_bid + yes_ask) / 2
            no_mid = (no_bid + no_ask) / 2
            
            # Expected values
            yes_ev = (yes_mid * (1 - yes_ask)) - ((1 - yes_mid) * yes_ask)
            no_ev = (no_mid * (1 - no_ask)) - ((1 - no_mid) * no_ask)
            
            # Spreads
            yes_spread = yes_ask - yes_bid
            
            market_data.append({
                "ticker": m.ticker,
                "strike": float(strike),
                "yes_bid": yes_bid,
                "yes_ask": yes_ask,
                "no_bid": no_bid,
                "no_ask": no_ask,
                "yes_mid": yes_mid,
                "no_mid": no_mid,
                "yes_ev": yes_ev,
                "no_ev": no_ev,
                "yes_spread": yes_spread,
                "yes_prob": yes_mid * 100,
                "status": str(m.status).split('.')[-1]
            })
    
    # Sort by strike price
    market_data.sort(key=lambda x: x["strike"])
    
    print("GAS PRICE BETTING LADDER:", flush=True)
    print("=" * 100, flush=True)
    print(f"{'Price':>8} {'Status':<12} {'YES Bid':>10} {'YES Ask':>10} {'Prob%':>8} {'Better EV':>8}", flush=True)
    print("-" * 100, flush=True)
    
    # Identify opportunities
    positive_ev_markets = []
    
    for m in market_data[:30]:  # Show top 30
        better_ev = max(m["yes_ev"], m["no_ev"])
        better_side = "YES" if m["yes_ev"] >= m["no_ev"] else "NO"
        
        # Highlight positive EV
        if better_ev > 0.001:
            marker = "✅"
            positive_ev_markets.append((m["strike"], better_side, better_ev))
        elif better_ev > -0.001:
            marker = "❓"
        else:
            marker = "  "
        
        print(f"${m['strike']:>7.3f} {m['status']:<12} ${m['yes_bid']:>9.4f} ${m['yes_ask']:>9.4f} {m['yes_prob']:>7.1f}% {better_side:>7} {marker}", flush=True)
    
    print("\n" + "=" * 100, flush=True)
    
    if positive_ev_markets:
        print(f"\n✅ OPPORTUNITIES FOUND! ({len(positive_ev_markets)} markets with positive EV):\n", flush=True)
        for strike, side, ev in positive_ev_markets:
            print(f"   ${strike:.3f}: Bet {side} (EV: +${ev:.4f})", flush=True)
    else:
        print(f"\n❌ No positive EV opportunities found.", flush=True)
        print("All markets have negative expected value (market maker fee).\n", flush=True)
        
        # But show the tightest spreads
        best_spreads = sorted(market_data, key=lambda x: x["yes_spread"])[:5]
        print("💡 Best spreads (if you have a contrarian view):\n", flush=True)
        for m in best_spreads:
            print(f"   ${m['strike']:.3f}: Spread = ${m['yes_spread']:.4f}, Mid = {m['yes_prob']:.1f}%", flush=True)
    
    # Show the probability curve
    print(f"\n" + "=" * 100, flush=True)
    print("MARKET CONSENSUS - Implied Gas Prices:\n", flush=True)
    
    # Draw probability distribution
    for m in market_data[:20]:
        bars = int(m['yes_prob'] / 5)
        bar_visual = "█" * bars + "░" * (20 - bars)
        print(f"${m['strike']:.3f} {bar_visual} {m['yes_prob']:.1f}%", flush=True)

except Exception as e:
    print(f"❌ Error: {e}", flush=True)
    import traceback
    traceback.print_exc()
