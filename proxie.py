import requests
from lxml import html
from lxml.html import fromstring
from itertools import cycle
import traceback

import urllib

page = urllib.urlopen("proxybullshit.html").read()
#print page

tree = html.fromstring(page)#.content

#print(page.content)
proxies = []
#likesText = tree.xpath('/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr[486]/td[1]/font[2]')[0]

table = tree.xpath('''//*[@onmouseover="this.style.background='#002424'"]''')
#print(table)
for i in range(len(table)):
    if i > 2:
        ip = table[i].xpath('td[1]/font[2]/text()[1]')
        #rint(ip)
        port = table[i].xpath('td[1]/font[2]/text()[2]')
        #print(port)
        print(ip[0] + ":" + port[0])
        proxies.append(ip[0] + ":" + port[0])
print(proxies)

#If you are copy pasting proxy ips, put in the list below
#proxies = ['121.129.127.209:80', '124.41.215.238:45169', '185.93.3.123:8080', '194.182.64.67:3128', '106.0.38.174:8080', '163.172.175.210:3128', '13.92.196.150:8080']
proxy_pool = cycle(proxies)

url = 'https://httpbin.org/ip'
for i in range(1,11):
    #Get a proxy from the pool
    proxy = next(proxy_pool)
    print("Request #%d"%i)
    try:
        response = requests.get(url,proxies={"http": proxy, "https": proxy})
        print(response.json())
    except:
        #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work.
        #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url
        print("Skipping. Connnection error")
