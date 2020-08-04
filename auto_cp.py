#coding:utf-8
import urllib.request
import re
from io import BytesIO
import gzip
from bs4 import BeautifulSoup

host = 'http://10.20.40.21:8081'
targets = ['/c/Freeme/platforms/android-25/ALPS-MP-N1.MP15-V1_DROI6758_66_N1_6758/project/droi_g1930epq/+/34969']

first_header = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
	'Connection': 'keep-alive',
	'Cookie': 'GERRIT_UI=POLYGERRIT; GerritAccount=aScfprrjhuIFfB4kC.yOOjraPh0aNhFIRG; XSRF_TOKEN=aScfprtcaN3KOsqrusVkfbZuLlWl37hGea',
	'Host': '10.20.40.21:8081',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
}

gr_app = {
	'Accept': '*/*',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
	'Connection': 'keep-alive',
	'Cookie': 'GERRIT_UI=POLYGERRIT; GerritAccount=aScfprrjhuIFfB4kC.yOOjraPh0aNhFIRG; XSRF_TOKEN=aScfprtcaN3KOsqrusVkfbZuLlWl37hGea',
	'Host': '10.20.40.21:8081',
	'If-Modified-Since': 'Tue, 12 Nov 2019 10:52:50 GMT',
	'Origin': 'http://10.20.40.21:8081',
	'Referer': 'http://10.20.40.21:8081/c/Freeme/platforms/android-25/ALPS-MP-N1.MP15-V1_DROI6758_66_N1_6758/project/droi_g1930epq/+/34969',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
}

def add_header(request, headers):
	for key in list(headers.keys()):
		request.add_header(key, headers.get(key))

def save_file(raw, file):
	with open (file, 'w') as file_object:
		file_object.write(raw)

def request(url, header, codec):
	# print('request: ', url)
	request = urllib.request.Request(url)
	if header != None:
		add_header(request, header)
	response = urllib.request.urlopen(request)
	encode = response.info().get('Content-Encoding')
	html_raw = response.read()
	# print('status\t', response.status)

	if encode == 'gzip':
		buff = BytesIO(html_raw)
		f = gzip.GzipFile(fileobj=buff)
		html_raw = f.read() if codec == '' else f.read().decode(codec)
		return html_raw
	elif codec != '':
		html_raw = html_raw.decode(codec)

	return html_raw

def html_2_soup(raw):
	return BeautifulSoup(raw, 'html.parser')

first_soup = html_2_soup(request(host + targets[0], first_header, 'utf8'))

for link in first_soup.find_all('link'):
	target = link.get('href')
	
	if 'gr-app.html' in target:
		link_url = host + target
		second_html = request(link_url, gr_app, 'utf8')

		# save_file(second_html, 'gr-app.html')
		print(second_html)