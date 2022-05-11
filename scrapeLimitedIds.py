import requests

minimum = int(input('minimum value: '))
maximum = int(input('maximum value: '))

r = requests.get('https://www.rolimons.com/itemapi/itemdetails').json()['items']

ids = [f'{id}\n' for id in list(r.keys()) if (r[id][3] >= minimum) and (r[id][3] <= maximum)]
with open('ids.txt','w') as f:
    f.writelines(ids)

input(f'scraped {len(ids)} limited IDs')