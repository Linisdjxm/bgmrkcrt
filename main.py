from audioop import ulaw2lin
import re
import requests
import json

ua2=r'linisdjxm/bangumi-corrected-rank (https://github.com/Linisdjxm/bgmrkcrt)'
header={'User-Agent': ua}
header2={'User-Agent': ua2}
URL = r"https://api.bgm.tv/v0/subjects/"

count = 1
re1 = re.compile(r'<a href="/subject/(?P<g1>[0-9]*)" class="l">(?P<g2>[\S ]*?)</a>[\S\s]*?Rank </small>(?P<g3>[0-9]*)</span>')
data=[]
datan = []
datar = []
rkd = []
lst = {}
edrk = {}
while count <= 10:
        textb = requests.get(r'https://bgm.tv/anime/browser?sort=rank&page=' + str(count),headers=header)
        textb.encoding = 'UTF-8'
        text=textb.text
        lst[count] = re.findall(re1,text)
        for item in lst[count]:
                #print(item)
                data.append(item[0])
                datan.append(item[1])
                datar.append(item[2])
        #print(data)
        count += 1
#print(data)
cx = 0
print("PROCESS 1")
for item in data:
        cx += 1
        textb = requests.get(URL + str(item),headers=header2)
        if cx % 15 == 0:
            print("GET RESPONSE!")
        textb.encoding = 'UTF-8'
        text = textb.json()
        #print(text)
        total=(text["rating"]["total"])
        #print(total)
        count = 2
        sum = 0
        while count <= 9:
                sum += count * (text["rating"]["count"][str(count)])
                #print(str(count) + " * " + str(text["rating"]["count"][str(count)]))
                count += 1
        rkd.append(round((sum/(total-text["rating"]["count"]["1"]-text["rating"]["count"]["10"]))*10000))
        #rkd.append(round((sum/(total))*10000))
count = 0
#print(rkd)
print("PROCESS 2")

for item in rkd:
        edrk[str(datar[count])+":"+datan[count]] = item
        count += 1
a1 = sorted(edrk.items(), key=lambda x: x[1], reverse=True)
for item in a1:
    print(str(item[0]) + " : " + str(item[1]))
#print(text)
