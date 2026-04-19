#!/usr/bin/env python3
"""
Find specific market from URL: kxbtcd-26apr1119
"""

from pykalshi import KalshiClient
from dotenv import load_dotenv

def main():
    load_dotenv()
    client = KalshiClient()

    target_ticker = "kxbtcd-26apr1119"
    print(f"🔍 Looking for market: {target_ticker}\n", flush=True)
    
    # Try direct lookup
    try:
        market = client.get_market(target_ticker)
        print(f"✅ Found market: {target_ticker}", flush=True)
        print(f"   Title: {market.title}", flush=True)
        print(f"   Status: {market.status}", flush=True)
        print(f"   YES Bid: ${market.yes_bid_dollars}", flush=True)
        print(f"   YES Ask: ${market.yes_ask_dollars}", flush=True)
        print(f"   NO Bid: ${market.no_bid_dollars}", flush=True)
        print(f"   NO Ask: ${market.no_ask_dollars}", flush=True)
        print(f"   Closes: {market.close_time}", flush=True)
    except Exception as e:
        print(f"❌ Direct lookup failed: {e}\n", flush=True)
        
        # Try searching KXBTCD series for April 11 at 7 PM (19:00)
        print("Trying to find via series search...", flush=True)
        
        try:
            markets = client.get_markets(series_ticker="KXBTCD", limit=500)
            print(f"Fetched {len(markets)} KXBTCD markets\n", flush=True)
            
            # Look for April 11 markets
            april11_markets = [m for m in markets if m.ticker and "APR11" in m.ticker.upper()]
            print(f"Found {len(april11_markets)} markets for April 11\n", flush=True)
            
            if april11_markets:
                print("April 11 Markets:", flush=True)
                for m in april11_markets[:20]:
                    print(f"  {m.ticker}: Status={m.status}, YES: ${m.yes_bid_dollars}-${m.yes_ask_dollars}", flush=True)
        except Exception as e2:
            print(f"Series search failed: {e2}", flush=True)

if __name__ == "__main__":
    main()
