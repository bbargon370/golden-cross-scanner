# golden-cross-scanner

A simple Python utility for scanning a list of stock tickers and reporting those
that have recently formed a **golden cross**. A golden cross occurs when a
short-term moving average (50-day by default) crosses above a long-term moving
average (200-day by default), which many traders interpret as a bullish signal.

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python golden_cross_scanner.py TICKER [TICKER ...]
```

The script will download historical price data for the supplied tickers using
`yfinance` and print those that have a golden cross in the most recent data.
