#!/usr/bin/env python3
"""
Analyze US Gas Price market: KXAAAGASW-26APR13
"""

from pykalshi import KalshiClient
from dotenv import load_dotenv

load_dotenv()
client = KalshiClient()

print("🔍 Analyzing Gas Price Market\n", flush=True)

# Try direct lookup
target = "kxaaagasw-26apr13"
print(f"Searching: {target}\n", flush=True)

try:
    market = client.get_market(target)
    
    print(f"✅ Found: {target}\n", flush=True)
    print(f"Title: {market.title}", flush=True)
    print(f"Status: {market.status}", flush=True)
    print(f"Closes: {market.close_time}", flush=True)
    
    # Get pricing
    yes_bid = float(market.yes_bid_dollars) if isinstance(market.yes_bid_dollars, str) else market.yes_bid_dollars
    yes_ask = float(market.yes_ask_dollars) if isinstance(market.yes_ask_dollars, str) else market.yes_ask_dollars
    no_bid = float(market.no_bid_dollars) if isinstance(market.no_bid_dollars, str) else market.no_bid_dollars
    no_ask = float(market.no_ask_dollars) if isinstance(market.no_ask_dollars, str) else market.no_ask_dollars
    
    print(f"\n💰 PRICING:", flush=True)
    print(f"   YES (gas price UP): ${yes_bid:.4f} - ${yes_ask:.4f}", flush=True)
    print(f"   NO (gas price down/flat): ${no_bid:.4f} - ${no_ask:.4f}", flush=True)
    
    # Analysis
    yes_mid = (yes_bid + yes_ask) / 2
    no_mid = (no_bid + no_ask) / 2
    
    print(f"\n📊 MARKET ANALYSIS:", flush=True)
    print(f"   YES probability: {yes_mid * 100:.1f}%", flush=True)
    print(f"   NO probability: {no_mid * 100:.1f}%", flush=True)
    
    # Spreads
    yes_spread = yes_ask - yes_bid
    no_spread = no_ask - no_bid
    yes_spread_pct = (yes_spread / yes_mid * 100) if yes_mid > 0 else 0
    no_spread_pct = (no_spread / no_mid * 100) if no_mid > 0 else 0
    
    print(f"\n📈 SPREAD ANALYSIS:", flush=True)
    print(f"   YES Spread: ${yes_spread:.4f} ({yes_spread_pct:.1f}%)", flush=True)
    print(f"   NO Spread: ${no_spread:.4f} ({no_spread_pct:.1f}%)", flush=True)
    
    # Expected value
    yes_ev = (yes_mid * (1 - yes_ask)) - ((1 - yes_mid) * yes_ask)
    no_ev = (no_mid * (1 - no_ask)) - ((1 - no_mid) * no_ask)
    
    print(f"\n💡 EXPECTED VALUE:", flush=True)
    print(f"   YES EV: ${yes_ev:.4f} ({(yes_ev/yes_ask)*100:.2f}% ROI)", flush=True)
    print(f"   NO EV: ${no_ev:.4f} ({(no_ev/no_ask)*100:.2f}% ROI)", flush=True)
    
    if yes_ev > 0.001:
        print(f"\n   ✅ YES has positive expected value!", flush=True)
        better_bet = "YES"
    elif no_ev > 0.001:
        print(f"\n   ✅ NO has positive expected value!", flush=True)
        better_bet = "NO"
    else:
        if abs(yes_ev) < abs(no_ev):
            print(f"\n   ⚠️  Both negative. YES is slightly better.", flush=True)
            better_bet = "YES"
        else:
            print(f"\n   ⚠️  Both negative. NO is slightly better.", flush=True)
            better_bet = "NO"
    
    print(f"\n🎯 RECOMMENDATION: Bet {better_bet} (if you have a view)", flush=True)
    
except Exception as e:
    print(f"❌ Not found: {e}", flush=True)
    
    # Try searching by series
    print("\nSearching KXAAAGASW series...", flush=True)
    
    try:
        markets = client.get_markets(series_ticker="KXAAAGASW", limit=100)
        print(f"Found {len(markets)} KXAAAGASW markets\n", flush=True)
        
        if markets:
            # Look for April 13
            apr13 = [m for m in markets if m.ticker and "APR13" in m.ticker.upper()]
            print(f"April 13 markets: {len(apr13)}\n", flush=True)
            
            if apr13:
                for m in apr13[:10]:
                    print(f"  {m.ticker}: {str(m.status).split('.')[-1]}", flush=True)
            else:
                print("Available dates:")
                dates = set()
                for m in markets:
                    if m.ticker:
                        parts = m.ticker.split('-')
                        if len(parts) >= 2:
                            dates.add(parts[1])
                
                for d in sorted(dates)[:20]:
                    print(f"  {d}", flush=True)
    except Exception as e2:
        print(f"Series search failed: {e2}", flush=True)
