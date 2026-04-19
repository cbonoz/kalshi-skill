#!/usr/bin/env python3
"""
Detailed analysis of Boston vs St. Louis game market
"""

from pykalshi import KalshiClient
from dotenv import load_dotenv

load_dotenv()
client = KalshiClient()

print("⚾ Boston Red Sox vs St. Louis Cardinals - April 11, 7:15 PM\n", flush=True)

try:
    # Get both markets
    bos_market = client.get_market("KXMLBGAME-26APR111915BOSSTL-BOS")
    stl_market = client.get_market("KXMLBGAME-26APR111915BOSSTL-STL")
    
    # Boston pricing
    bos_bid = float(bos_market.yes_bid_dollars) if isinstance(bos_market.yes_bid_dollars, str) else bos_market.yes_bid_dollars
    bos_ask = float(bos_market.yes_ask_dollars) if isinstance(bos_market.yes_ask_dollars, str) else bos_market.yes_ask_dollars
    bos_mid = (bos_bid + bos_ask) / 2
    
    # St. Louis pricing
    stl_bid = float(stl_market.yes_bid_dollars) if isinstance(stl_market.yes_bid_dollars, str) else stl_market.yes_bid_dollars
    stl_ask = float(stl_market.yes_ask_dollars) if isinstance(stl_market.yes_ask_dollars, str) else stl_market.yes_ask_dollars
    stl_mid = (stl_bid + stl_ask) / 2
    
    print("=" * 80, flush=True)
    print("GAME PRICING:", flush=True)
    print("=" * 80, flush=True)
    print(f"\n🔴 BOSTON RED SOX:", flush=True)
    print(f"   Bid: ${bos_bid:.4f}", flush=True)
    print(f"   Ask: ${bos_ask:.4f}", flush=True)
    print(f"   Mid: ${bos_mid:.4f}", flush=True)
    print(f"   Probability: {bos_mid * 100:.1f}%", flush=True)
    print(f"   Spread: ${bos_ask - bos_bid:.4f} ({((bos_ask - bos_bid) / bos_mid * 100):.1f}%)", flush=True)
    
    print(f"\n⚪ ST. LOUIS CARDINALS:", flush=True)
    print(f"   Bid: ${stl_bid:.4f}", flush=True)
    print(f"   Ask: ${stl_ask:.4f}", flush=True)
    print(f"   Mid: ${stl_mid:.4f}", flush=True)
    print(f"   Probability: {stl_mid * 100:.1f}%", flush=True)
    print(f"   Spread: ${stl_ask - stl_bid:.4f} ({((stl_ask - stl_bid) / stl_mid * 100):.1f}%)", flush=True)
    
    # Check for arbitrage
    pair_sum_mid = bos_mid + stl_mid
    pair_sum_bid = bos_bid + stl_bid
    pair_sum_ask = bos_ask + stl_ask
    
    print(f"\n" + "=" * 80, flush=True)
    print("ARBITRAGE CHECK:", flush=True)
    print("=" * 80, flush=True)
    print(f"\nBid prices sum: ${pair_sum_bid:.4f} (should be ~$1.00)", flush=True)
    print(f"Mid prices sum: ${pair_sum_mid:.4f}", flush=True)
    print(f"Ask prices sum: ${pair_sum_ask:.4f}", flush=True)
    
    if pair_sum_ask < 0.99:
        print(f"\n✅ ARBITRAGE OPPORTUNITY FOUND!", flush=True)
        print(f"   Buy BOS at ${bos_ask:.4f}", flush=True)
        print(f"   Buy STL at ${stl_ask:.4f}", flush=True)
        print(f"   Total cost: ${pair_sum_ask:.4f}", flush=True)
        print(f"   Riskless profit: ${1.00 - pair_sum_ask:.4f} ({((1.00 - pair_sum_ask)/pair_sum_ask)*100:.2f}%)", flush=True)
    elif pair_sum_bid > 1.01:
        print(f"\n✅ REVERSE ARBITRAGE FOUND!", flush=True)
        print(f"   Sell BOS at ${bos_bid:.4f}", flush=True)
        print(f"   Sell STL at ${stl_bid:.4f}", flush=True)
        print(f"   Total revenue: ${pair_sum_bid:.4f}", flush=True)
        print(f"   Riskless profit: ${pair_sum_bid - 1.00:.4f}", flush=True)
    else:
        print(f"\n❌ No arbitrage found.", flush=True)
        
        if pair_sum_ask > 1.00:
            print(f"   Market is slightly overpriced at asks")
            print(f"   Overpricing: {((pair_sum_ask - 1.00) / 1.00 * 100):.2f}%", flush=True)
        elif pair_sum_bid < 1.00:
            print(f"   Market is slightly underpriced at bids")
            print(f"   Underpricing: {((1.00 - pair_sum_bid) / 1.00 * 100):.2f}%", flush=True)
        else:
            print(f"   ✅ Prices are perfectly balanced", flush=True)
    
    # Compare which team is favored
    print(f"\n" + "=" * 80, flush=True)
    print("ODDS INTERPRETATION:", flush=True)
    print("=" * 80, flush=True)
    
    if bos_mid > stl_mid:
        advantage = (bos_mid - stl_mid) * 100
        print(f"\nBoston is favored by {advantage:.1f} percentage points", flush=True)
        print(f"Boston is ~{(bos_mid/stl_mid):.2f}x more likely to win", flush=True)
    else:
        advantage = (stl_mid - bos_mid) * 100
        print(f"\nSt. Louis is favored by {advantage:.1f} percentage points", flush=True)
        print(f"St. Louis is ~{(stl_mid/bos_mid):.2f}x more likely to win", flush=True)
    
    print(f"\nBoston win probability: {bos_mid * 100:.1f}%", flush=True)
    print(f"St. Louis win probability: {stl_mid * 100:.1f}%", flush=True)
    print(f"Total probability: {pair_sum_mid * 100:.1f}%", flush=True)

except Exception as e:
    print(f"❌ Error: {e}", flush=True)
    import traceback
    traceback.print_exc()
