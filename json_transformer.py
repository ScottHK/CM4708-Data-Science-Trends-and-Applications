import pandas as pd
import os
import json

path = './raw_data/'
files = os.listdir(path)


for file in files:
    print(file)
    json_object = open(path + file, encoding='utf8')
    data = json.load(json_object)
    df = pd.DataFrame({
                'name': [],
                'implicitmod': [],
                'explicitmod': [],
                'price': [],
                'currency': [],
                'id': []
            })


    for stash in data['stashes']:

        if stash['public'] == True:

            for item in stash['items']:
                implicitmod = ''
                explicitmod = ''

                try:
                    note_string = item['note'].split(' ')
                except:
                    continue
                
                try:
                    for mod in item['implicitMods']:
                        implicitmod += mod + ';'
                except:
                    pass

                try:
                    for mod in item['explicitMods']:
                        explicitmod += mod + ';'
                except:
                    pass
                
                try:
                    df_item = pd.DataFrame({
                        'name': [item['name']],
                        'implicitmod': [implicitmod],
                        'explicitmod': [explicitmod],
                        'price': [note_string[1]],
                        'currency': [note_string[2]],
                        'id': [item['id']]
                    })

                    df = pd.concat([df, df_item])
                except:
                    continue

    df.to_csv('./processed_data/' + file + ".csv")