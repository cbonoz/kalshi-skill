import argparse
from kalshi_client import KalshiMarketClient


def main():
    parser = argparse.ArgumentParser(description="Kalshi Skill CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Balance
    subparsers.add_parser("balance", help="Show portfolio balance")

    # Positions
    subparsers.add_parser("positions", help="Show open positions")

    # Orders
    subparsers.add_parser("orders", help="Show open orders")

    # Get market
    market_parser = subparsers.add_parser("market", help="Show details for a market")
    market_parser.add_argument("ticker", help="Market ticker")

    # Get all markets
    all_parser = subparsers.add_parser("markets", help="List all markets")
    all_parser.add_argument("--limit", type=int, default=10, help="Number of markets to show")

    args = parser.parse_args()
    client = KalshiMarketClient()

    if args.command == "balance":
        bal = client.get_portfolio_balance()
        print(bal)
    elif args.command == "positions":
        import pprint
        pprint.pprint(client.get_positions())
    elif args.command == "orders":
        import pprint
        pprint.pprint(client.get_orders())
    elif args.command == "market":
        import pprint
        pprint.pprint(client.get_market(args.ticker))
    elif args.command == "markets":
        import pprint
        pprint.pprint(client.get_all_markets(limit=args.limit))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
