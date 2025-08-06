import sys
from typing import List

import yfinance as yf
import pandas as pd


def has_golden_cross(df: pd.DataFrame, short_window: int = 50, long_window: int = 200) -> bool:
    """Return True if DataFrame contains a golden cross in the most recent data.

    A golden cross occurs when the short moving average crosses above the long
    moving average after previously being below it. We only check the last two
    points to determine if a cross has just happened.
    """
    if len(df) < long_window + 2:
        # not enough data to compute moving averages
        return False

    short_ma = df['Close'].rolling(window=short_window).mean()
    long_ma = df['Close'].rolling(window=long_window).mean()

    # compute the difference between short and long moving averages
    diff = short_ma - long_ma

    # check if there is a crossing on the latest day
    prev_diff = diff.iloc[-2]
    last_diff = diff.iloc[-1]

    return prev_diff < 0 and last_diff > 0


def scan_tickers(tickers: List[str], period: str = "1y") -> List[str]:
    """Return a list of tickers that formed a golden cross in the last period."""
    matches = []
    for ticker in tickers:
        try:
            data = yf.download(ticker, period=period, progress=False)
        except Exception as exc:  # pragma: no cover - network issues
            print(f"Failed to download data for {ticker}: {exc}", file=sys.stderr)
            continue

        if data.empty:
            print(f"No data for {ticker}", file=sys.stderr)
            continue

        if has_golden_cross(data):
            matches.append(ticker)

    return matches


def main(args: List[str]) -> int:
    if not args:
        print("Usage: python golden_cross_scanner.py TICKER [TICKER ...]")
        return 1

    tickers = args
    matches = scan_tickers(tickers)

    if matches:
        print("Tickers with a recent golden cross:")
        for ticker in matches:
            print(f"- {ticker}")
    else:
        print("No golden crosses detected among the provided tickers.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
