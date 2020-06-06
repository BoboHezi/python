import urllib.request
import re
# import PyV8
# import execjs
from bs4 import BeautifulSoup

host = 'http://10.20.40.21:8081'
targets = ['/c/Freeme/platforms/android-25/ALPS-MP-N1.MP15-V1_DROI6758_66_N1_6758/project/droi_g1930epq/+/34969']

first_header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
	'Cache-Control': 'max-age=0',
	'Connection': 'keep-alive',
	'Cookie': 'GERRIT_UI=POLYGERRIT; GerritAccount=aScfprqTXx44dBi0lQGNRL-I5aDZuqVaYq; XSRF_TOKEN=aScfprsO1aGOedB64gHvQIilydlDgHUgIa',
	'Host': '10.20.40.21:8081',
	'Referer': 'http://10.20.40.21:8081/dashboard/self',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
}

def add_header(request, headers):
	for key in list(headers.keys()):
		request.add_header(key, first_header.get(key))

def save_file(raw, file):
	with open (file, 'w') as file_object:
		file_object.write(raw)

def request(url, header, codec):
	request = urllib.request.Request(url)
	add_header(request, header)
	response = urllib.request.urlopen(request)
	
	html_raw = ''
	if codec == '':
		html_raw = response.read()
	else:
		html_raw = response.read().decode(codec)
	# print('response code', response.getcode())
	return html_raw

def html_2_soup(raw):
	return BeautifulSoup(raw, 'html.parser')

first_soup = html_2_soup(request(host + targets[0], first_header, 'utf8'))

for link in first_soup.find_all('link'):
	target = link.get('href')
	if 'gr-app' in target:
		link_url = host + target
		print(link_url)
		second_html = request(link_url, first_header, 'ISO-8859-1')
		# print(second_html)
		save_file(second_html, target.replace('/', '-') + '.html')