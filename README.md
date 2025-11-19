# DayTrade - Stock Analysis and Trading Strategies

A Python-based framework for testing daytrading strategies using only public web data from Yahoo Finance, SEC filings, Reddit, and other sources.

## Overview

This repository contains tools and algorithms for analyzing stock market data and generating trading signals based on various strategies. The primary focus is on earnings correlation analysis - a strategy that leverages sector-wide patterns observed during earnings seasons.

## Features

### Data Collection
- **Yahoo Finance Integration**: Automated collection of historical price data and company summaries
- **S&P 500 Coverage**: Pre-configured to track 500+ stocks from the S&P 500 index
- **Earnings Data**: Extraction of earnings call dates, estimates, and actuals
- **Sector Classification**: Automatic grouping of stocks by industry sector

### Analysis Tools

#### Earnings Correlation Analyzer
A sophisticated algorithm that generates trading signals based on correlated company earnings calls:
- Identifies companies in the same sector as your target stock
- Analyzes historical price movements after earnings calls
- Calculates statistical metrics (average change, standard deviation, positive/negative ratios)
- Generates BUY/SELL/NEUTRAL signals with confidence scores
- Tracks upcoming earnings calendars for leading indicators

## Repository Structure

```
daytrade/
├── data/                    # Data storage directory
│   ├── chart/              # Historical price data (501 stocks)
│   ├── summary/            # Company summary data (501 stocks)
│   └── spy/                # S&P 500 ticker lists (10 files)
├── log/                    # Execution logs
├── notebook/               # Jupyter notebooks for analysis
│   ├── analysis.ipynb      # Main analysis notebook
│   ├── earnings_correlation_example.ipynb  # Earnings strategy examples
│   ├── spy.ipynb          # S&P 500 data exploration
│   └── yahoo.ipynb        # Yahoo Finance API testing
└── src/                    # Source code
    ├── earnings_correlation_analyzer.py  # Main algorithm
    ├── get_spy.py         # Data collection script
    ├── get_spy.sh         # Batch data collection
    ├── kill_sessions.sh   # Utility script
    └── yahoo.py           # Yahoo Finance API wrapper

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Dependencies
```bash
pip install pandas numpy requests
```

For Jupyter notebook support:
```bash
pip install jupyter matplotlib
```

## Usage

### 1. Earnings Correlation Analysis

Analyze a stock and get trading signals based on correlated company earnings:

```bash
cd src
python3 earnings_correlation_analyzer.py --symbol AAPL --days-after 5
```

**Parameters:**
- `--symbol`: Stock ticker symbol to analyze (required)
- `--days-after`: Number of trading days to measure price change (default: 5)
- `--data-dir`: Path to data directory (default: ../data)
- `--output`: Save results to JSON file (optional)

**Example Output:**
```
============================================================
Earnings Correlation Analysis for AAPL
============================================================

Target Sector: Technology

Finding correlated companies...
Found 81 correlated companies in same sector

Historical Earnings Analysis (past 80 earnings calls)
------------------------------------------------------------
Average price change after 5 days: -0.09%
Median price change: 0.09%
Standard deviation: 4.97%
Positive movements: 41 (51.2%)
Negative movements: 39 (48.8%)

Trading Signal:
------------------------------------------------------------
Signal: NEUTRAL
Confidence: 48.8%
Reasoning: Based on 80 historical earnings calls from
           20 correlated companies
```

### 2. Batch Data Collection

Collect fresh data from Yahoo Finance:

```bash
cd src
./get_spy.sh
```

This script runs 10 parallel sessions to collect data for all S&P 500 stocks.

### 3. Jupyter Notebook Analysis

Launch Jupyter and explore the example notebooks:

```bash
jupyter notebook notebook/earnings_correlation_example.ipynb
```

The notebook includes:
- Single stock analysis examples
- Multi-stock comparisons
- Visualization of results
- Time horizon analysis
- Signal export for trading systems

## Strategy: Earnings Correlation

### Hypothesis
Companies in the same sector often exhibit similar price movements following their respective earnings calls. This creates an opportunity:
1. Monitor earnings calls from companies in the same sector
2. Observe their post-earnings price movements
3. Use this information as a leading indicator for other companies in the sector

### Implementation
The algorithm:
1. Identifies the target company's sector
2. Finds all correlated companies (same sector)
3. Analyzes historical earnings data:
   - Extracts quarterly earnings dates
   - Measures price changes N days after each earnings call
   - Calculates earnings surprises (actual vs. estimate)
4. Computes statistical metrics:
   - Average and median price change
   - Standard deviation (volatility)
   - Positive/negative movement ratio
5. Generates trading signal:
   - **BUY**: >60% positive movements + avg change >1%
   - **SELL**: <40% positive movements + avg change <-1%
   - **NEUTRAL**: Otherwise
6. Provides upcoming earnings calendar for timing

### Use Cases
- **Pre-earnings positioning**: Position yourself before target company earnings based on sector patterns
- **Sector rotation**: Identify which sectors show strong post-earnings momentum
- **Risk assessment**: Understand typical volatility after earnings in a sector
- **Calendar strategy**: Trade around known earnings dates

## Data Structure

### Chart Data
JSON files containing historical OHLC (Open, High, Low, Close) price data:
```json
{
  "meta": {
    "symbol": "AAPL",
    "currency": "USD",
    "exchangeName": "NMS"
  },
  "timestamp": [1234567890, ...],
  "indicators": {
    "quote": [{
      "open": [...],
      "high": [...],
      "low": [...],
      "close": [...],
      "volume": [...]
    }],
    "adjclose": [...]
  }
}
```

### Summary Data
JSON files with comprehensive company information:
- Earnings history and estimates
- Upcoming earnings dates
- Sector and industry classification
- Financial metrics
- Analyst recommendations

### S&P 500 Lists
CSV files containing ticker symbols with metadata:
```csv
,index,name,ticker,identifier,sedol,weight,sector,sharesheld,localcurrency
0,0,APPLE INC,AAPL,037833100,2046251,6.689877,-,184676605.0,USD
```

## Development

### Adding New Strategies
1. Create a new Python file in `src/`
2. Import data loaders from `earnings_correlation_analyzer.py`
3. Implement your analysis logic
4. Add examples to a Jupyter notebook

### Extending Data Collection
- Modify `yahoo.py` to add new Yahoo Finance endpoints
- Update `get_spy.py` to collect additional data points
- Add new data sources beyond Yahoo Finance

## Limitations and Disclaimers

⚠️ **Important Notes:**
- This is for educational and research purposes only
- Historical performance does not guarantee future results
- Always perform your own due diligence before trading
- The algorithms use approximations (e.g., quarter end dates)
- Data quality depends on Yahoo Finance API availability
- No warranty or guarantee of accuracy is provided

## Contributing

Contributions are welcome! Areas for improvement:
- Additional trading strategies
- Enhanced data collection (SEC filings, social media sentiment)
- Backtesting framework
- Real-time data integration
- Risk management tools
- Performance tracking

## License

This project uses publicly available data and is intended for educational purposes.

## Acknowledgments

- Data sourced from Yahoo Finance
- S&P 500 constituent data
- Open source Python data science ecosystem (pandas, numpy)

