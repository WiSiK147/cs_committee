# Codeforces League Leaderboard Aggregator

This script automatically fetches and aggregates the total number of solved problems for participants across multiple contests within a private Codeforces group. It ignores time penalties and hacking points, focusing purely on the number of successful solves, and outputs the results into clean JSON files for web integration.

*Note: This project is fully vibe-coded.*

## Features
* **Multi-League Support:** Aggregate different sets of contests into separate JSON leaderboards (e.g., Div 1 and Div 2).
* **Penalty-Free Scoring:** Ranks participants purely by the number of problems solved (`points > 0`).
* **Secure Authentication:** Uses a `.env` file to keep your Codeforces API Key and Secret safe.
* **Automated Rate Limiting:** Built-in delays prevent API bans from Codeforces.

## Prerequisites
* Python 3.x
* `requests`
* `python-dotenv`

## Setup
1. Clone or download this repository.
2. Install the required Python packages:
   ```bash
   pip install requests python-dotenv
   ```
3. Create a `.env` file in the root directory and add your Codeforces API credentials:
   ```env
   CF_API_KEY="your_api_key_here"
   CF_API_SECRET="your_api_secret_here"
   ```
   *(Generate these at [Codeforces API Settings](https://codeforces.com/settings/api))*

## Configuration
Open the Python script and modify the `LEAGUES` dictionary to match your desired output files and Codeforces contest IDs:
```python
LEAGUES = {
    'league_div1.json': [123456, 123457],
    'league_div2.json': [987654, 987655]
}
```

## Usage
Run the script via terminal:
```bash
python cf_leaderboard_script.py
```
The script will fetch the standings, aggregate the solves, and generate the configured JSON files in the same directory.
