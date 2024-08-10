from requests import get, post, put, session


class Cloudflare:
    baseURL = 'https://api.cloudflare.com/client/v4'

    def __init__(self, auth):
        self.auth = auth
        
        headers ={
            'Authorization': auth,
            'Content-Type': 'application/json'
        }

        self.session = session()
        self.session.headers = headers
        

    def getZones(self, domainName):
        response = self.session.get('https://api.cloudflare.com/client/v4/zones', params={'name':domainName})
        return response

    def getDNSRecords(self, zoneID):
        response = self.session.get('https://api.cloudflare.com/client/v4/zones/' + zoneID + '/dns_records')

        DNSRecords_Objects = []
        DNSRecords = response.json()['result']
        for record in DNSRecords:
            DNSRecords_Objects.append( DNSRecord(record, self.session) )

        return DNSRecords_Objects


class DNSRecord:
    def __init__(self, data, session):
        self.id = data['id']
        self.zoneID = data['zone_id']
        self.zoneName = data['zone_name']
        self.name = data['name']
        self.type = data['type']
        
        self.content = data['content']
        
        self.proxiable = data['proxiable']
        self.proxied = data['proxied']

        self.data = {
            'type': self.type,
            'name': self.name,
            'proxied': self.proxied,
            'content': self.content
        }

        self.session = session

    def change(self, newContent = None, newProxied = None, newName = None, newType = None):

        if newContent:
            self.data['content'] = newContent

        if newProxied:
            self.data['proxied'] = newProxied

        if newName:
            self.data['name'] = newName

        if newType:
            self.data['type'] = newType

        response = self.session.put(f'https://api.cloudflare.com/client/v4/zones/{self.zoneID}/dns_records/{self.id}', json=self.data)
        return response

    def __str__(self):
        info = ''
        info += 'Name: ' + self.name
        info += '\nType: ' + self.type
        info += '\nContent: ' + self.content
        info += '\nProxied: ' + str(self.proxied)
        return info
