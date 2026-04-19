#!/usr/bin/env python3
"""
Find SINGLE-SIDE mispricings in S&P 500 markets
Look for YES or NO sides that are overpriced/underpriced relative to implied probability
"""

from pykalshi import KalshiClient
from dotenv import load_dotenv

load_dotenv()
client = KalshiClient()

print("🔍 Finding SINGLE-SIDE VALUE in S&P 500 Markets (April 13 H1600)\n", flush=True)

try:
    # Get all KXINXU markets for Apr13 H1600
    markets = client.get_markets(series_ticker="KXINXU", limit=500)
    
    # Filter for April 13 at 4 PM
    apr13_4pm = [m for m in markets if m.ticker and "APR13H1600" in m.ticker]
    
    print(f"Analyzing {len(apr13_4pm)} S&P 500 strike levels for single-side value...\n", flush=True)
    
    # Parse and find value
    value_opportunities = []
    
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
        
        # If one side missing, infer from other
        if (yes_bid or yes_ask) and not (no_bid or no_ask):
            no_bid = 1 - yes_ask if yes_ask else 0.5
            no_ask = 1 - yes_bid if yes_bid else 0.5
        elif (no_bid or no_ask) and not (yes_bid or yes_ask):
            yes_bid = 1 - no_ask if no_ask else 0.5
            yes_ask = 1 - no_bid if no_bid else 0.5
        
        # Skip if not enough data
        if not ((yes_bid or yes_ask) and (no_bid or no_ask)):
            continue
        
        # Calculate implied probabilities from each side
        yes_mid = (yes_bid + yes_ask) / 2 if (yes_bid or yes_ask) else None
        no_mid = (no_bid + no_ask) / 2 if (no_bid or no_ask) else None
        
        # What should each side be worth based on the other side?
        # If NO mid = 0.30, then YES should = 0.70
        if no_mid:
            fair_yes_price = 1 - no_mid  # What YES should be
            yes_overpriced = yes_ask - fair_yes_price if yes_ask else None
            yes_underpriced = fair_yes_price - yes_bid if yes_bid else None
        else:
            fair_yes_price = None
            yes_overpriced = None
            yes_underpriced = None
        
        if yes_mid:
            fair_no_price = 1 - yes_mid  # What NO should be
            no_overpriced = no_ask - fair_no_price if no_ask else None
            no_underpriced = fair_no_price - no_bid if no_bid else None
        else:
            fair_no_price = None
            no_overpriced = None
            no_underpriced = None
        
        # Look for good deals
        # A "good deal" on YES ask = buying at a discount vs what it should be
        # A "good deal" on NO ask = buying at a discount vs what it should be
        
        if yes_ask and fair_yes_price and yes_ask < fair_yes_price - 0.01:
            # YES is CHEAP - good time to buy YES
            value_opportunities.append({
                "strike": strike,
                "side": "BUY YES",
                "price": yes_ask,
                "fair": fair_yes_price,
                "discount": fair_yes_price - yes_ask,
                "discount_pct": ((fair_yes_price - yes_ask) / fair_yes_price * 100) if fair_yes_price else 0,
                "implied_prob": yes_mid * 100 if yes_mid else None,
                "no_mid": no_mid * 100 if no_mid else None,
                "no_bid_ask": (no_bid, no_ask),
            })
        
        if no_ask and fair_no_price and no_ask < fair_no_price - 0.01:
            # NO is CHEAP - good time to buy NO
            value_opportunities.append({
                "strike": strike,
                "side": "BUY NO",
                "price": no_ask,
                "fair": fair_no_price,
                "discount": fair_no_price - no_ask,
                "discount_pct": ((fair_no_price - no_ask) / fair_no_price * 100) if fair_no_price else 0,
                "implied_prob": no_mid * 100 if no_mid else None,
                "yes_bid_ask": (yes_bid, yes_ask),
            })
        
        # Also look for YES bid overpriced (selling YES at premium)
        if yes_bid and fair_yes_price and yes_bid > fair_yes_price + 0.01:
            value_opportunities.append({
                "strike": strike,
                "side": "SELL YES",
                "price": yes_bid,
                "fair": fair_yes_price,
                "premium": yes_bid - fair_yes_price,
                "premium_pct": ((yes_bid - fair_yes_price) / fair_yes_price * 100) if fair_yes_price else 0,
                "implied_prob": yes_mid * 100 if yes_mid else None,
                "no_bid_ask": (no_bid, no_ask),
            })
        
        # Look for NO bid overpriced (selling NO at premium)
        if no_bid and fair_no_price and no_bid > fair_no_price + 0.01:
            value_opportunities.append({
                "strike": strike,
                "side": "SELL NO",
                "price": no_bid,
                "fair": fair_no_price,
                "premium": no_bid - fair_no_price,
                "premium_pct": ((no_bid - fair_no_price) / fair_no_price * 100) if fair_no_price else 0,
                "implied_prob": no_mid * 100 if no_mid else None,
                "yes_bid_ask": (yes_bid, yes_ask),
            })
    
    # Sort by discount/premium %
    value_opportunities.sort(key=lambda x: x.get('discount_pct', x.get('premium_pct', 0)), reverse=True)
    
    if value_opportunities:
        print("=" * 100, flush=True)
        print("💎 UNDERPRICED/OVERPRICED SINGLE-SIDE OPPORTUNITIES:\n", flush=True)
        
        for opp in value_opportunities[:30]:
            print(f"Strike {opp['strike']:>8,.0f}: {opp['side']:<12}", flush=True)
            
            if 'discount' in opp:
                print(f"   📌 Price: ${opp['price']:.4f} (fair: ${opp['fair']:.4f})", flush=True)
                print(f"   💰 Discount: ${opp['discount']:.4f} ({opp['discount_pct']:.2f}%)", flush=True)
            else:
                print(f"   📌 Price: ${opp['price']:.4f} (fair: ${opp['fair']:.4f})", flush=True)
                print(f"   💰 Premium: ${opp['premium']:.4f} ({opp['premium_pct']:.2f}%)", flush=True)
            
            if opp['implied_prob']:
                print(f"   ℹ️  Implied probability: {opp['implied_prob']:.1f}%", flush=True)
            print()
    else:
        print("❌ No single-side mispricings found.\n", flush=True)
        print("All YES and NO sides appear fairly priced relative to each other.", flush=True)

except Exception as e:
    print(f"❌ Error: {e}", flush=True)
    import traceback
    traceback.print_exc()
