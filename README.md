![Screenshot 2024-10-28 at 01 39 09](https://github.com/user-attachments/assets/f3a31a2c-95bc-4d0f-981a-7d56772f1d72)

# NIFTY Tracker

A command-line tool to monitor the **NIFTY 50 index** in real-time, analyze trends over standard intervals, and receive system alerts when specified levels are reached.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Command-Line Arguments](#command-line-arguments)
  - [Running the Script](#running-the-script)
- [Example Output](#example-output)
- [Creating an Executable](#creating-an-executable)
  - [Using PyInstaller](#using-pyinstaller)
- [Troubleshooting](#troubleshooting)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)
- [Acknowledgments](#acknowledgments)
- [Contact](#contact)

---

## Introduction

`nifty_tracker.py` is a Python script that allows users to monitor the **NIFTY 50 index** in real-time. It fetches the current NIFTY index value at regular intervals, analyzes trends over various time frames, and provides visual alerts when the index reaches specified levels.

---

## Features

- **Real-Time Monitoring**: Fetches the current NIFTY 50 index value every 30 seconds.
- **Trend Analysis**: Analyzes trends over standard intervals (1 min, 5 min, 15 min, 30 min, 60 min).
- **Visual Indicators**: Displays trends using up/down arrows and colors (green for up, red for down, white for no change).
- **Custom Alerts**: Allows users to specify target NIFTY levels; triggers system notifications when these levels are reached.
- **Command-Line Interface**: Easy to use with command-line arguments for quick configuration.
- **Cross-Platform Compatibility**: Designed for macOS but can be adapted for Windows and Linux.

---

## Prerequisites

- **Operating System**: macOS (for system notifications using `osascript`)
- **Python**: Version 3.6 or higher
- **Python Packages**:
  - `nsepython`
  - `colorama`

---

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/nifty_tracker.git
   cd nifty_tracker
   ```

2. **Set Up a Virtual Environment (Optional but Recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Required Packages**

   ```bash
   pip install nsepython colorama
   ```

---

## Usage

### Command-Line Arguments

- **Target Levels**: You can specify one or more NIFTY index levels as command-line arguments. The script will trigger alerts when these levels are reached or crossed.

### Running the Script

1. **Basic Usage**

   ```bash
   python nifty_tracker.py [levels]
   ```

   - Replace `[levels]` with the NIFTY levels you want to monitor, separated by spaces.

2. **Examples**

   - **Monitor Specific Levels**

     ```bash
     python nifty_tracker.py 18000 18200 18500
     ```

   - **Run Without Target Levels**

     ```bash
     python nifty_tracker.py
     ```

     - The script will display the NIFTY index value and trends but will not trigger any level-based alerts.

---

## Example Output

```
Monitoring NIFTY levels: [18000.0, 18200.0, 18500.0]
[2023-10-27 09:15:00] NIFTY Value: 17950.25 | Trends: 1 min N/A | 5 min N/A | 15 min N/A | 30 min N/A | 60 min N/A
[2023-10-27 09:15:30] NIFTY Value: 17960.50 | Trends: 1 min ↑ | 5 min N/A | 15 min N/A | 30 min N/A | 60 min N/A
[2023-10-27 09:16:00] NIFTY Value: 17955.00 | Trends: 1 min ↓ | 5 min N/A | 15 min N/A | 30 min N/A | 60 min N/A
[2023-10-27 09:16:30] NIFTY Value: 18005.75 | Trends: 1 min ↑ | 5 min N/A | 15 min N/A | 30 min N/A | 60 min N/A
Alert triggered: NIFTY has reached or crossed the level of 18000.0.
```

- **Color Indicators**:
  - **Green Text**: Immediate upward trend.
  - **Red Text**: Immediate downward trend.
  - **White Text**: No immediate change or first data point.

- **Trend Symbols**:
  - **↑**: Upward trend.
  - **↓**: Downward trend.
  - **→**: No change.
  - **N/A**: Not enough data for the interval.

---

## Creating an Executable

### Using PyInstaller

You can create a standalone executable of the script using PyInstaller.

1. **Install PyInstaller**

   ```bash
   pip install pyinstaller
   ```

2. **Generate the Executable**

   ```bash
   pyinstaller --onefile --name nifty_tracker nifty_tracker.py \
   --hidden-import nsepython \
   --hidden-import pandas \
   --hidden-import numpy \
   --hidden-import requests \
   --hidden-import dateutil \
   --hidden-import certifi \
   --hidden-import pytz
   ```

3. **Run the Executable**

   ```bash
   ./dist/nifty_tracker 18000 18200 18500
   ```

4. **Optionally, Move the Executable to a Directory in PATH**

   ```bash
   sudo mv dist/nifty_tracker /usr/local/bin/
   sudo chmod +x /usr/local/bin/nifty_tracker
   ```

5. **Run from Anywhere**

   ```bash
   nifty_tracker 18000 18200 18500
   ```

**Note**: The executable is platform-specific. An executable built on macOS will only run on macOS.

---

## Troubleshooting

- **ModuleNotFoundError**

  - Ensure all dependencies are installed in your environment.

    ```bash
    pip install nsepython colorama
    ```

  - When using PyInstaller, include missing modules with `--hidden-import`.

- **SSL Certificate Errors**

  - Include `certifi` in hidden imports when building the executable.

- **Unicode Characters Not Displaying Correctly**

  - If trend arrows don't display properly, replace them with text equivalents in the script.

- **Notifications Not Appearing**

  - Ensure that notifications are enabled for Terminal or your Python environment in macOS System Preferences.

- **Data Not Updating**

  - Ensure you are running the script during Indian stock market hours (9:15 AM to 3:30 PM IST).
  - Check your internet connection.

---

## Customization

- **Change Fetch Interval**

  - Modify the `time.sleep(30)` line in the script to change how often data is fetched.

- **Adjust Trend Intervals**

  - Edit the `intervals` list in the `start_fetching` function.

    ```python
    intervals = [1, 5, 15, 30, 60]  # in minutes
    ```

- **Modify Alert Conditions**

  - Change the condition in the `start_fetching` function to trigger alerts when the index falls below a level.

    ```python
    if current_value <= level:
        # Trigger alert
    ```

- **Cross-Platform Notifications**

  - Replace the `trigger_alert` function to use a cross-platform library like `plyer`.

    ```python
    from plyer import notification

    def trigger_alert(message):
        notification.notify(
            title='NIFTY Alert',
            message=message,
            timeout=10
        )
    ```

- **Change Colors**

  - Adjust the colors used by modifying the `colorama` `Fore` attributes in the script.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Project**

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m 'Add some feature'
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Disclaimer

- **Data Accuracy**

  - The script relies on data from NSE via `nsepython`. Ensure compliance with NSE's terms of service.
  - Verify critical information through official channels.

- **Usage Terms**

  - Be mindful of any rate limits or usage restrictions associated with the data sources.

---

## Acknowledgments

- **nsepython**: For providing an interface to fetch real-time data from NSE.
- **colorama**: For enabling colored terminal text.
- **PyInstaller**: For packaging the script into an executable.

---

## Contact

- **Author**: [Your Name]
- **Email**: [your.email@example.com](mailto:mdibrahimhassan@gmail.com)
- **GitHub**: [yourusername](https://github.com/Ibrahimhass)

Feel free to open an issue if you have any questions or suggestions.

---

**Note**: Replace placeholders like `[Your Name]`, `your.email@example.com`, and `yourusername` with your actual information.
