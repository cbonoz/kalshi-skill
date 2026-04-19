"""
Kalshi Market Client Wrapper
Provides a clean interface for interacting with Kalshi prediction markets
"""

from pykalshi import KalshiClient, MarketStatus
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
import json

# Load environment variables from .env
load_dotenv()



class KalshiMarketClient:
    """Wrapper around pykalshi.KalshiClient with custom business logic"""

    def get_all_markets(self, limit: int = 50, fetch_all: bool = False) -> List[Dict[str, Any]]:
        """
        Get all markets, optionally limited by count or fetch all.

        Args:
            limit: Number of results to return (ignored if fetch_all=True)
            fetch_all: If True, fetch all markets (no limit)

        Returns:
            List of all markets
        """
        try:
            markets = self.client.get_markets(limit=limit, fetch_all=fetch_all)
            return [self._market_to_dict(m) for m in markets]
        except Exception as e:
            print(f"❌ Error fetching all markets: {e}")
            return []
    def __init__(self):
        """Initialize the Kalshi client"""
        self.client = KalshiClient()

    def get_bitcoin_markets(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get Bitcoin-related markets"""
        try:
            markets = self.client.get_markets(series_ticker="KXBTC", limit=limit)
            return [self._market_to_dict(m) for m in markets]
        except Exception as e:
            print(f"❌ Error fetching Bitcoin markets: {e}")
            return []

    def get_markets_by_series(self, series_ticker: str, limit: int = 50, fetch_all: bool = False) -> List[Dict[str, Any]]:
        """
        Get markets by series ticker (e.g., KXBTC, KXETC, etc.)

        Args:
            series_ticker: Series ticker code
            limit: Number of results to return (ignored if fetch_all=True)
            fetch_all: If True, fetch all markets in the series (no limit)

        Returns:
            List of matching markets
        """
        try:
            markets = self.client.get_markets(series_ticker=series_ticker, limit=limit, fetch_all=fetch_all)
            return [self._market_to_dict(m) for m in markets]
        except Exception as e:
            print(f"❌ Error fetching markets for series {series_ticker}: {e}")
            return []

    def get_market(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Fetch a specific market by ticker

        Args:
            ticker: Market ticker

        Returns:
            Market details or None if not found
        """
        try:
            market = self.client.get_market(ticker)
            return self._market_to_dict(market, include_orderbook=True, include_trades=True)
        except Exception as e:
            print(f"❌ Error fetching market {ticker}: {e}")
            return None

    # ==================== Market Data ====================

    def get_orderbook(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Get orderbook for a market"""
        try:
            market = self.client.get_market(ticker)
            orderbook = market.get_orderbook()
            return {
                "yes_bids": orderbook.yes_dollars,
                "yes_asks": orderbook.yes_sizes,
                "no_bids": orderbook.no_dollars,
                "no_asks": orderbook.no_sizes,
            }
        except Exception as e:
            print(f"❌ Error fetching orderbook for {ticker}: {e}")
            return None

    def get_recent_trades(self, ticker: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent trades for a market"""
        try:
            market = self.client.get_market(ticker)
            trades = market.get_trades(limit=limit)
            return [
                {
                    "price": trade.price,
                    "quantity": trade.count_fp,
                    "side": trade.side.name,
                    "timestamp": trade.created_time,
                }
                for trade in trades
            ]
        except Exception as e:
            print(f"❌ Error fetching trades for {ticker}: {e}")
            return []

    def get_candlesticks(self, ticker: str, start_ts: int, end_ts: int, period: str = "1H"):
        """Get candlestick data for a market"""
        try:
            from pykalshi import CandlestickPeriod

            market = self.client.get_market(ticker)
            period_map = {
                "1H": CandlestickPeriod.ONE_HOUR,
                "1D": CandlestickPeriod.ONE_DAY,
            }
            candles = market.get_candlesticks(start_ts, end_ts, period=period_map.get(period, CandlestickPeriod.ONE_HOUR))
            return [
                {
                    "open": candle.open,
                    "high": candle.high,
                    "low": candle.low,
                    "close": candle.close,
                    "timestamp": candle.start_ts,
                }
                for candle in candles
            ]
        except Exception as e:
            print(f"❌ Error fetching candlesticks for {ticker}: {e}")
            return []

    # ==================== Portfolio ====================

    def get_portfolio_balance(self) -> Optional[float]:
        """Get current portfolio balance in dollars"""
        try:
            balance = self.client.portfolio.get_balance()
            return balance.balance / 100  # Convert cents to dollars
        except Exception as e:
            print(f"❌ Error fetching balance: {e}")
            return None

    def get_positions(self) -> List[Dict[str, Any]]:
        """Get all open positions"""
        try:
            positions = self.client.portfolio.get_positions()
            return [
                {
                    "market_ticker": pos.market_ticker,
                    "quantity": pos.quantity_fp,
                    "entry_price": pos.entry_price,
                    "cost": pos.quantity_fp * pos.entry_price,
                }
                for pos in positions
            ]
        except Exception as e:
            print(f"❌ Error fetching positions: {e}")
            return []

    def get_orders(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get orders with optional status filter"""
        try:
            orders = self.client.portfolio.get_orders()
            result = []
            for order in orders:
                try:
                    result.append({
                        "order_id": order.order_id,
                        "market_ticker": getattr(order, 'market_ticker', getattr(order, 'ticker', 'N/A')),
                        "side": order.side.name if hasattr(order.side, 'name') else str(order.side),
                        "quantity": order.quantity_fp,
                        "price": order.price,
                        "status": order.status.name if hasattr(order.status, 'name') else str(order.status),
                        "created_time": order.created_time,
                    })
                except Exception as e:
                    continue
            return result
        except Exception as e:
            print(f"❌ Error fetching orders: {e}")
            return []

    # ==================== Helper Methods ====================

    def _market_to_dict(self, market, include_orderbook: bool = False, include_trades: bool = False) -> Dict[str, Any]:
        """Convert market object to dictionary"""
        # API returns prices as strings like '0.4900', need to convert to float
        yes_bid = float(market.yes_bid_dollars) if market.yes_bid_dollars else 0.0
        yes_ask = float(market.yes_ask_dollars) if market.yes_ask_dollars else 0.0
        no_bid = float(market.no_bid_dollars) if market.no_bid_dollars else 0.0
        no_ask = float(market.no_ask_dollars) if market.no_ask_dollars else 0.0
        last_price = float(market.last_price_dollars) if market.last_price_dollars else 0.0

        data = {
            "ticker": market.ticker,
            "title": market.title,
            "status": str(market.status).split('.')[-1],  # Convert enum to string
            "yes_bid": yes_bid,
            "yes_ask": yes_ask,
            "no_bid": no_bid,
            "no_ask": no_ask,
            "last_price": last_price,
            "expiration": market.expiration_time,
            "result": market.result,
        }

        if include_orderbook:
            try:
                ob = market.get_orderbook()
                data["orderbook"] = {
                    "yes_bids": [float(x) for x in ob.yes_dollars[:5]] if ob.yes_dollars else [],
                    "yes_asks": [float(x) for x in ob.yes_sizes[:5]] if ob.yes_sizes else [],
                    "no_bids": [float(x) for x in ob.no_dollars[:5]] if ob.no_dollars else [],
                    "no_asks": [float(x) for x in ob.no_sizes[:5]] if ob.no_sizes else [],
                }
            except:
                pass

        if include_trades:
            try:
                trades = market.get_trades(limit=5)
                data["recent_trades"] = [
                    {
                        "price": float(t.price),
                        "quantity": t.count_fp,
                        "side": t.side.name,
                        "time": t.created_time,
                    }
                    for t in trades
                ]
            except:
                pass

        return data
