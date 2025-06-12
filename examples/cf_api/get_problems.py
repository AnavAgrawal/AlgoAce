import sys
import os
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import json
import time

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '..', 'data', 'problems_data.jsonl')

def fetch_problems() :
    
    response = requests.get("https://codeforces.com/api/problemset.problems")

    if response.status_code == 200:
        data = response.json()

        problems = data['result']['problems'][:500]

        with open(file_path, 'w') as file:

            for problem in problems:
                deal = {
                    'rating': problem.get('rating', ''),
                    'name': problem.get('name', ''),
                    'tags': problem.get('tags', []),
                    'problem_url': f"https://codeforces.com/problemset/problem/{problem.get('contestId', '')}/{problem.get('index', '')}",
                }
                # print(deal)

                doc_object = {"doc": str(deal)}
                file.write(json.dumps(doc_object) + '\n')
        # print(data['result'][0])

        # with open(data,'r') as file:
        #     print(file.read())

    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

if __name__ == "__main__":
    fetch_problems()
    scheduler = BackgroundScheduler()
    # Runs every 30 mins to get the latest problems
    scheduler.add_job(fetch_problems, 'interval', minutes=30)
    # fetch_and_save_all_articles()
    try:
        print("Starting scheduler. Press Ctrl+C to exit.")
        scheduler.start()  # This will block the main thread
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("Exiting the script...")
        scheduler.shutdown()  # Cleanly shutdown the scheduler before exiting