#!/usr/bin/env python3
from pykalshi import KalshiClient
from dotenv import load_dotenv

load_dotenv()
client = KalshiClient()

print("🔍 Searching for 15-minute Bitcoin markets\n", flush=True)

# Try direct lookup
target = "kxbtc15m-26apr111900"
print(f"Trying direct lookup: {target}", flush=True)

try:
    market = client.get_market(target)
    print(f"✅ Found: {target}", flush=True)
    print(f"   Title: {market.title}", flush=True)
    print(f"   Status: {market.status}", flush=True)
    if market.yes_bid_dollars and market.yes_ask_dollars:
        yes_bid = float(market.yes_bid_dollars) if isinstance(market.yes_bid_dollars, str) else market.yes_bid_dollars
        yes_ask = float(market.yes_ask_dollars) if isinstance(market.yes_ask_dollars, str) else market.yes_ask_dollars
        print(f"   YES: ${yes_bid:.4f} - ${yes_ask:.4f}", flush=True)
except Exception as e:
    print(f"❌ Not found: {e}\n", flush=True)

# Try searching KXBTC15M series
print("\nSearching KXBTC15M series...", flush=True)

try:
    markets = client.get_markets(series_ticker="KXBTC15M", limit=100)
    print(f"Found {len(markets)} 15-min markets\n", flush=True)
    
    if markets:
        # Look for April 11 markets
        apr11 = [m for m in markets if m.ticker and "APR11" in m.ticker.upper()]
        print(f"April 11 markets: {len(apr11)}\n", flush=True)
        
        if apr11:
            # Show sample
            print("Sample April 11 markets:", flush=True)
            for m in apr11[:15]:
                if m.yes_bid_dollars and m.yes_ask_dollars:
                    yes_bid = float(m.yes_bid_dollars) if isinstance(m.yes_bid_dollars, str) else m.yes_bid_dollars
                    yes_ask = float(m.yes_ask_dollars) if isinstance(m.yes_ask_dollars, str) else m.yes_ask_dollars
                    yes_info = f"${yes_bid:.4f}-${yes_ask:.4f}"
                else:
                    yes_info = "No prices"
                print(f"  {m.ticker}: {str(m.status).split('.')[-1]:<15} {yes_info}", flush=True)
        else:
            # Show all available
            print("All markets found:", flush=True)
            dates = set()
            for m in markets:
                if m.ticker:
                    parts = m.ticker.split('-')
                    if len(parts) >= 2:
                        dates.add(parts[1])
            
            print(f"Dates: {sorted(dates)}\n", flush=True)
            for m in markets[:20]:
                print(f"  {m.ticker}", flush=True)
                
except Exception as e:
    print(f"Error searching KXBTC15M: {e}", flush=True)
    import traceback
    traceback.print_exc()
