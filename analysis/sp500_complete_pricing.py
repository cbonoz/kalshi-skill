#!/usr/bin/env python3
"""
Show complete YES vs NO pricing for S&P 500 markets
Display all available strikes with their ask prices for each side
"""

from pykalshi import KalshiClient
from dotenv import load_dotenv

load_dotenv()
client = KalshiClient()

print("📊 S&P 500 COMPLETE PRICING - April 13 H1600\n", flush=True)
print("Find underpriced ASKs on either YES or NO side\n", flush=True)

try:
    markets = client.get_markets(series_ticker="KXINXU", limit=500)
    apr13_4pm = [m for m in markets if m.ticker and "APR13H1600" in m.ticker]
    
    market_data = []
    
    for m in apr13_4pm:
        parts = m.ticker.split('-')
        strike_str = parts[-1] if len(parts) > 0 else ""
        
        try:
            strike = float(strike_str.replace('T', '').replace('B', ''))
        except:
            continue
        
        yes_bid = float(m.yes_bid_dollars) if isinstance(m.yes_bid_dollars, str) else m.yes_bid_dollars
        yes_ask = float(m.yes_ask_dollars) if isinstance(m.yes_ask_dollars, str) else m.yes_ask_dollars
        no_bid = float(m.no_bid_dollars) if isinstance(m.no_bid_dollars, str) else 0
        no_ask = float(m.no_ask_dollars) if isinstance(m.no_ask_dollars, str) else 0
        
        # Infer missing prices
        if yes_ask and not no_bid:
            no_bid = 1 - yes_ask
        if yes_bid and not no_ask:
            no_ask = 1 - yes_bid
        
        if yes_bid > 0 or yes_ask > 0:
            yes_mid = (yes_bid + yes_ask) / 2 if yes_bid > 0 else yes_ask
        else:
            yes_mid = None
        
        if no_bid > 0 or no_ask > 0:
            no_mid = (no_bid + no_ask) / 2 if no_bid > 0 else no_ask
        else:
            no_mid = None
        
        # Determine which is more expensive to buy
        yes_buy_cost = yes_ask if yes_ask > 0 else None
        no_buy_cost = no_ask if no_ask > 0 else None
        
        if yes_mid and no_mid:
            # Check if one side is notably cheaper
            cost_diff = None
            cheaper_side = None
            if yes_buy_cost and no_buy_cost:
                if yes_buy_cost < no_buy_cost:
                    cost_diff = no_buy_cost - yes_buy_cost
                    cheaper_side = "YES"
                elif no_buy_cost < yes_buy_cost:
                    cost_diff = yes_buy_cost - no_buy_cost
                    cheaper_side = "NO"
            
            market_data.append({
                "strike": strike,
                "yes_ask": yes_ask,
                "no_ask": no_ask,
                "yes_mid": yes_mid * 100,
                "no_mid": no_mid * 100,
                "cheaper_side": cheaper_side,
                "cost_diff": cost_diff,
                "yes_bid": yes_bid,
                "no_bid": no_bid,
            })
    
    # Sort by strike descending
    market_data.sort(key=lambda x: x["strike"], reverse=True)
    
    # Show the data
    print("=" * 110, flush=True)
    print(f"{'Strike':>10} {'YES Bid':>10} {'YES Ask':>10} {'Prob%':>8} {'NO Ask':>10} {'NO Bid':>10} {'Prob%':>8} {'Cheaper':>10}", flush=True)
    print("-" * 110, flush=True)
    
    best_deals = []
    
    for m in market_data:
        # Highlight extreme value
        marker = ""
        if m['cheaper_side'] and m['cost_diff'] and m['cost_diff'] > 0.02:
            marker = " ← VALUE!"
            best_deals.append((m['strike'], m['cheaper_side'], m['cost_diff'], m[f'{m["cheaper_side"].lower()}_ask']))
        
        print(f"{m['strike']:>10,.0f} ${m['yes_bid']:>9.4f} ${m['yes_ask']:>9.4f} {m['yes_mid']:>7.1f}% ${m['no_ask']:>9.4f} ${m['no_bid']:>9.4f} {m['no_mid']:>7.1f}% {m['cheaper_side']:>10}{marker}", flush=True)
    
    print("\n" + "=" * 110, flush=True)
    
    if best_deals:
        print(f"\n💡 POTENTIAL VALUE PLAYS (one side notably cheaper):\n", flush=True)
        for strike, side, savings, price in best_deals:
            print(f"   ${strike:>8,.0f}: Buy {side} at ${price:.4f} (saves ${savings:.4f} vs buying {('NO' if side == 'YES' else 'YES')})", flush=True)
    else:
        print(f"\n💭 All prices are fairly balanced - no notable single-side discounts.\n", flush=True)
        print("This doesn't mean there's no opportunity - look for strikes where your view differs from market consensus:", flush=True)
        print("  • If you think S&P will be ABOVE 6,825: Buy YES cheap (low price)")
        print("  • If you think S&P will be BELOW 6,825: Buy NO cheap (low price)", flush=True)

except Exception as e:
    print(f"❌ Error: {e}", flush=True)
    import traceback
    traceback.print_exc()
