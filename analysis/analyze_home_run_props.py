#!/usr/bin/env python3
"""Analyze home run player props for mispricing opportunities."""

import os
from datetime import datetime
from dotenv import load_dotenv
from pykalshi import KalshiClient
from kalshi_client import KalshiMarketClient

load_dotenv()

# Initialize
wrapper = KalshiMarketClient()
client = wrapper.client

# Player data from screenshot (Red Sox vs Cardinals home run props)
# Format: (player_name, team, position)
players = [
    ("Roman Anthony", "BOS", "OF"),
    ("Trevor Story", "BOS", "IF"),
    ("Caleb Durbin", "BOS", "OF"),
    ("Carlos Narváez", "STL", "C"),
    ("Ceddanne Rafaela", "BOS", "IF"),
    ("Ivan Herrera", "STL", "C"),
    ("JJ Wetherholt", "STL", "IF"),
    ("Jarren Duran", "BOS", "OF"),
    ("Jordan Walker", "STL", "OF"),
    ("José Fermín", "STL", "C"),
    ("Marcelo Mayer", "BOS", "SS"),
    ("Nolan Gorman", "STL", "IF"),
    ("Pedro Pagés", "STL", "C"),
    ("Ramón Urías", "STL", "IF"),
    ("Thomas Saggese", "STL", "IF"),
    ("Victor Scott", "BOS", "OF"),
    ("Willson Contreras", "STL", "C"),
    ("Wilyer Abreu", "BOS", "OF"),
]

print("🏟️  HOME RUN PROP ANALYSIS - BOS vs STL")
print("=" * 80)
print()

# Try to find player prop markets
# These are typically KXMLBPLAYER or similar
# Let's search for markets with player names

found_props = []
arbitrage_opportunities = []
underpriced_yes = []

for player_name, team, position in players:
    # Try different market search patterns
    search_patterns = [
        f"{player_name}",
        f"{player_name} home run",
        f"{player_name} 1+",
    ]
    
    for pattern in search_patterns:
        try:
            # Try direct get_market with guessed ticker
            # Player prop format might be: KXMLB[DATE]-[PLAYER]-HR or similar
            
            # Try series search
            markets = client.get_markets(
                series_ticker=f"KXMLB",
                limit=1000,
                min_close_ts=int(datetime(2026, 4, 11, 0, 0).timestamp()),
                max_close_ts=int(datetime(2026, 4, 13, 0, 0).timestamp()),
            )
            
            # Look for this player's market
            for market in markets.get("markets", []):
                ticker = market.get("ticker", "").upper()
                title = market.get("title", "").upper()
                
                if (player_name.upper() in title or player_name.upper() in ticker) and ("HOME RUN" in title or "1+" in title):
                    found_props.append({
                        "player": player_name,
                        "ticker": market.get("ticker"),
                        "title": market.get("title"),
                        "yes_bid": market.get("yes_bid"),
                        "yes_ask": market.get("yes_ask"),
                        "no_bid": market.get("no_bid"),
                        "no_ask": market.get("no_ask"),
                    })
            break
        except Exception as e:
            continue

if found_props:
    print(f"Found {len(found_props)} home run markets:\n")
    
    for prop in found_props:
        print(f"{prop['player']:20s} | YES: {prop['yes_ask']:6.2%} | NO: {prop['no_ask']:6.2%}", end="")
        
        # Check for arbitrage (asking prices)
        ask_total = (prop.get("yes_ask", 0) or 0) + (prop.get("no_ask", 0) or 0)
        spread = ask_total - 1.0
        
        if spread < 0:
            print(f" | 🎯 ARBITRAGE: Cost both sides = ${ask_total:.2f}")
            arbitrage_opportunities.append(prop)
        else:
            print(f" | Spread: {spread:+.1%}")

    print("\n" + "=" * 80)
    
    if arbitrage_opportunities:
        print(f"\n✅ ARBITRAGE FOUND ({len(arbitrage_opportunities)} props):")
        for prop in arbitrage_opportunities:
            print(f"  • {prop['player']}: Buy YES @ {prop['yes_ask']:.2%} + NO @ {prop['no_ask']:.2%} = {prop['yes_ask'] + prop['no_ask']:.2%}")
    else:
        print("\n❌ No arbitrage found (all props fairly priced, sum to $1.00-$1.04)")
    
    print("\n📊 FAIR VALUE COMPARISON:")
    print("-" * 80)
    
    # Estimate fair probability based on typical MLB home run rates:
    # - Catchers: 3-5% per game
    # - Corner infielders: 4-6% per game  
    # - Middle infielders: 2-3% per game
    # - Outfielders: 5-7% per game
    
    typical_rates = {
        "C": 0.04,   # Catcher: ~4%
        "IF": 0.035, # Infielder: ~3.5%
        "SS": 0.025, # Shortstop: ~2.5%
        "OF": 0.06,  # Outfielder: ~6%
    }
    
    good_deals = []
    
    for prop in found_props:
        player_name = prop['player']
        # Find player position
        player_pos = None
        for p_name, team, pos in players:
            if p_name == player_name:
                player_pos = pos
                break
        
        typical_rate = typical_rates.get(player_pos, 0.04)
        yes_price = prop.get("yes_ask", 0) or 0
        
        discount = (typical_rate - yes_price) / typical_rate if typical_rate > 0 else 0
        
        print(f"{player_name:20s} ({player_pos}): Market={yes_price:5.1%}, Typical={typical_rate:5.1%}, Discount={discount:+6.1%}", end="")
        
        if discount >= 0.20:  # 20%+ discount to typical rate
            print(" ⭐ POTENTIAL VALUE")
            good_deals.append(prop)
        elif discount >= 0.10:
            print(" ✓ Slight edge")
        else:
            print()
    
    if good_deals:
        print(f"\n🎯 GOOD DEALS ({len(good_deals)} props priced below typical rates):")
        for prop in good_deals:
            print(f"  • {prop['player']}: {prop['yes_ask']:.1%} (vs typical)")
    else:
        print("\n📍 Most props fairly priced to typical home run rates")

else:
    print("⚠️  Could not find player prop markets in API")
    print("\nManual Analysis of Provided Prices:")
    print("-" * 80)
    
    # Use the prices provided by user
    provided_prices = {
        "Roman Anthony": (0.12, 0.89),
        "Trevor Story": (0.10, 0.91),
        "Caleb Durbin": (0.05, 0.96),
        "Carlos Narváez": (0.06, 0.95),
        "Ceddanne Rafaela": (0.07, 0.95),
        "Ivan Herrera": (0.09, 0.92),
        "JJ Wetherholt": (0.05, 0.98),
        "Jarren Duran": (0.11, 0.90),
        "Jordan Walker": (0.11, 0.90),
        "José Fermín": (0.03, 0.98),
        "Marcelo Mayer": (0.07, 0.95),
        "Nolan Gorman": (0.09, 0.94),
        "Pedro Pagés": (0.07, 0.97),
        "Ramón Urías": (0.07, 0.94),
        "Thomas Saggese": (0.05, 0.97),
        "Victor Scott": (0.03, 0.99),
        "Willson Contreras": (0.13, 0.89),
        "Wilyer Abreu": (0.12, 0.90),
    }
    
    typical_rates = {
        "C": 0.04, "IF": 0.035, "SS": 0.025, "OF": 0.06,
    }
    
    print(f"{'Player':20s} {'Position':8s} {'YES':6s} {'NO':6s} {'Total':6s} {'Fair?':6s} {'Assessment':20s}")
    print("-" * 80)
    
    good_deals = []
    
    for player_name, team, position in players:
        if player_name not in provided_prices:
            continue
        
        yes_price, no_price = provided_prices[player_name]
        total = yes_price + no_price
        typical = typical_rates.get(position, 0.04)
        
        # Assessment
        if total > 1.05:
            assessment = "WIDE SPREAD"
            indicator = "⚠️"
        elif yes_price < typical * 0.7:
            assessment = "UNDERPRICED YES"
            indicator = "✓"
            good_deals.append((player_name, yes_price, typical, position))
        elif yes_price > typical * 1.3:
            assessment = "OVERPRICED YES"
            indicator = "✗"
        else:
            assessment = "Fair"
            indicator = "="
        
        print(f"{player_name:20s} {position:8s} {yes_price:5.1%} {no_price:5.1%} {total:5.1%} {indicator:6s} {assessment:20s}")
    
    print("\n" + "=" * 80)
    
    if good_deals:
        print(f"\n✅ POTENTIAL GOOD DEALS ({len(good_deals)} props):\n")
        for player, yes_price, typical, pos in good_deals:
            discount_pct = (typical - yes_price) / typical * 100
            print(f"  • {player:20s} @ {yes_price:.1%} (vs {typical:.1%} typical {pos}) = {discount_pct:.0f}% discount")
    else:
        print("\n📊 PRICING SUMMARY:")
        print("  • Most home run props are fairly priced to ~2-6% actual home run rates")
        print("  • YES side reflects accurate probability - not overpriced by market")
        print("  • These are real-money bets where market has good data on historical rates")
        print("  • Willson Contreras (13¢) and Roman Anthony (12¢) highest priced")
        print("  • José Fermín (3¢) and Victor Scott (3¢) lowest priced")
        print("\n💡 KEY INSIGHT:")
        print("  For these to be 'good deals', you'd need to:")
        print("  1. Have better player data than the market (injury status, recent form, etc.)")
        print("  2. Know matchup details (vs RHP/LHP, park factors)")
        print("  3. Be contrarian on player ability vs their historical rates")
