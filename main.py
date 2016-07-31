import urllib.request
import bs4
from bs4 import BeautifulSoup
import gzip

def http_request(url):
    # Build custom http header
    request = urllib.request.Request(url)
    request.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
    request.add_header("Accept", "*/*")
    request.add_header("Accept-Encoding", "gzip, deflate, sdch")
    request.add_header("Accept-Language", "en,zh-CN;q=0.8,zh;q=0.6")

    # Get http response
    response = None

    try:
        response = urllib.request.urlopen(request)

    except urllib.request.HTTPError as e:
        printf("Error code: {}".format(e.code))
    
    except Exception as e:
        printf("Network error occurs: ", e)
    
    return response

def get_content(r):
    video_clip_list = list()
    url = "http://www.ttmeiju.com/meiju/Greys.Anatomy.html?page={}"

    for i in r:
        # fetch content from web
        response_byte = http_request(url.format(i)).read()
        response_decompressed = gzip.decompress(response_byte)
        response_decoded = response_decompressed.decode('gbk')


        # start parsing web content
        parsed = BeautifulSoup(response_decoded, 'html.parser')

        div_group = parsed.find('div', {'class': 'seedlistdiv'})
        table = div_group.find('table', {'class': 'seedtable'})

        tr_group = table.find_all('tr', {'class': 'Scontent'})

        for tr in tr_group:
            rows = tr.find_all('td')

            title = rows[1].get_text().strip()

            magnet = rows[2].find('a', {'title': '磁力链高清美剧下载'}).attrs['href']

            size = rows[3].get_text()

            video_format = rows[4].get_text()

            video_clip = dict()
            video_clip['title'] = title
            video_clip['magnet'] = magnet
            video_clip['size'] = size
            video_clip['format'] = video_format

            video_clip_list.append(video_clip)

    return video_clip_list

clip_list = get_content(range(0, 2))

for clip in clip_list:
    print('Title:', clip['title'])
    print('Magnet:', clip['magnet'])
    print('Size:', clip['size'])
    print('Format:', clip['format'])
    print()
    