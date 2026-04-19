#!/usr/bin/env python3
"""
Detailed KXBTCMAXMON market analysis for trading opportunities
"""

from pykalshi import KalshiClient
from dotenv import load_dotenv

def main():
    load_dotenv()
    client = KalshiClient()

    print("🔍 Deep Analysis: KXBTCMAXMON Markets (April 30, 2026)\n", flush=True)
    
    try:
        # Fetch KXBTCMAXMON markets
        markets = client.get_markets(series_ticker="KXBTCMAXMON", limit=100)
        
        # Filter for April 30 active markets
        april30_active = [m for m in markets if "26APR30" in m.ticker and "ACTIVE" in str(m.status)]
        
        print(f"Found {len(april30_active)} ACTIVE markets for April 30, 2026\n", flush=True)
        
        # Analyze each market
        opportunities = []
        
        for market in april30_active:
            yes_bid = float(market.yes_bid_dollars) if market.yes_bid_dollars else 0.0
            yes_ask = float(market.yes_ask_dollars) if market.yes_ask_dollars else 0.0
            no_bid = float(market.no_bid_dollars) if market.no_bid_dollars else 0.0
            no_ask = float(market.no_ask_dollars) if market.no_ask_dollars else 0.0
            
            if yes_bid == 0 and yes_ask == 0:
                continue
            
            # Extract strike price from ticker
            parts = market.ticker.split("-")
            strike = int(parts[-1]) / 100 if len(parts) > 0 else 0
            
            # Calculate spreads
            yes_spread = yes_ask - yes_bid
            no_spread = no_ask - no_bid
            
            # Mid prices
            yes_mid = (yes_bid + yes_ask) / 2
            no_mid = (no_bid + no_ask) / 2
            
            # Check for arbitrage (prices don't sum to 1.0)
            pair_total = yes_mid + no_mid
            
            # Implied win probability
            implied_yes_prob = yes_mid * 100
            
            opportunities.append({
                "strike": strike,
                "yes_bid": yes_bid,
                "yes_ask": yes_ask,
                "no_bid": no_bid,
                "no_ask": no_ask,
                "yes_mid": yes_mid,
                "no_mid": no_mid,
                "yes_spread": yes_spread,
                "no_spread": no_spread,
                "pair_total": pair_total,
                "implied_prob": implied_yes_prob,
                "ticker": market.ticker,
                "title": market.title,
            })
        
        # Sort by strike
        opportunities.sort(key=lambda x: x["strike"])
        
        # Print opportunity analysis
        print("=" * 100, flush=True)
        print("SPREAD ANALYSIS (Bid-Ask Efficiency):", flush=True)
        print("=" * 100, flush=True)
        print(f"{'Strike':>12} {'YES Bid':>10} {'YES Ask':>10} {'Spread':>8} {'NO Bid':>10} {'NO Ask':>10} {'Spread':>8}\n", flush=True)
        
        wide_spreads = []
        for opp in opportunities:
            yes_spread_pct = (opp["yes_spread"] / opp["yes_mid"] * 100) if opp["yes_mid"] > 0 else 0
            no_spread_pct = (opp["no_spread"] / opp["no_mid"] * 100) if opp["no_mid"] > 0 else 0
            
            print(f"${opp['strike']:>10,.0f} ${opp['yes_bid']:>9.4f} ${opp['yes_ask']:>9.4f} {yes_spread_pct:>6.1f}% ${opp['no_bid']:>9.4f} ${opp['no_ask']:>9.4f} {no_spread_pct:>6.1f}%", flush=True)
            
            if yes_spread_pct > 5 or no_spread_pct > 5:
                wide_spreads.append(opp)
        
        print(f"\n📊 Wide Spreads (>5%): {len(wide_spreads)} markets\n", flush=True)
        
        # Print probability curve
        print("=" * 100, flush=True)
        print("PROBABILITY CURVE (Market's BTC Price Estimate):", flush=True)
        print("=" * 100, flush=True)
        print(f"{'Strike':>12} {'Implied Prob YES':>18} {'Confidence':>12}\n", flush=True)
        
        for opp in opportunities:
            prob_pct = opp["implied_prob"]
            bars = int(prob_pct / 5)
            bar_visual = "█" * bars + "░" * (20 - bars)
            print(f"${opp['strike']:>10,.0f} {prob_pct:>15.1f}% {bar_visual}", flush=True)
        
        # Find the most likely strike (closest to 50%)
        median_market = min(opportunities, key=lambda x: abs(x["implied_prob"] - 50))
        
        print(f"\n💡 Market Consensus:", flush=True)
        print(f"   Most likely BTC price on April 30: ${median_market['strike']:,.0f}", flush=True)
        print(f"   Confidence level: {median_market['implied_prob']:.1f}%\n", flush=True)
        
        # Arbitrage opportunities
        print("=" * 100, flush=True)
        print("ARBITRAGE OPPORTUNITIES (Pair Sum ≠ $1.00):", flush=True)
        print("=" * 100, flush=True)
        
        arb_opps = [o for o in opportunities if abs(o["pair_total"] - 1.0) > 0.01]
        
        if arb_opps:
            print(f"{'Strike':>12} {'YES Mid':>10} {'NO Mid':>10} {'Total':>10} {'Arb $':>10}\n", flush=True)
            for opp in arb_opps:
                arb_profit = abs(1.0 - opp["pair_total"])
                print(f"${opp['strike']:>10,.0f} ${opp['yes_mid']:>9.4f} ${opp['no_mid']:>9.4f} ${opp['pair_total']:>9.4f} ${arb_profit:>9.4f}", flush=True)
        else:
            print("No significant arbitrage opportunities found (all pairs sum to ~$1.00)\n", flush=True)
        
        # Trading recommendations
        print("=" * 100, flush=True)
        print("BEST VALUE OPPORTUNITIES (Highest Expected Return):", flush=True)
        print("=" * 100, flush=True)
        
        opportunities_scored = []
        for opp in opportunities:
            yes_prob = opp["implied_prob"] / 100
            no_prob = 1 - yes_prob
            
            # Calculate expected value for betting each side
            # EV = (probability of winning * gain) - (probability of losing * loss)
            yes_ev = (yes_prob * (1 - opp["yes_ask"])) - ((1 - yes_prob) * opp["yes_ask"])
            no_ev = (no_prob * (1 - opp["no_ask"])) - ((1 - no_prob) * opp["no_ask"])
            
            # Return on investment (%)
            yes_roi = yes_ev / opp["yes_ask"] * 100 if opp["yes_ask"] > 0 else 0
            no_roi = no_ev / opp["no_ask"] * 100 if opp["no_ask"] > 0 else 0
            
            better_side = "YES" if yes_ev >= no_ev else "NO"
            better_ev = max(yes_ev, no_ev)
            better_roi = max(yes_roi, no_roi)
            better_price = opp["yes_ask"] if better_side == "YES" else opp["no_ask"]
            
            opportunities_scored.append({
                **opp,
                "yes_ev": yes_ev,
                "no_ev": no_ev,
                "yes_roi": yes_roi,
                "no_roi": no_roi,
                "better_side": better_side,
                "better_ev": better_ev,
                "better_roi": better_roi,
                "better_price": better_price,
            })
        
        # Sort by absolute expected value
        opportunities_scored.sort(key=lambda x: abs(x["better_ev"]), reverse=True)
        
        print(f"{'Strike':>12} {'Better':>8} {'Price':>8} {'Expected Value':>15} {'ROI':>10}\n", flush=True)
        for opp in opportunities_scored[:5]:
            print(f"${opp['strike']:>10,.0f} {opp['better_side']:>8} ${opp['better_price']:>7.4f} ${opp['better_ev']:>14.4f} {opp['better_roi']:>9.1f}%", flush=True)
        
        print(f"\n" + "=" * 100, flush=True)
        print("DETAILED OPPORTUNITY BREAKDOWN:", flush=True)
        print("=" * 100, flush=True)
        
        for opp in opportunities_scored:
            print(f"\n💰 ${opp['strike']:,.0f} Strike:", flush=True)
            print(f"   YES Side (Probability {opp['implied_prob']:.1f}%):")
            print(f"      • Can buy YES at: ${opp['yes_bid']:.4f} - ${opp['yes_ask']:.4f}")
            print(f"      • Expected Value: ${opp['yes_ev']:+.4f}")
            print(f"      • ROI: {opp['yes_roi']:+.1f}%")
            print(f"   NO Side (Probability {100-opp['implied_prob']:.1f}%):")
            print(f"      • Can buy NO at: ${opp['no_bid']:.4f} - ${opp['no_ask']:.4f}")
            print(f"      • Expected Value: ${opp['no_ev']:+.4f}")
            print(f"      • ROI: {opp['no_roi']:+.1f}%")
            print(f"   ➜ BETTER BET: {opp['better_side']} (EV: ${opp['better_ev']:+.4f})", flush=True)
        
    except Exception as e:
        print(f"❌ Error: {e}", flush=True)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
