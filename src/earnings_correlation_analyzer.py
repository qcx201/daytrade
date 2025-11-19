#!/usr/bin/env python3
"""
Earnings Correlation Analyzer

This script analyzes stock price movements based on earnings calls of correlated companies.
The strategy is based on the hypothesis that correlated companies (same sector, similar business)
often show similar price movements after their respective earnings calls.

Usage:
    python earnings_correlation_analyzer.py --symbol AAPL --days-after 5
"""

import os
import sys
import json
import argparse
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict


def load_summary_data(data_dir, symbol):
    """Load summary data for a given symbol."""
    filepath = os.path.join(data_dir, 'summary', f'summary-{symbol.lower()}.json')
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as f:
        return json.load(f)


def load_chart_data(data_dir, symbol):
    """Load historical price chart data for a given symbol."""
    filepath = os.path.join(data_dir, 'chart', f'chart-{symbol.lower()}.json')
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as f:
        return json.load(f)


def parse_quarter_date(quarter_str):
    """Convert quarter string like '1Q2024' to approximate date."""
    import re
    match = re.match(r'(\d)Q(\d{4})', quarter_str)
    if not match:
        return None
    
    quarter = int(match.group(1))
    year = int(match.group(2))
    
    # Approximate month for each quarter (end of quarter)
    quarter_months = {1: 3, 2: 6, 3: 9, 4: 12}
    month = quarter_months.get(quarter, 3)
    
    return datetime(year, month, 28)  # Use 28th to avoid month-end issues


def get_earnings_dates(summary_data):
    """Extract earnings call dates from summary data."""
    if not summary_data:
        return []
    
    earnings_dates = []
    
    # Get historical earnings from earnings chart
    earnings_chart = summary_data.get('earnings', {}).get('earningsChart', {})
    quarterly = earnings_chart.get('quarterly', [])
    
    for quarter in quarterly:
        if 'date' in quarter:
            quarter_date = parse_quarter_date(quarter['date'])
            if quarter_date:
                earnings_dates.append({
                    'date': quarter_date,
                    'quarter_str': quarter['date'],
                    'actual': quarter.get('actual', {}).get('raw'),
                    'estimate': quarter.get('estimate', {}).get('raw')
                })
    
    # Get upcoming earnings date
    calendar_events = summary_data.get('calendarEvents', {})
    if 'earnings' in calendar_events:
        earnings_info = calendar_events['earnings']
        if 'earningsCallDate' in earnings_info:
            call_dates = earnings_info['earningsCallDate']
            if call_dates:
                earnings_dates.append({
                    'date': call_dates[0].get('fmt'),
                    'upcoming': True
                })
    
    return earnings_dates


def get_sector(summary_data):
    """Extract sector information from summary data."""
    if not summary_data:
        return None
    
    profile = summary_data.get('summaryProfile', {})
    return profile.get('sector', profile.get('industry'))


def calculate_price_change(chart_data, start_date, days_after):
    """
    Calculate price change percentage after a specific date.
    
    Args:
        chart_data: Historical price data
        start_date: Date string in format 'YYYY-MM-DD', timestamp, or datetime object
        days_after: Number of trading days to measure change
    
    Returns:
        Dictionary with price change metrics
    """
    if not chart_data:
        return None
    
    timestamps = chart_data.get('timestamp', [])
    quotes = chart_data.get('indicators', {}).get('quote', [{}])[0]
    closes = quotes.get('close', [])
    
    if not timestamps or not closes:
        return None
    
    # Convert start_date to timestamp
    if isinstance(start_date, datetime):
        start_ts = int(start_date.timestamp())
    elif isinstance(start_date, str):
        try:
            if '-' in start_date:
                dt = datetime.strptime(start_date, '%Y-%m-%d')
            else:
                dt = datetime.strptime(start_date, '%Y/%m/%d')
            start_ts = int(dt.timestamp())
        except:
            return None
    else:
        start_ts = start_date
    
    # Find the closest timestamp on or after start date
    start_idx = None
    for i, ts in enumerate(timestamps):
        if ts >= start_ts and closes[i] is not None:
            start_idx = i
            break
    
    if start_idx is None or start_idx + days_after >= len(timestamps):
        return None
    
    # Find price at start and after N days
    start_price = closes[start_idx]
    
    # Look for valid close price within days_after range
    end_price = None
    end_idx = None
    for i in range(start_idx + 1, min(start_idx + days_after + 5, len(closes))):
        if closes[i] is not None:
            if end_idx is None or (i - start_idx) <= days_after:
                end_price = closes[i]
                end_idx = i
            if (i - start_idx) >= days_after:
                break
    
    if end_price is None or start_price is None or start_price == 0:
        return None
    
    pct_change = ((end_price - start_price) / start_price) * 100
    
    return {
        'start_price': start_price,
        'end_price': end_price,
        'pct_change': pct_change,
        'days': end_idx - start_idx if end_idx else None
    }


def find_correlated_companies(data_dir, target_symbol, target_sector):
    """
    Find companies in the same sector as the target company.
    
    Args:
        data_dir: Path to data directory
        target_symbol: The target stock symbol
        target_sector: The target company's sector
    
    Returns:
        List of correlated company symbols
    """
    summary_dir = os.path.join(data_dir, 'summary')
    correlated = []
    
    for filename in os.listdir(summary_dir):
        if not filename.startswith('summary-') or not filename.endswith('.json'):
            continue
        
        symbol = filename.replace('summary-', '').replace('.json', '').upper()
        
        if symbol == target_symbol.upper():
            continue
        
        summary = load_summary_data(data_dir, symbol)
        sector = get_sector(summary)
        
        if sector and target_sector and sector.lower() == target_sector.lower():
            correlated.append(symbol)
    
    return correlated


def analyze_earnings_correlation(data_dir, target_symbol, days_after=5, min_historical=3):
    """
    Analyze correlation between earnings calls and subsequent price movements.
    
    Args:
        data_dir: Path to data directory
        target_symbol: The target stock symbol to analyze
        days_after: Number of days after earnings to measure price change
        min_historical: Minimum number of historical earnings to analyze
    
    Returns:
        Dictionary with analysis results and trading signals
    """
    print(f"\n{'='*60}")
    print(f"Earnings Correlation Analysis for {target_symbol}")
    print(f"{'='*60}\n")
    
    # Load target company data
    target_summary = load_summary_data(data_dir, target_symbol)
    if not target_summary:
        return {'error': f'No summary data found for {target_symbol}'}
    
    target_sector = get_sector(target_summary)
    print(f"Target Sector: {target_sector}\n")
    
    # Find correlated companies
    print("Finding correlated companies...")
    correlated_companies = find_correlated_companies(data_dir, target_symbol, target_sector)
    print(f"Found {len(correlated_companies)} correlated companies in same sector\n")
    
    if len(correlated_companies) < 3:
        print("Warning: Too few correlated companies for reliable analysis")
    
    # Analyze historical earnings impact for correlated companies
    results = []
    
    for symbol in correlated_companies[:20]:  # Limit to top 20 for performance
        summary = load_summary_data(data_dir, symbol)
        chart = load_chart_data(data_dir, symbol)
        
        if not summary or not chart:
            continue
        
        earnings_dates = get_earnings_dates(summary)
        
        for earnings in earnings_dates:
            if earnings.get('upcoming'):
                continue
            
            date = earnings.get('date')
            quarter_str = earnings.get('quarter_str', str(date))
            if not date:
                continue
            
            price_change = calculate_price_change(chart, date, days_after)
            
            if price_change:
                results.append({
                    'symbol': symbol,
                    'date': quarter_str,
                    'pct_change': price_change['pct_change'],
                    'actual': earnings.get('actual'),
                    'estimate': earnings.get('estimate')
                })
    
    if not results:
        return {'error': 'Insufficient historical earnings data for analysis'}
    
    # Statistical analysis
    df = pd.DataFrame(results)
    
    print(f"Historical Earnings Analysis (past {len(results)} earnings calls)")
    print(f"{'-'*60}")
    print(f"Average price change after {days_after} days: {df['pct_change'].mean():.2f}%")
    print(f"Median price change: {df['pct_change'].median():.2f}%")
    print(f"Standard deviation: {df['pct_change'].std():.2f}%")
    print(f"Positive movements: {(df['pct_change'] > 0).sum()} ({(df['pct_change'] > 0).sum() / len(df) * 100:.1f}%)")
    print(f"Negative movements: {(df['pct_change'] < 0).sum()} ({(df['pct_change'] < 0).sum() / len(df) * 100:.1f}%)\n")
    
    # Check for earnings surprises
    df['surprise'] = df.apply(
        lambda x: (x['actual'] - x['estimate']) / x['estimate'] * 100 
        if x['actual'] is not None and x['estimate'] is not None and x['estimate'] != 0 
        else None, 
        axis=1
    )
    
    surprise_df = df[df['surprise'].notna()]
    if len(surprise_df) > 0:
        print("Earnings Surprise Analysis:")
        print(f"{'-'*60}")
        positive_surprise = surprise_df[surprise_df['surprise'] > 0]
        negative_surprise = surprise_df[surprise_df['surprise'] < 0]
        
        if len(positive_surprise) > 0:
            print(f"Positive surprises: avg price change = {positive_surprise['pct_change'].mean():.2f}%")
        if len(negative_surprise) > 0:
            print(f"Negative surprises: avg price change = {negative_surprise['pct_change'].mean():.2f}%")
        print()
    
    # Get upcoming earnings for correlated companies
    upcoming_earnings = []
    for symbol in correlated_companies[:20]:
        summary = load_summary_data(data_dir, symbol)
        if not summary:
            continue
        
        calendar_events = summary.get('calendarEvents', {})
        if 'earnings' in calendar_events:
            earnings_info = calendar_events['earnings']
            if 'earningsCallDate' in earnings_info:
                call_dates = earnings_info['earningsCallDate']
                if call_dates:
                    upcoming_earnings.append({
                        'symbol': symbol,
                        'date': call_dates[0].get('fmt'),
                        'timestamp': call_dates[0].get('raw')
                    })
    
    # Sort by date
    upcoming_earnings = sorted(upcoming_earnings, key=lambda x: x.get('timestamp', 0))
    
    print("Upcoming Earnings Calls from Correlated Companies:")
    print(f"{'-'*60}")
    if upcoming_earnings:
        for i, earning in enumerate(upcoming_earnings[:10], 1):
            print(f"{i}. {earning['symbol']}: {earning['date']}")
    else:
        print("No upcoming earnings calls found")
    print()
    
    # Generate trading signal
    avg_change = df['pct_change'].mean()
    positive_ratio = (df['pct_change'] > 0).sum() / len(df)
    
    signal = 'NEUTRAL'
    confidence = 0.0
    
    if positive_ratio > 0.6 and avg_change > 1.0:
        signal = 'BUY'
        confidence = min(positive_ratio * abs(avg_change) / 2, 100)
    elif positive_ratio < 0.4 and avg_change < -1.0:
        signal = 'SELL'
        confidence = min((1 - positive_ratio) * abs(avg_change) / 2, 100)
    else:
        confidence = 50 - abs(50 - positive_ratio * 100)
    
    print("Trading Signal:")
    print(f"{'-'*60}")
    print(f"Signal: {signal}")
    print(f"Confidence: {confidence:.1f}%")
    print(f"Reasoning: Based on {len(results)} historical earnings calls from")
    print(f"           {len(df['symbol'].unique())} correlated companies")
    
    if signal != 'NEUTRAL':
        print(f"\nStrategy: Monitor upcoming earnings from correlated companies.")
        print(f"          Expected {target_symbol} to move {signal.lower()} with average")
        print(f"          change of {avg_change:.2f}% within {days_after} trading days.")
    
    print(f"\n{'='*60}\n")
    
    return {
        'target_symbol': target_symbol,
        'sector': target_sector,
        'correlated_companies': len(correlated_companies),
        'historical_earnings_analyzed': len(results),
        'avg_price_change': avg_change,
        'median_price_change': df['pct_change'].median(),
        'std_price_change': df['pct_change'].std(),
        'positive_ratio': positive_ratio,
        'signal': signal,
        'confidence': confidence,
        'upcoming_earnings': upcoming_earnings[:5],
        'days_after': days_after
    }


def main():
    """Main function to run the earnings correlation analyzer."""
    parser = argparse.ArgumentParser(
        prog='earnings_correlation_analyzer',
        description='Analyze stock signals based on correlated company earnings calls',
    )
    
    parser.add_argument(
        '-s', '--symbol',
        required=True,
        type=str,
        help='Stock symbol to analyze (e.g., AAPL)'
    )
    
    parser.add_argument(
        '-d', '--days-after',
        default=5,
        type=int,
        help='Number of trading days after earnings to measure price change (default: 5)'
    )
    
    parser.add_argument(
        '--data-dir',
        default=None,
        type=str,
        help='Path to data directory (default: ../data)'
    )
    
    parser.add_argument(
        '-o', '--output',
        default=None,
        type=str,
        help='Output JSON file for results (optional)'
    )
    
    args = parser.parse_args()
    
    # Set up data directory
    if args.data_dir:
        data_dir = args.data_dir
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, '..', 'data')
    
    data_dir = os.path.abspath(data_dir)
    
    if not os.path.exists(data_dir):
        print(f"Error: Data directory not found: {data_dir}")
        sys.exit(1)
    
    # Run analysis
    results = analyze_earnings_correlation(
        data_dir,
        args.symbol,
        days_after=args.days_after
    )
    
    # Save results if output file specified
    if args.output and 'error' not in results:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=4)
        print(f"Results saved to: {args.output}")
    
    # Exit with error code if analysis failed
    if 'error' in results:
        print(f"Error: {results['error']}")
        sys.exit(1)


if __name__ == '__main__':
    main()
