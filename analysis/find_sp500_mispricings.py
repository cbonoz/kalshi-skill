#!/usr/bin/env python3
"""
Find mispricings/arbitrage in S&P 500 markets for April 13 at 4 PM
Check if YES and NO sides don't properly sum to $1.00
"""

from pykalshi import KalshiClient
from dotenv import load_dotenv

load_dotenv()
client = KalshiClient()

print("🔍 Hunting for S&P 500 Mispricings (April 13 H1600)\n", flush=True)

try:
    # Get all KXINXU markets for Apr13 H1600
    markets = client.get_markets(series_ticker="KXINXU", limit=500)
    
    # Filter for April 13 at 4 PM
    apr13_4pm = [m for m in markets if m.ticker and "APR13H1600" in m.ticker]
    
    print(f"Analyzing {len(apr13_4pm)} S&P 500 strike levels...\n", flush=True)
    
    # Parse and check for arbitrage
    arbitrage_opps = []
    extreme_pricing = []
    
    for m in apr13_4pm:
        # Extract strike price
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
        
        # Skip if prices are missing
        if not (yes_bid and yes_ask and no_bid and no_ask):
            # Try to infer from one side
            if yes_bid and yes_ask:
                no_bid = 1 - yes_ask
                no_ask = 1 - yes_bid
            elif no_bid and no_ask:
                yes_bid = 1 - no_ask
                yes_ask = 1 - no_bid
            else:
                continue
        
        # Check for arbitrage opportunities
        # Opportunity 1: Buy YES at bid + Buy NO at ask < $1.00 (riskless profit)
        buy_both = yes_bid + no_ask
        if buy_both < 0.99:  # -1% arbitrage threshold
            arbitrage_opps.append({
                "strike": strike,
                "type": "Buy both sides cheap",
                "yes_bid": yes_bid,
                "no_ask": no_ask,
                "total_cost": buy_both,
                "profit": 1.00 - buy_both,
                "profit_pct": ((1.00 - buy_both) / buy_both * 100) if buy_both > 0 else 0,
                "yes_bid_ask": (yes_bid, yes_ask),
                "no_bid_ask": (no_bid, no_ask)
            })
        
        # Opportunity 2: Sell YES at ask + Sell NO at bid > $1.00 (riskless profit)
        sell_both = yes_ask + no_bid
        if sell_both > 1.01:  # +1% arbitrage threshold
            arbitrage_opps.append({
                "strike": strike,
                "type": "Sell both sides dear",
                "yes_ask": yes_ask,
                "no_bid": no_bid,
                "total_revenue": sell_both,
                "profit": sell_both - 1.00,
                "profit_pct": ((sell_both - 1.00) / 1.00 * 100),
                "yes_bid_ask": (yes_bid, yes_ask),
                "no_bid_ask": (no_bid, no_ask)
            })
        
        # Check for extreme pricing imbalances
        yes_mid = (yes_bid + yes_ask) / 2 if (yes_bid or yes_ask) else 0.5
        no_mid = (no_bid + no_ask) / 2 if (no_bid or no_ask) else 0.5
        pair_sum = yes_mid + no_mid
        
        if pair_sum < 0.95 or pair_sum > 1.05:
            extreme_pricing.append({
                "strike": strike,
                "yes_mid": yes_mid,
                "no_mid": no_mid,
                "pair_sum": pair_sum,
                "imbalance": abs(pair_sum - 1.00),
                "yes_bid_ask": (yes_bid, yes_ask),
                "no_bid_ask": (no_bid, no_ask)
            })
    
    # Sort by profit
    arbitrage_opps.sort(key=lambda x: x.get('profit', 0), reverse=True)
    extreme_pricing.sort(key=lambda x: x['imbalance'], reverse=True)
    
    # Display results
    if arbitrage_opps:
        print("=" * 100, flush=True)
        print("✅ ARBITRAGE OPPORTUNITIES FOUND!\n", flush=True)
        
        for opp in arbitrage_opps[:20]:
            print(f"📍 Strike: {opp['strike']:>8,.0f}", flush=True)
            print(f"   Strategy: {opp['type']}", flush=True)
            
            if 'yes_bid' in opp:
                print(f"   • Buy YES at ${opp['yes_bid']:.4f}", flush=True)
                print(f"   • Buy NO at ${opp['no_ask']:.4f}", flush=True)
            elif 'yes_ask' in opp:
                print(f"   • Sell YES at ${opp['yes_ask']:.4f}", flush=True)
                print(f"   • Sell NO at ${opp['no_bid']:.4f}", flush=True)
            
            profit_str = f"${opp['profit']:.4f}" if 'profit' in opp else "N/A"
            print(f"   💰 Riskless profit: {profit_str} ({opp.get('profit_pct', 0):.2f}%)\n", flush=True)
    
    else:
        print("❌ No arbitrage opportunities found.\n", flush=True)
    
    if extreme_pricing and not arbitrage_opps:
        print("⚠️  Pricing Imbalances (not quite arbitrage, but suspicious):\n", flush=True)
        print(f"{'Strike':>10} {'YES':>18} {'NO':>18} {'Sum':>10} {'Imbalance':>10}", flush=True)
        print("-" * 80, flush=True)
        
        for m in extreme_pricing[:10]:
            print(f"{m['strike']:>10,.0f} {m['yes_mid']:>9.4f}-mid  {m['no_mid']:>9.4f}-mid  ${m['pair_sum']:>9.4f} {m['imbalance']:>9.2f}%", flush=True)
    
    # Summary statistics
    print("\n" + "=" * 100, flush=True)
    print("SUMMARY:", flush=True)
    print(f"   Total strikes analyzed: {len(apr13_4pm)}", flush=True)
    print(f"   Arbitrage opportunities: {len(arbitrage_opps)}", flush=True)
    print(f"   Pricing imbalances: {len(extreme_pricing)}", flush=True)
    
    if not arbitrage_opps and not extreme_pricing:
        print("\n💡 Conclusion: Market appears FAIRLY PRICED with no obvious mispricings.", flush=True)

except Exception as e:
    print(f"❌ Error: {e}", flush=True)
    import traceback
    traceback.print_exc()
