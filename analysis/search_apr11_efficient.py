#!/usr/bin/env python3
from pykalshi import KalshiClient
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()
client = KalshiClient()

print("🔍 Searching for markets around April 11, 2026\n", flush=True)

# April 11, 2026 midnight EDT (UTC-4)
april11_start_edt = datetime(2026, 4, 11, 0, 0, 0, tzinfo=timezone.utc)
april11_start_utc = april11_start_edt  # Unix timestamp for April 11 00:00 UTC
unix_april11 = int(april11_start_utc.timestamp())

# April 12 midnight UTC (end of April 11 EDT day)
april12_start_utc = datetime(2026, 4, 12, 4, 0, 0, tzinfo=timezone.utc)  # 4 AM UTC = midnight EDT
unix_april12 = int(april12_start_utc.timestamp())

print(f"Searching KXBTCD for markets expiring April 11 (EDT):", flush=True)
print(f"  Min timestamp: {unix_april11} (April 11, 2026 00:00 UTC)", flush=True)
print(f"  Max timestamp: {unix_april12} (April 12, 2026 04:00 UTC)\n", flush=True)

try:
    # Search using timestamp filter
    markets = client.get_markets(
        series_ticker="KXBTCD",
        min_close_ts=unix_april11,
        max_close_ts=unix_april12,
        limit=500
    )
    
    print(f"Found {len(markets)} markets for April 11\n", flush=True)
    
    if markets:
        # First, see what dates are in the results
        dates_found = set()
        for m in markets:
            if m.ticker:
                parts = m.ticker.split('-')
                if len(parts) >= 2:
                    dates_found.add(parts[1])
        
        print(f"Dates found in results: {sorted(dates_found)}\n", flush=True)
        
        # Look specifically for APR11
        apr11_markets = [m for m in markets if m.ticker and "APR11" in m.ticker]
        apr12_markets = [m for m in markets if m.ticker and "APR12" in m.ticker]
        
        print(f"April 11 markets: {len(apr11_markets)}", flush=True)
        print(f"April 12 markets: {len(apr12_markets)}\n", flush=True)
        
        # Look for the specific market from the URL
        target = "26APR1119"
        target_markets = [m for m in markets if m.ticker and target in m.ticker]
        
        if target_markets:
            print(f"✅ Found {len(target_markets)} markets matching {target}:\n", flush=True)
            for m in target_markets[:20]:
                if m.yes_bid_dollars and m.yes_ask_dollars:
                    yes_bid = float(m.yes_bid_dollars) if isinstance(m.yes_bid_dollars, str) else m.yes_bid_dollars
                    yes_ask = float(m.yes_ask_dollars) if isinstance(m.yes_ask_dollars, str) else m.yes_ask_dollars
                    yes_info = f"${yes_bid:.4f}-${yes_ask:.4f}"
                else:
                    yes_info = "No prices"
                print(f"  {m.ticker}: {str(m.status).split('.')[-1]:<15} {yes_info}", flush=True)
        else:
            print(f"❌ No markets found matching {target}\n", flush=True)
            print("First 30 markets:", flush=True)
            print(f"{'Ticker':<45} {'Status':<15} {'YES Bid-Ask':<20}", flush=True)
            print("-" * 80, flush=True)
            
            for m in markets[:30]:
                status = str(m.status).split('.')[-1]
                if m.yes_bid_dollars and m.yes_ask_dollars:
                    yes_bid = float(m.yes_bid_dollars) if isinstance(m.yes_bid_dollars, str) else m.yes_bid_dollars
                    yes_ask = float(m.yes_ask_dollars) if isinstance(m.yes_ask_dollars, str) else m.yes_ask_dollars
                    yes_info = f"${yes_bid:.4f}-${yes_ask:.4f}"
                else:
                    yes_info = "N/A"
                print(f"{m.ticker:<45} {status:<15} {yes_info:<20}", flush=True)
    else:
        print("No markets found. Let's try a broader search...", flush=True)
        
        # Try April 12
        print("\nSearching for April 12 markets instead...", flush=True)
        markets = client.get_markets(
            series_ticker="KXBTCD",
            min_close_ts=unix_april12,
            max_close_ts=unix_april12 + 86400,
            limit=500
        )
        
        print(f"Found {len(markets)} markets for April 12\n", flush=True)
        if markets:
            for m in markets[:10]:
                print(f"  {m.ticker}")

except Exception as e:
    print(f"❌ Error: {e}", flush=True)
    import traceback
    traceback.print_exc()
