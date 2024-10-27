import time
import yfinance as yf
import subprocess
from datetime import datetime, timedelta
import argparse
from collections import deque
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def fetch_nifty_value():
    """Fetches the current NIFTY 50 index value."""
    ticker = yf.Ticker('^NSEI')
    todays_data = ticker.history(period='1d', interval='1m')
    if todays_data.empty or 'Close' not in todays_data.columns:
        return None
    current_value = todays_data['Close'].iloc[-1]
    return current_value

def trigger_alert(message):
    """Triggers a system alert on macOS."""
    script = f'display notification "{message}" with title "NIFTY Alert"'
    subprocess.call(['osascript', '-e', script])

def start_fetching(target_levels):
    """Starts the data fetching, monitoring, and trend analysis loop."""
    try:
        alerted_levels = set()
        value_history = deque()  # Store tuples of (timestamp, value)
        while True:
            current_value = fetch_nifty_value()
            if current_value is None:
                print("Failed to fetch NIFTY value. Retrying in 30 seconds...")
                time.sleep(30)
                continue
            timestamp = datetime.now()
            value_history.append((timestamp, current_value))
            # Remove data older than the maximum interval we are interested in (e.g., 1 hour)
            while value_history and timestamp - value_history[0][0] > timedelta(hours=1):
                value_history.popleft()
            # Determine trends over standard intervals
            intervals = [1, 5, 15, 30, 60]  # in minutes
            trends = {}
            for interval in intervals:
                past_time = timestamp - timedelta(minutes=interval)
                # Find the value closest to the past_time
                past_value = None
                for t, v in value_history:
                    if t <= past_time:
                        past_value = v
                    else:
                        break
                if past_value is not None:
                    if current_value > past_value:
                        trends[interval] = '↑'  # Up arrow
                    elif current_value < past_value:
                        trends[interval] = '↓'  # Down arrow
                    else:
                        trends[interval] = '~'  # Right arrow (no change)
                else:
                    trends[interval] = 'N/A'
            # Color the current value
            if len(value_history) > 1:
                last_value = value_history[-2][1]
                if current_value > last_value:
                    color = Fore.GREEN
                elif current_value < last_value:
                    color = Fore.RED
                else:
                    color = Fore.WHITE
            else:
                color = Fore.WHITE

            # Prepare trend string
            trend_str = ' | '.join([f"{interval} min {trends[interval]}" for interval in intervals])

            print(f"{color}[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] NIFTY Value: {current_value:.2f} | Trends: {trend_str}")

            # Check for target levels
            for level in target_levels:
                if level in alerted_levels:
                    continue  # Skip levels that have already triggered an alert
                if current_value >= level:
                    message = f"NIFTY has reached or crossed the level of {level}."
                    trigger_alert(message)
                    print(f"Alert triggered: {message}")
                    alerted_levels.add(level)

            # Wait for 30 seconds
            time.sleep(30)
    except KeyboardInterrupt:
        print("Stopped fetching data.")

def parse_arguments():
    parser = argparse.ArgumentParser(description='NIFTY Tracker CLI')
    parser.add_argument('levels', metavar='N', type=float, nargs='*',
                        help='Absolute NIFTY levels to monitor (e.g., 18000 18200 18500)')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    target_levels = sorted(args.levels)
    if target_levels:
        print(f"Monitoring NIFTY levels: {target_levels}")
    else:
        print("No target levels specified.")
    start_fetching(target_levels)
