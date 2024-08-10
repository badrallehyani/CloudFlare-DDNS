import os
from dotenv import load_dotenv
load_dotenv()

from cloudflare import Cloudflare
from requests import get

auth = os.getenv("auth")
me = Cloudflare(auth)

# Get Zones
domainName = 'badr.dev' # replace with urs
zone = me.getZones(domainName).json()['result'][0]

# Get DNS Records
DNSRecords = me.getDNSRecords(zone['id'])

# Change the root IP to THIS device ip
newIP = get('https://ifconfig.me').text

for record in DNSRecords:
    if record.name == domainName:
        res = record.change( newContent = newIP )
        input(res.json())
        break
