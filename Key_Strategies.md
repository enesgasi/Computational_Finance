# Trading Strategy Summary

| Strategy | Goal / Aim | Performs Well | Performs Poorly | Key Parameters |
|----------|------------|---------------|----------------|----------------|
| **Arbitrage (2-asset pairs)** | Exploit **temporary mispricing** between two equivalent assets (e.g., BTC/WBTC) to earn risk-free profit | Liquid, fast markets with small price deviations | Illiquid markets, slow execution, high slippage | - Price ratio thresholds (entry/exit)<br>- Transaction fees (t_f)<br>- Capital allocation |
| **Rebalancing (Portfolio / Multi-asset)** | Maintain **balanced portfolio** and **capture volatility** by systematically selling winners and buying losers | Volatile but sideways markets, with mean-reverting price behavior | Strong trending markets (one-directional bull/bear), high transaction costs | - Number of assets<br>- Band / deviation threshold (margin)<br>- Transaction fees (t_f)<br>- Target allocation (equal-weight or custom) |
| **Mean Reversion (Single asset / Spread)** | Profit from **prices reverting to mean** after extreme deviations | Sideways or range-bound markets, assets with stable historical mean | Strong trending markets, regime changes, or shifting mean | - Entry threshold (entry_th)<br>- Exit threshold (exit_th)<br>- Z-score or standardized deviation measure<br>- Position sizing |
| **Triangular Arbitrage (3 currencies / FX pairs)** | Exploit **inconsistencies among 3 related exchange rates** (e.g., BTC/EUR × EUR/USDT ≠ BTC/USDT) | Highly liquid, fast markets where execution is near-instantaneous | Illiquid markets, high latency, deep order book needed, large spreads | - Price/cross-rate thresholds (margin)<br>- Capital allocation<br>- Transaction fees and slippage consideration |

### Key Notes
1. **Execution speed matters**
   - Arbitrage & Triangular arbitrage require **low latency**.
   - Rebalancing & Mean Reversion tolerate slower execution.  
2. **Transaction costs are critical**
   - Arbitrage strategies are **fee-sensitive**.
   - Rebalancing: band threshold prevents **over-trading**.  
3. **Market regime impacts success**
   - Sideways/volatile → Mean Reversion & Rebalancing excel
   - Trending → Rebalancing & Mean Reversion underperform  
4. **Thresholds are your tuning knobs**
   - Arbitrage: ratio deviation threshold
   - Mean Reversion: entry & exit z-score
   - Rebalancing: deviation band
   - Triangular Arb: margin above/below equilibrium
