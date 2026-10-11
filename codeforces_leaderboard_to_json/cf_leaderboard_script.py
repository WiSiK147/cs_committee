import os
import time
import random
import string
import hashlib
import requests
import json
from collections import defaultdict
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# ==========================================
# CONFIGURATION
# ==========================================
# Fetch credentials securely from .env
API_KEY = os.getenv('CF_API_KEY')
API_SECRET = os.getenv('CF_API_SECRET')

# Helper function to parse comma-separated IDs from the .env file
def parse_ids(env_string):
    if not env_string:
        return []
    return [int(x.strip()) for x in env_string.split(',') if x.strip()]

# Define your leagues, parsing the contest IDs directly from .env variables.
LEAGUES = {
    'league_pro.json': parse_ids(os.getenv('LEAGUE_PRO_IDS')),
    'league_challenger.json': parse_ids(os.getenv('LEAGUE_CHA_IDS'))
}
# ==========================================

def generate_api_sig(method_name, params):
    """Generates the required Codeforces API cryptographic signature."""
    rand6 = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    sorted_params = sorted(params.items())
    query_string = '&'.join([f"{k}={v}" for k, v in sorted_params])
    hash_base = f"{rand6}/{method_name}?{query_string}#{API_SECRET}"
    hash_hex = hashlib.sha512(hash_base.encode('utf-8')).hexdigest()
    return rand6 + hash_hex

def get_contest_standings(contest_id):
    """Fetches standings for a single contest."""
    method_name = 'contest.standings'
    
    params = {
        'apiKey': API_KEY,
        'contestId': contest_id,
        'time': int(time.time())
    }
    
    params['apiSig'] = generate_api_sig(method_name, params)
    url = f"https://codeforces.com/api/{method_name}"
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['status'] == 'OK':
            return data['result']
        else:
            print(f"Error fetching contest {contest_id}: {data.get('comment')}")
            return None
    except Exception as e:
        print(f"Failed to connect to Codeforces for contest {contest_id}: {e}")
        return None

def process_league(output_file, contest_ids):
    """Fetches data for a list of contests and exports to a specific JSON file."""
    if not contest_ids:
        print(f"Skipping {output_file}: No contest IDs provided.")
        return

    leaderboard = defaultdict(int)
    
    print(f"\n--- Processing {output_file} ({len(contest_ids)} contests) ---")
    
    for contest_id in contest_ids:
        print(f"Fetching Contest {contest_id}...")
        result = get_contest_standings(contest_id)
        
        if not result:
            continue
            
        for row in result['rows']:
            solved_in_contest = 0
            for problem_result in row['problemResults']:
                if problem_result['points'] > 0:
                    solved_in_contest += 1
            
            for member in row['party']['members']:
                handle = member['handle']
                leaderboard[handle] += solved_in_contest
                
        # 1.5-second sleep ensures you don't get IP banned by Codeforces
        time.sleep(1.5)

    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    
    json_data = []
    for rank, (handle, total_solved) in enumerate(sorted_leaderboard, start=1):
        json_data.append({
            "rank": rank,
            "handle": handle,
            "solved": total_solved
        })
        
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4)
        
    print(f"Success! {output_file} generated.")

def main():
    if not API_KEY or not API_SECRET:
        print("Error: API_KEY or API_SECRET not found. Please check your .env file.")
        return

    for output_file, contest_ids in LEAGUES.items():
        process_league(output_file, contest_ids)

if __name__ == "__main__":
    main()
