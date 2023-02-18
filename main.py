import requests
import json
import time
from datetime import datetime

# Settings (Placeholders used for sensitive information)
client_id = 'placeholder'       
client_secret = 'placeholder'   
production = 0

try:
    # Check if token already exists. Error will be thrown if the file doesn't already exist, executing the except
    with open("access_token.txt", "r") as file:
        token = file.read()

except:
    print('Token does not already exist! Requesting new token...')
    token = ''

if not token:

    # Request an access token
    token_response = requests.post('https://www.pathofexile.com/oauth/token', data={
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
        'scope': 'service:psapi'
    }, headers={'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'OAuth {}/0.0.1 (contact: placeholder)'.format(client_id)})

    # Parse the JSON response
    token_response_data = json.loads(token_response.text)
    # Extract the access token from response
    token = token_response_data['access_token']

    # Save the access token for future use
    print('Request successful. Writing for future use in access_token.txt')
    with open("access_token.txt", "w") as file:
        file.write(token)


access_token = token
counter = 1
next_change_id = None
string_date = str(datetime.today().strftime('%Y-%m-%d_%H-%M-%S'))

while True:

    url = 'https://api.pathofexile.com/public-stash-tabs'
    if next_change_id is not None:
        url += f'?id={next_change_id}'

    # In script method of seeing script running
    if not production:
        print("Change ID: " + next_change_id)

    # Use the access token to make a request to the Public Stash Tab API with a bearer token auth type
    response = requests.get(url, headers={
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'OAuth {}/0.0.1 (contact: placeholder)'.format(client_id)
    })

    # Parse the JSON response
    response_data = json.loads(response.text)

    file_name = './raw_data/{}_data{}.json'.format(string_date, str(counter))

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(response_data, f, ensure_ascii=False, indent=4)

    # Check if there are more pages of stash tabs
    if 'next_change_id' in response_data:
        next_change_id = response_data['next_change_id']
        counter += 1
        time.sleep(0.5)
    else:
        break