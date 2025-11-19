# Quick Start Guide

Get started with the DayTrade earnings correlation analyzer in 5 minutes.

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Run Your First Analysis

```bash
cd src
python3 earnings_correlation_analyzer.py --symbol AAPL --days-after 5
```

This will analyze Apple (AAPL) and show you:
- How correlated tech companies performed after their earnings
- Average price movements in the sector
- Trading signal (BUY/SELL/NEUTRAL) with confidence
- Upcoming earnings dates to watch

## Step 3: Try Different Stocks and Sectors

### Technology Stocks
```bash
python3 earnings_correlation_analyzer.py --symbol MSFT --days-after 5
python3 earnings_correlation_analyzer.py --symbol NVDA --days-after 3
```

### Financial Stocks
```bash
python3 earnings_correlation_analyzer.py --symbol JPM --days-after 5
python3 earnings_correlation_analyzer.py --symbol BAC --days-after 10
```

### Healthcare Stocks
```bash
python3 earnings_correlation_analyzer.py --symbol JNJ --days-after 5
python3 earnings_correlation_analyzer.py --symbol UNH --days-after 5
```

## Step 4: Adjust the Time Horizon

The `--days-after` parameter controls how many trading days after earnings you measure:

- **1-3 days**: Capture immediate reaction, less noise
- **5 days**: Balanced view (default)
- **10-20 days**: Longer trend, more market noise

```bash
# Short-term (1 day)
python3 earnings_correlation_analyzer.py --symbol AAPL --days-after 1

# Medium-term (5 days) 
python3 earnings_correlation_analyzer.py --symbol AAPL --days-after 5

# Long-term (20 days)
python3 earnings_correlation_analyzer.py --symbol AAPL --days-after 20
```

## Step 5: Save Results to JSON

```bash
python3 earnings_correlation_analyzer.py --symbol AAPL --days-after 5 --output ../data/aapl_analysis.json
```

This saves the results in a structured format you can integrate with trading systems.

## Step 6: Explore the Jupyter Notebook

```bash
cd ../notebook
jupyter notebook earnings_correlation_example.ipynb
```

The notebook includes:
- Multiple stock comparisons
- Visualization of results
- Time horizon analysis
- Batch processing examples

## Understanding the Output

### Signal Types

- **BUY**: Sector shows strong positive momentum after earnings (>60% positive, avg >1%)
- **SELL**: Sector shows negative momentum after earnings (<40% positive, avg <-1%)
- **NEUTRAL**: No clear directional bias

### Confidence Score

- **0-30%**: Low confidence - pattern is weak or inconsistent
- **30-60%**: Medium confidence - moderate pattern observed
- **60-100%**: High confidence - strong consistent pattern

### How to Use

1. **Leading Indicator**: Watch for upcoming earnings from correlated companies
2. **Timing**: Position yourself before the target stock's earnings
3. **Risk Management**: Higher confidence = larger position size
4. **Validation**: Cross-reference with other technical/fundamental analysis

## Common Use Cases

### Case 1: Pre-Earnings Trade
```bash
# Check JPM before its earnings
python3 earnings_correlation_analyzer.py --symbol JPM --days-after 5
```
Look at "Upcoming Earnings Calls" - if you see other banks reporting soon, observe their results and position accordingly.

### Case 2: Sector Comparison
```bash
# Compare multiple banks
for symbol in JPM BAC WFC GS; do
    python3 earnings_correlation_analyzer.py --symbol $symbol --days-after 5
done
```
Find which bank has the strongest/weakest correlation signal.

### Case 3: Time Horizon Optimization
```bash
# Test multiple time horizons
for days in 1 3 5 10 20; do
    python3 earnings_correlation_analyzer.py --symbol AAPL --days-after $days
done
```
Find the optimal holding period for your strategy.

## Troubleshooting

### "No summary data found"
- Make sure the data directory exists: `../data/summary/`
- Check if the ticker symbol is correct and in the dataset
- Run data collection: `cd src && ./get_spy.sh`

### "Insufficient historical earnings data"
- Some stocks may have limited earnings history in the dataset
- Try a different stock in the same sector
- The dataset covers 501 S&P 500 stocks

### "Module not found" error
- Install dependencies: `pip install -r requirements.txt`
- Make sure you're using Python 3.8 or higher

## Next Steps

1. **Backtest**: Validate the strategy with historical data
2. **Automate**: Set up scheduled analysis before earnings seasons
3. **Integrate**: Connect to your broker's API for live trading
4. **Enhance**: Add more data sources (news sentiment, SEC filings)
5. **Monitor**: Track your trades and refine the strategy

## Tips

- 💡 Focus on sectors with tight correlation (financials, tech hardware)
- 💡 Earnings season happens quarterly - plan ahead
- 💡 Combine with position sizing based on confidence scores
- 💡 Use stop-losses - not all patterns play out every time
- 💡 Paper trade first to validate before using real money

## Getting Help

- Check the main README.md for detailed documentation
- Explore example notebooks in the `notebook/` directory
- Review the source code in `src/earnings_correlation_analyzer.py`

Happy trading! 📈
