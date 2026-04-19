#!/usr/bin/env python3
"""
Analyze Bitcoin hourly prediction markets - focusing on opportunities
"""

from pykalshi import KalshiClient
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import re

def parse_hourly_ticker(ticker):
    """Extract date/time/strike from hourly market ticker
    Format: KXBTC-26APR1300-T81799.99 where:
    - 26 = year (2026)
    - APR = month
    - 13 = day
    - 00 = hour offset from midnight
    """
    parts = ticker.split('-')
    if len(parts) >= 3:
        date_time = parts[1]  # e.g., "26APR1300"
        strike_type = parts[2]  # e.g., "T81799.99" or "B81750"
        
        if len(date_time) >= 8:  # YYMMMDDHH
            try:
                # Format: YYMMsDDHH, e.g., 26APR1300
                dt = datetime.strptime(date_time, "%y%b%d%H")
                
                # Extract strike price from strike_type
                strike_str = strike_type[1:] if len(strike_type) > 1 else "0"
                # Remove decimals if present
                if '.' in strike_str:
                    strike_price = float(strike_str)
                else:
                    strike_price = int(strike_str) / 100  # Convert cents to dollars
                
                return {
                    "date_time": date_time,
                    "datetime_obj": dt,
                    "strike_type": strike_type,
                    "strike_price": strike_price,
                    "strike_type_letter": strike_type[0]
                }
            except Exception as e:
                pass
    return None

def main():
    load_dotenv()
    client = KalshiClient()

    print("🔍 Bitcoin Hourly Markets Analysis\n", flush=True)
    
    try:
        # Fetch hourly markets (they're part of KXBTC series)
        markets = client.get_markets(series_ticker="KXBTC", limit=1000)
        print(f"Fetched {len(markets)} markets from KXBTC series\n", flush=True)
        
        # Separate hourly from daily - hourly has timestamp with hours/mins
        # Format: KXBTC-26APR1300-... (hourly) vs KXBTC-26APR-... (daily)
        hourly_markets = []
        for m in markets:
            if m.ticker:
                parts = m.ticker.split('-')
                if len(parts) >= 2:
                    date_part = parts[1]
                    # Hourly format has 8+ chars (DDMMMHHMM), daily only has 5-6 (DDMMM)
                    if len(date_part) >= 8:
                        hourly_markets.append(m)
        
        print(f"Found {len(hourly_markets)} hourly markets\n", flush=True)
        
        # Filter by status and pricing
        active_hourly = [m for m in hourly_markets if "ACTIVE" in str(m.status) and m.yes_bid_dollars and m.yes_ask_dollars]
        print(f"Active hourly markets with prices: {len(active_hourly)}\n", flush=True)
        
        if not active_hourly:
            print("No active hourly markets found. Checking other statuses...", flush=True)
            for status in ["INITIALIZED", "FROZEN"]:
                count = len([m for m in hourly_markets if status in str(m.status)])
                print(f"  {status}: {count}", flush=True)
            
            # Show all hourly market details
            print(f"\nAll Hourly Markets ({len(hourly_markets)} total):\n", flush=True)
            
            # Group by date-hour
            by_hour = {}
            for m in hourly_markets[:100]:  # First 100
                info = parse_hourly_ticker(m.ticker)
                if info:
                    hour_key = info["date_time"]
                    if hour_key not in by_hour:
                        by_hour[hour_key] = []
                    by_hour[hour_key].append({
                        "ticker": m.ticker,
                        "status": str(m.status),
                        "type": info["strike_type"],
                        "strike": info["strike_price"],
                        "yes_bid": m.yes_bid_dollars,
                        "yes_ask": m.yes_ask_dollars,
                    })
            
            print(f"Found {len(by_hour)} distinct hour-expiration times:\n", flush=True)
            for hour_key in sorted(by_hour.keys()):
                markets_at_hour = by_hour[hour_key]
                print(f"\n⏰ {hour_key} ({len(markets_at_hour)} markets):", flush=True)
                
                # Show variety of strikes/types
                strike_types = set()
                for m_info in markets_at_hour:
                    strike_types.add(f"{m_info['type'][0]}${m_info['strike']:,.0f}")
                
                print(f"   Strike types: {', '.join(sorted(strike_types)[:10])}", flush=True)
                
                # Show best priced one
                with_prices = [m_info for m_info in markets_at_hour if m_info['yes_bid']]
                if with_prices:
                    best = with_prices[0]
                    print(f"   Sample: {best['ticker']}, Status: {best['status']}", flush=True)
                    if best['yes_bid'] and best['yes_ask']:
                        yes_bid = float(best['yes_bid']) if isinstance(best['yes_bid'], str) else best['yes_bid']
                        yes_ask = float(best['yes_ask']) if isinstance(best['yes_ask'], str) else best['yes_ask']
                        print(f"           YES: ${yes_bid:.4f} - ${yes_ask:.4f}", flush=True)
        
        else:
            # Analyze active hourly markets
            print("📊 Active Hourly Markets Analysis:\n", flush=True)
            
            # Group by hour
            by_hour = {}
            for m in active_hourly:
                info = parse_hourly_ticker(m.ticker)
                if info:
                    hour_key = info["date_time"]
                    if hour_key not in by_hour:
                        by_hour[hour_key] = []
                    
                    yes_bid = float(m.yes_bid_dollars)
                    yes_ask = float(m.yes_ask_dollars)
                    spread = yes_ask - yes_bid
                    spread_pct = (spread / ((yes_bid + yes_ask) / 2) * 100) if (yes_bid + yes_ask) > 0 else 0
                    
                    by_hour[hour_key].append({
                        "ticker": m.ticker,
                        "status": str(m.status),
                        "strike": info["strike_price"],
                        "strike_type": info["strike_type_letter"],
                        "yes_bid": yes_bid,
                        "yes_ask": yes_ask,
                        "spread": spread,
                        "spread_pct": spread_pct,
                    })
            
            print(f"Active hours: {sorted(by_hour.keys())}\n", flush=True)
            
            for hour_key in sorted(by_hour.keys()):
                markets_at_hour = by_hour[hour_key]
                markets_at_hour.sort(key=lambda x: x["spread_pct"])
                
                print(f"\n⏰ {hour_key} - {len(markets_at_hour)} active markets:", flush=True)
                print(f"{'Ticker':<45} {'Spread':>12} {'YES Bid':>10} {'YES Ask':>10}", flush=True)
                print("-" * 80, flush=True)
                
                for m_info in markets_at_hour[:10]:
                    print(f"{m_info['ticker']:<45} {m_info['spread_pct']:>10.1f}% ${m_info['yes_bid']:>9.4f} ${m_info['yes_ask']:>9.4f}", flush=True)
    
    except Exception as e:
        print(f"❌ Error: {e}", flush=True)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
