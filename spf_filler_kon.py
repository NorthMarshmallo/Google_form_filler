import requests
from bs4 import BeautifulSoup
import re

beg_url = input()
url = beg_url

if 'vk.cc' in beg_url:
    beg_page = requests.get(beg_url)
    print(beg_page.text)

    url = re.findall(r"URL='[^']+'", beg_page.text, flags=re.S)[0][5:-1]

print(url)
if 'forms.gle' in url:
    GoogleURL = requests.head(url).headers['location'].rsplit('/', 1)[0]
else:
    GoogleURL = url.rsplit('/', 1)[0]
print(GoogleURL)

page = requests.get(url)
print(page.content)
soup = BeautifulSoup(page.text, 'lxml')
print(soup)

urlResponse = GoogleURL + '/formResponse'
urlReferer = GoogleURL + '/viewform'

x = input()

infos = [['command name',
        'song name',
        'city name',
        'team size',
        'members',
        'Нет',
        'Нет',
        'reference']
        ]

if x == '1':
    infos = infos[:1]

match = re.findall('(?<=\[\[)(\d+)', re.search(r'FB_PUBLIC_LOAD_DATA_ = (.*);', ''.join(list(page.text)), flags=re.S).group(1))
# (?<= ) means to look for the following (but not include it in the results):
# \[\[ means find 2 square brackets characters. The backslash is used to tell regex to use the character [ and not the function.
# (\d+) means to match the start of a digit of any size (and return it in results)

print(match)

for info in infos:
    results = ['entry.' + x for x in match[1:] if len(x)>5] # Skip the first item, which is 831400739
    results = results[:len(info)]

    print(results)
    form_data = {v: info[i] for i, v in enumerate(results)}

    user_agent = {'Referer': urlReferer,
               'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36"}
    r = requests.post(urlResponse, data=form_data, headers=user_agent)