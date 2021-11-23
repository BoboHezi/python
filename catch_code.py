from selenium import webdriver
from auto_cp import save_file
from os import getcwd
import time

def find_sth(driver, selector, delay):
	sth = None
	start = time.time();
	while sth == None and time.time() - start <= delay:
		select = driver.find_elements_by_css_selector(selector)
		if len(select) != 0:
			sth = select[0]
	return sth

def open(url):
	driver = webdriver.Chrome()
	driver.get(url)
	return driver

def dump_file_objs(driver, url):
	folders_container = find_sth(driver, '#cdk-accordion-child-0 > div > file-list > grid-layout', 5).find_elements_by_class_name('file-list-item')
	folders = {}
	print('folders:')
	for folder in folders_container:
		print('\t' + folder.text)
		folders[folder.text] = folder
	# print(folders)

	files_container = find_sth(driver, '#cdk-accordion-child-1 > div > file-list > grid-layout', 5).find_elements_by_class_name('file-list-item')
	files = {}
	print('files:')
	for file in files_container:
		print('\t' + file.text)
		files[file.text] = file
	# print(files)

	return files,folders

if ( __name__ == "__main__"):
	url = 'https://cs.android.com/android/platform/superproject/+/master:build/bazel'
	driver = open(url)
	rst = dump_file_objs(driver, url)

	base = getcwd() + '\\build\\bazel'

	for file in rst[0]:
		# rst[0].get(file).click()
		new_driver = open(url + '/' + file)
		print('\nfile %s: ' % file)
		raw_html = find_sth(new_driver, 'body > oss-app > div > div > repository-browser > browse-repository-contents > repository-detail > div > div > file-detail > main', 5)
		print('content\n%s' % raw_html.text)
		path = ('%s\\%s' % (base, file))
		save_file(raw_html.text, path)
		# driver.back()
		new_driver.close()
