"""
Kalshi Market CLI
Command-line interface for browsing and analyzing Kalshi prediction markets
"""

from kalshi_client import KalshiMarketClient
import json


def print_header(text: str):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_markets_table(markets: list, limit: int = 10):
    """Pretty print markets in a table format"""
    for i, m in enumerate(markets[:limit], 1):
        print(f"\n{i}. {m['ticker']}: {m['title'][:50]}")
        print(f"   Status: {m['status']}")
        print(f"   YES: Bid=${m['yes_bid']:.4f} | Ask=${m['yes_ask']:.4f}")
        print(f"   NO:  Bid=${m['no_bid']:.4f} | Ask=${m['no_ask']:.4f}")
        print(f"   Expiration: {m['expiration']}")


def demo_browse_markets():
    """Demo: Browse available markets"""
    print_header("BROWSE AVAILABLE MARKETS")

    client = KalshiMarketClient()
    markets = client.get_all_markets(limit=5)

    if markets:
        print_markets_table(markets)
        print(f"\n✅ Found {len(markets)} markets")
    else:
        print("❌ No markets found")


def demo_bitcoin_markets():
    """Demo: Find Bitcoin markets"""
    print_header("BITCOIN MARKETS")

    client = KalshiMarketClient()
    markets = client.get_bitcoin_markets(limit=10)

    if markets:
        print_markets_table(markets)
        print(f"\n✅ Found {len(markets)} Bitcoin markets")
    else:
        print("❌ No Bitcoin markets found")


def demo_market_details():
    """Demo: Get detailed info for a specific market"""
    print_header("MARKET DETAILS")

    client = KalshiMarketClient()

    # First, get a market to inspect
    markets = client.get_all_markets(limit=1)
    if not markets:
        print("❌ No markets available")
        return

    ticker = markets[0]['ticker']
    print(f"📊 Fetching details for: {ticker}")

    market = client.get_market(ticker)
    if market:
        print(f"\n  Ticker: {market['ticker']}")
        print(f"  Title: {market['title']}")
        print(f"  Status: {market['status']}")
        print(f"  Last Price: ${market['last_price']:.4f}")
        print(f"  Result: {market['result'] or 'Pending'}")

        print(f"\n💹 Pricing:")
        print(f"  YES Bid: ${market['yes_bid']:.4f} | YES Ask: ${market['yes_ask']:.4f}")
        print(f"  NO Bid: ${market['no_bid']:.4f} | NO Ask: ${market['no_ask']:.4f}")

        if 'recent_trades' in market and market['recent_trades']:
            print(f"\n💱 Recent Trades:")
            for trade in market['recent_trades'][:3]:
                print(f"  {trade['side']}: ${trade['price']:.4f} | Qty: {trade['quantity']}")
    else:
        print("❌ Could not fetch market details")


def demo_portfolio():
    """Demo: Check portfolio"""
    print_header("PORTFOLIO INFO")

    client = KalshiMarketClient()

    # Get balance
    balance = client.get_portfolio_balance()
    if balance is not None:
        print(f"💰 Available Balance: ${balance:.2f}")
    else:
        print("❌ Could not fetch balance")

    # Get positions
    positions = client.get_positions()
    if positions:
        print(f"\n📊 Open Positions ({len(positions)}):")
        for pos in positions[:5]:
            print(f"  {pos['market_ticker']}: {pos['quantity']} shares @ ${pos['entry_price']:.4f}")
    else:
        print("  No open positions")

    # Get orders
    orders = client.get_orders()
    if orders:
        print(f"\n📋 Recent Orders ({len(orders)}):")
        for order in orders[:5]:
            print(f"  {order['market_ticker']}: {order['side']} {order['quantity']} @ ${order['price']:.4f}")
    else:
        print("  No open orders")


def demo_search_series():
    """Demo: Search markets by series"""
    print_header("SEARCH MARKETS BY SERIES")

    client = KalshiMarketClient()

    # Search for KXBTC
    markets = client.get_markets_by_series("KXBTC", limit=5)
    if markets:
        print(f"🔍 Found {len(markets)} KXBTC markets:")
        print_markets_table(markets)
    else:
        print("❌ No KXBTC markets found")


def main():
    """Run demo examples"""
    print("\n" + "🚀 " * 20)
    print("KALSHI MARKET CLIENT - DEMO")
    print("🚀 " * 20)

    try:
        # Run all demos
        demo_browse_markets()
        demo_bitcoin_markets()
        demo_market_details()
        demo_search_series()
        demo_portfolio()

        print_header("DEMO COMPLETE")
        print("\n✅ All examples completed successfully!")
        print("\n💡 To use in your code:")
        print("   from kalshi_client import KalshiMarketClient")
        print("   client = KalshiMarketClient()")
        print("   markets = client.get_all_markets()")

    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
