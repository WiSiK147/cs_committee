# Codeforces League Leaderboard Aggregator

This script automatically fetches and aggregates the total number of solved problems for participants across multiple contests within a private Codeforces group. It ignores time penalties and hacking points, focusing purely on the number of successful solves, and outputs the results into clean JSON files for web integration.

*Note: This project is fully vibe-coded.*

## Features
* **Multi-League Support:** Aggregate different sets of contests into separate JSON leaderboards (e.g., Pro and Challenger).
* **Penalty-Free Scoring:** Ranks participants purely by the number of problems solved (`points > 0`).
* **Secure Configuration:** Uses a `.env` file to store both your Codeforces API credentials and your contest IDs.
* **Automated Rate Limiting:** Built-in delays prevent API bans from Codeforces.

## Prerequisites
* Python 3.x
* `requests`
* `python-dotenv`

## Setup & Configuration
1. Clone or download this repository.
2. Install the required Python packages:
   ```bash
   pip install requests python-dotenv
   ```
3. Create a `.env` file in the root directory and add your Codeforces API credentials and your comma-separated contest IDs:
   ```env
   CF_API_KEY="your_api_key_here"
   CF_API_SECRET="your_api_secret_here"
   LEAGUE_PRO_IDS="123456,123457,123458"
   LEAGUE_CHA_IDS="987654,987655"
   ```
   *(Generate credentials at [Codeforces API Settings](https://codeforces.com/settings/api))*

## Usage
Run the script via terminal:
```bash
python cf_leaderboard_script.py
```
The script will fetch the standings, aggregate the solves, and generate the configured JSON files (`league_pro.json` and `league_challenger.json`) in the same directory.
