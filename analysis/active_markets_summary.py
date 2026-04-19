#!/usr/bin/env python3
"""
Summary of ALL currently open (ACTIVE) Bitcoin prediction markets
"""

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                    ACTIVE BITCOIN MARKETS ON KALSHI                            ║
║                         (Currently Open for Trading)                           ║
╚════════════════════════════════════════════════════════════════════════════════╝

📊 MARKET #1: 15-MINUTE MICRO MARKET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ticker: KXBTC15M-26APR111900-00
Title: "BTC price up in next 15 mins?"
Expires: April 11, 2026 at 7:00 PM EDT (23:00 UTC)
Time Left: ~8 hours

Current Prices:
  ├─ YES (price goes UP):      $0.43-$0.44  (43.5% implied probability)
  ├─ NO (price stays/DOWN):    $0.56-$0.57  (56.5% implied probability)
  └─ Spread: 1.8-2.3% (TIGHT - good liquidity)

Expected Value:
  ├─ YES: -1.14% ROI (slightly unfavorable)
  └─ NO: -0.88% ROI (slightly less unfavorable)

Best Option: NO (if you believe BTC won't rally in next 15 mins)


📊 MARKET #2-7: MONTHLY BITCOIN MARKETS  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Series: KXBTCMAXMON (Monthly Trimmed Mean Bitcoin)
Expires: April 30, 2026 (7:00 PM EDT)
Time Left: ~19 days

Current Prices & Expected Value:

┌─────────────────────────────────────────────────────────────────────────┐
│ Strike        YES Bid-Ask         NO Bid-Ask         Spread    Better   │
├─────────────────────────────────────────────────────────────────────────┤
│ $75,000     $0.74-$0.76       $0.24-$0.26        2.7%      YES (-1.9%) │
│ $77,500     $0.49-$0.50       $0.50-$0.51        2.0%      YES (-1.0%) │
│ $80,000     $0.27-$0.29       $0.71-$0.73        2.8%      YES (-1.4%) │
│ $82,500     $0.16-$0.18       $0.82-$0.84        2.4%      YES (-1.2%) │
│ $85,000     $0.07-$0.08       $0.92-$0.93        1.1%      NO  (-0.5%) │
│ $87,500     $0.06-$0.07       $0.93-$0.94        1.1%      NO  (-0.5%) │
└─────────────────────────────────────────────────────────────────────────┘

Market Consensus: 
  → ~77.5% probability BTC will close ABOVE $75,000
  → ~50% probability BTC will close ABOVE $77,500 (most likely price)
  → ~7% probability BTC will close ABOVE $85,000


═════════════════════════════════════════════════════════════════════════════════

TRADING RECOMMENDATION:
━━━━━━━━━━━━━━━━━━━━━━━

If you want to place a bet TODAY with the best risk/reward:

🏆 BEST SHORT-TERM PLAY: 
   Buy NO on KXBTC15M-26APR111900-00 at $0.57
   • Expires in ~8 hours
   • Bet: Bitcoin won't significantly rally in next 15 mins
   • Expected loss: ~$0.005 per share (0.88% fee)
   • High probability win (56.5%)

🏆 BEST LONG-TERM PLAY:
   Buy YES on $77,500 KXBTCMAXMON at $0.50
   • Expires in 19 days (April 30)
   • Bet: Bitcoin closes above $77,500 by end of month
   • Expected loss: ~$0.005 per share (1.0% fee)
   • Fair odds: market is 50-50 on this strike


═════════════════════════════════════════════════════════════════════════════════

⚠️  IMPORTANT NOTES:
   • ALL currently available markets have NEGATIVE expected value
     (market makers take ~0.5-1.5% fee on both sides)
   • These are "fair" prices if you believe the market's probability estimates
   • If you have a CONTRARIAN VIEW (market is wrong), that's when you profit
   • 15-minute market expires in ~8 hours (watch it closely)
   • Monthly markets give you 19 days to be right

""", flush=True)
