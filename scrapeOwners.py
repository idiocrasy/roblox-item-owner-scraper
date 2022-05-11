import os, random, requests
from threading import Thread, activeCount

threads = 100
assetids =  open('ids.txt','r').read().splitlines()
cookie = open('cookie.txt','r').readline().strip()
proxies = [{'https':'http://'+proxy} for proxy in open('proxies.txt','r').read().splitlines()]

def getName(ids, filename):
    global usernames
    idlists = [ids[x:x+200] for x in range(0, len(ids), 200)]
    for idlist in idlists:
        try:
            r = requests.post('https://users.roblox.com/v1/users', data={"userIds":idlist, "excludeBannedUsers":True}, proxies=random.choice(proxies)).json()['data']
            names = [f['name']+'\n' for f in r]
            usernames += len(names)
            with open(filename, 'a') as f:
                f.writelines(names)
        except Exception as e:
            idlists.append(idlist)

def scrape(assetid, filename):
    cursor = ''
    while True:
        try:
            r = req.get(f'https://inventory.roblox.com/v2/assets/{assetid}/owners?sortOrder=Asc&cursor={cursor}&limit=100').json()
            Thread(target=getName, args=([x['owner']['id'] for x in r['data'] if x['owner']], filename)).start()
            cursor = r['nextPageCursor']
            if not cursor: break
        except Exception as e:
            print(e)

def thread():
    while assetids:
        aid = assetids.pop()
        try:
            fname = requests.get(f'https://api.roblox.com/Marketplace/ProductInfo?assetId={aid}').json()['Name']
            fname = ''.join(c if c.isalnum() else '-' for c in fname)
        except:
            fname = str(aid)
        scrape(aid, os.path.join(f'lists/{fname}.txt'))
        print('finished', fname)

usernames = 0
req = requests.Session()
req.cookies['.ROBLOSECURITY'] = cookie
r = req.get('http://www.roblox.com/mobileapi/userinfo')
if 'mobileapi/userinfo' not in r.url:
    input('Invalid Cookie.')
    exit()

for i in range(threads):
    Thread(target=thread).start()

while 1:
    os.system(f'title AssetIDs left: {len(assetids)} ~ Threads Remaining: {activeCount()-1} ~ Usernames scraped: {usernames}')
