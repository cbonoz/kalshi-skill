#!/usr/bin/env python3
"""
Find and analyze Bitcoin hourly prediction markets on Kalshi
"""

from pykalshi import KalshiClient
from dotenv import load_dotenv
import json
from datetime import datetime, timezone

def main():
    load_dotenv()
    client = KalshiClient()

    print("🔍 Searching for Bitcoin Hourly Markets\n", flush=True)
    
    try:
        # Try to find hourly Bitcoin markets
        # Hourly markets likely have 'HOURLY', 'HR', 'H' in ticker or different naming
        
        print("Discovering market series...", flush=True)
        
        # First, let's try some common patterns for hourly Bitcoin
        hourly_patterns = [
            "KXBTC",  # General Bitcoin
            "KXBTCH",  # Bitcoin hourly?
            "KXBTCHR",  # Bitcoin hourly repeated?
        ]
        
        all_hourly_markets = []
        
        for pattern in hourly_patterns:
            try:
                print(f"\n  Searching for series: {pattern}...", flush=True)
                markets = client.get_markets(series_ticker=pattern, limit=500)
                
                if markets:
                    print(f"  Found {len(markets)} markets with {pattern}", flush=True)
                    
                    # Filter for hourly markets (look at expiration times)
                    hourly = [m for m in markets if m and hasattr(m, 'ticker')]
                    
                    # Show first few to understand structure
                    if hourly:
                        print(f"    Sample tickers:", flush=True)
                        for m in hourly[:5]:
                            print(f"      {m.ticker}", flush=True)
                        
                        all_hourly_markets.extend(hourly)
            except Exception as e:
                print(f"  {pattern}: {e}", flush=True)
        
        # If we didn't find any, try fetching with larger limit to explore
        if not all_hourly_markets:
            print("\nNo hourly markets found with common patterns.", flush=True)
            print("Trying broader search...", flush=True)
            
            try:
                # Get all Bitcoin markets to explore their structure
                markets = client.get_markets(series_ticker="KXBTC", limit=1000)
                print(f"Found {len(markets)} markets with KXBTC series", flush=True)
                
                if markets:
                    print("\nSample market tickers found:", flush=True)
                    for m in markets[:20]:
                        if m.yes_bid_dollars and m.yes_ask_dollars:
                            print(f"  {m.ticker} | Expires: {m.close_time} | YES: ${m.yes_bid_dollars:.4f}-${m.yes_ask_dollars:.4f}", flush=True)
                    
                    # Count by expiration pattern
                    expiration_types = {}
                    for m in markets:
                        if m.close_time:
                            # Extract hour/day pattern
                            close_dt = datetime.fromisoformat(m.close_time.replace('Z', '+00:00'))
                            # Determine if hourly or daily
                            ticker_parts = m.ticker.split('-')
                            date_part = ticker_parts[-1] if len(ticker_parts) > 0 else ""
                            
                            if len(date_part) == 8:  # YYYYMMDD format = daily
                                exp_type = "DAILY"
                            elif len(date_part) == 10:  # YYYYMMDDHH format = hourly
                                exp_type = "HOURLY"
                            else:
                                exp_type = f"OTHER({len(date_part)})"
                            
                            expiration_types[exp_type] = expiration_types.get(exp_type, 0) + 1
                    
                    print(f"\nMarket types found:", flush=True)
                    for exp_type, count in sorted(expiration_types.items(), key=lambda x: x[1], reverse=True):
                        print(f"  {exp_type}: {count} markets", flush=True)
                    
                    # Extract hourly markets if they exist
                    hourly_markets = []
                    for m in markets:
                        if m.ticker and len(m.ticker.split('-')[-1]) == 10:  # Likely hourly format
                            hourly_markets.append(m)
                    
                    if hourly_markets:
                        print(f"\n✅ Found {len(hourly_markets)} potential hourly markets!", flush=True)
                        
                        # Filter for ACTIVE with spreads
                        active_hourly = [m for m in hourly_markets if "ACTIVE" in str(m.status) and m.yes_bid_dollars and m.yes_ask_dollars]
                        print(f"   {len(active_hourly)} are ACTIVE with prices", flush=True)
                        
                        if active_hourly:
                            # Sort by spread
                            active_hourly.sort(key=lambda m: (float(m.yes_ask_dollars) - float(m.yes_bid_dollars)) if m.yes_ask_dollars and m.yes_bid_dollars else 999)
                            
                            print(f"\n📊 Top Hourly Markets (Tightest Spreads):\n", flush=True)
                            print(f"{'Ticker':<35} {'YES Bid':>10} {'YES Ask':>10} {'Spread':>10} {'Status':>12}", flush=True)
                            print("-" * 80, flush=True)
                            
                            for m in active_hourly[:20]:
                                yes_bid = float(m.yes_bid_dollars)
                                yes_ask = float(m.yes_ask_dollars)
                                spread = yes_ask - yes_bid
                                spread_pct = (spread / ((yes_bid + yes_ask) / 2) * 100) if (yes_bid + yes_ask) > 0 else 0
                                print(f"{m.ticker:<35} ${yes_bid:>9.4f} ${yes_ask:>9.4f} {spread_pct:>9.1f}% {str(m.status):>12}", flush=True)
                    else:
                        print("\nNo hourly markets detected in KXBTC series", flush=True)
                        print("Need to explore different series or fetch strategies", flush=True)
            
            except Exception as e:
                print(f"Error in broader search: {e}", flush=True)
                import traceback
                traceback.print_exc()
        
    except Exception as e:
        print(f"❌ Error: {e}", flush=True)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
