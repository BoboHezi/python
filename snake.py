#coding:utf-8
from selenium import webdriver
import time

def find_sth(selector, delay):
	sth = None
	start = time.time();
	while sth == None and time.time() - start <= delay:
		select = driver.find_elements_by_css_selector(selector)
		if len(select) != 0:
			sth = select[0]
	return sth

url = 'http://10.20.40.21:8081/c/Freeme/platforms/android-25/ALPS-MP-N1.MP15-V1_DROI6758_66_N1_6758/project/droi_g1930epq/+/36205'
driver = webdriver.Chrome()
driver.get(url)

# sign in btn
signIn = find_sth('body > div.gwt-PopupPanel.errorDialog > div > div > div:nth-child(3) > button:nth-child(1)', 5)
if signIn == None:
	driver.close()
	driver.quit()
	exit()
print('click sign in btn')
signIn.click()

# name & password input
f_user = find_sth('#f_user', 5)
f_pass = find_sth('#f_pass', 5)

if f_user == None or f_pass == None:
	driver.close()
	driver.quit()
	exit()

print('input user & pwd')
f_user.send_keys('zhangzhanbo')
f_pass.send_keys('Elifli54321')

# sign in btn
b_signin = find_sth('#b_signin', 5)
if b_signin == None:
	driver.close()
	driver.quit()
	exit()
print('start sign in')
b_signin.click()

# new ui switch
# new_ui_btn = find_sth('#gerrit_btmmenu > a', 5)
# if new_ui_btn == None:
# 	driver.close()
# 	driver.quit()
# 	exit()
# print('switch new ui')
# new_ui_btn.click()

# project info
project_name = find_sth('#change_infoTable > tbody > tr:nth-child(6) > td > a.gwt-InlineHyperlink', 5)
if project_name != None:
	time.sleep(0.1)
	print('Project: ', project_name.text)

# download btn
dld_btn = find_sth('#gerrit_body > div > div > div > div > div > div.com-google-gerrit-client-change-ChangeScreen_BinderImpl_GenCss_style-headerLine > div.com-google-gerrit-client-change-ChangeScreen_BinderImpl_GenCss_style-statusRight > div.com-google-gerrit-client-change-ChangeScreen_BinderImpl_GenCss_style-popdown > button:nth-child(3)', 5)
if dld_btn == None:
	driver.close()
	driver.quit()
	exit()
time.sleep(0.1)
dld_btn.click()

# cherry pick
cp_input = find_sth('body > div.com-google-gerrit-client-change-ChangeScreen_BinderImpl_GenCss_style-replyBox > div > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > span', 5)
if cp_input == None:
	driver.close()
	driver.quit()
	exit()
print('cherry pick: ', cp_input.text)