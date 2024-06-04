import os
import requests
import json
# from dotenv import load_dotenv
from urllib.parse import urlencode

# load_dotenv()

# base_url = "https://codeforces.com/api/user.status"

def get_url(cf_handle):
    params = {
    "handle": cf_handle,
    "from": "1",
    "count": "100"
    }

    encoded_parameters = urlencode(params)
    return f"https://codeforces.com/api/user.status?{encoded_parameters}"


def send_request(cf_handle):

    response = requests.get(get_url(cf_handle))
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '..', 'data', 'submission_data.jsonl')
    
    if response.status_code == 200:
        data = response.json()

        with open(file_path, 'w') as file:
            for submission in data['result']:
                problem = submission.get('problem', {})
                deal = {
                    'rating': problem.get('rating', ''),
                    'verdict': submission.get('verdict', ''),
                    # 'index': problem.get('index', ''),
                    'name': problem.get('name', ''),
                    'tags': problem.get('tags', []),
                    # 'language': submission.get('programmingLanguage', ''),
                    'problem_url': f"https://codeforces.com/problemset/problem/{problem.get('contestId', '')}/{problem.get('index', '')}",
                }

                doc_object = {"doc": str(deal)}
                file.write(json.dumps(doc_object) + '\n')

        # print(data['result'][0])

        # with open(data,'r') as file:
        #     print(file.read())

    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

# send_request("Anav_Agrawal")
