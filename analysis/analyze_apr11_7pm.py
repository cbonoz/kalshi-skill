#!/usr/bin/env python3
"""
Deep analysis of the active 15-minute Bitcoin market
KXBTC15M-26APR111900-00
"""

from pykalshi import KalshiClient
from dotenv import load_dotenv

load_dotenv()
client = KalshiClient()

print("🔍 Analyzing Active 15-Minute Bitcoin Market\n", flush=True)

try:
    # Get the specific market
    market = client.get_market("KXBTC15M-26APR111900-00")
    
    print(f"📊 Market Details:", flush=True)
    print(f"   Ticker: {market.ticker}", flush=True)
    print(f"   Title: {market.title}", flush=True)
    print(f"   Status: {market.status}", flush=True)
    print(f"   Closes at: {market.close_time}\n", flush=True)
    
    # Pricing analysis
    yes_bid = float(market.yes_bid_dollars) if isinstance(market.yes_bid_dollars, str) else market.yes_bid_dollars
    yes_ask = float(market.yes_ask_dollars) if isinstance(market.yes_ask_dollars, str) else market.yes_ask_dollars
    no_bid = float(market.no_bid_dollars) if isinstance(market.no_bid_dollars, str) else market.no_bid_dollars
    no_ask = float(market.no_ask_dollars) if isinstance(market.no_ask_dollars, str) else market.no_ask_dollars
    
    print(f"💰 Current Pricing:", flush=True)
    print(f"   YES Bid: ${yes_bid:.4f}", flush=True)
    print(f"   YES Ask: ${yes_ask:.4f}", flush=True)
    print(f"   Bid-Ask Spread: ${yes_ask - yes_bid:.4f} ({((yes_ask - yes_bid) / ((yes_bid + yes_ask)/2) * 100):.1f}%)", flush=True)
    
    print(f"\n   NO Bid: ${no_bid:.4f}", flush=True)
    print(f"   NO Ask: ${no_ask:.4f}", flush=True)
    print(f"   Bid-Ask Spread: ${no_ask - no_bid:.4f} ({((no_ask - no_bid) / ((no_bid + no_ask)/2) * 100):.1f}%)", flush=True)
    
    # Market interpretation
    yes_mid = (yes_bid + yes_ask) / 2
    no_mid = (no_bid + no_ask) / 2
    
    print(f"\n📈 Market Interpretation:", flush=True)
    print(f"   YES probability (midpoint): {yes_mid * 100:.1f}%", flush=True)
    print(f"   NO probability (midpoint): {no_mid * 100:.1f}%", flush=True)
    print(f"   Sum of midpoints: ${yes_mid + no_mid:.4f} (should be ~$1.00)", flush=True)
    
    # Gain/loss calculation
    print(f"\n💡 If you buy YES at ask (${yes_ask:.4f}):", flush=True)
    yes_max_gain = 1 - yes_ask
    yes_max_loss = yes_ask
    yes_breakeven = yes_ask
    print(f"   Max profit if YES: ${yes_max_gain:.4f} ({(yes_max_gain/yes_ask)*100:.1f}% ROI)", flush=True)
    print(f"   Max loss if NO: ${yes_max_loss:.4f} (100% loss)", flush=True)
    
    print(f"\n💡 If you buy NO at ask (${no_ask:.4f}):", flush=True)
    no_max_gain = 1 - no_ask
    no_max_loss = no_ask
    print(f"   Max profit if NO: ${no_max_gain:.4f} ({(no_max_gain/no_ask)*100:.1f}% ROI)", flush=True)
    print(f"   Max loss if YES: ${no_max_loss:.4f} (100% loss)", flush=True)
    
    # Expected value
    yes_ev = (yes_mid * yes_max_gain) - ((1 - yes_mid) * yes_ask)
    no_ev = (no_mid * no_max_gain) - ((1 - no_mid) * no_ask)
    
    print(f"\n📊 Expected Value Analysis:", flush=True)
    print(f"   YES Expected Value: ${yes_ev:.4f}", flush=True)
    print(f"   YES ROI: {(yes_ev/yes_ask)*100:.2f}%", flush=True)
    print(f"   NO Expected Value: ${no_ev:.4f}", flush=True)
    print(f"   NO ROI: {(no_ev/no_ask)*100:.2f}%", flush=True)
    
    if yes_ev > 0.001:
        print(f"\n   ✅ YES appears to have positive expected value!", flush=True)
    elif no_ev > 0.001:
        print(f"\n   ✅ NO appears to have positive expected value!", flush=True)
    else:
        print(f"\n   ⚠️  Both are slightly negative (market makers take a small cut)", flush=True)
    
    # Market details
    print(f"\n📋 Additional Info:", flush=True)
    print(f"   Volume: {market.volume if hasattr(market, 'volume') else 'N/A'}", flush=True)
    print(f"   Liquidity: {market.liquidity if hasattr(market, 'liquidity') else 'N/A'}", flush=True)
    
except Exception as e:
    print(f"❌ Error: {e}", flush=True)
    import traceback
    traceback.print_exc()
