import os, requests, time, pyautogui, random, pickle, csv
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
options.add_experimental_option("prefs", { "download.default_directory": r"E:\Data\_similarweb\0_sw\0_selenium_app_data"})

driver = webdriver.Chrome(service = Service("./chromedriver.exe"), options=options)

driver.set_window_position(800, -1000)
driver.set_window_size(850, 600)

actions = ActionChains(driver) 

# Replace with your credentials
username = "your_email@example.com"
password = "your_password"

states={
	"united states" :"840",
	"california" :"8406",
	"new york" :"84036",
	"virginia" :"84051"
}

sources = ["all traffic", "desktop", "mobile web"]

duration_checked = False

def save_cookies():
	pickle.dump(driver.get_cookies(), open("cookies.pkl","wb"))

def load_cookies():
	cookies = pickle.load(open("cookies.pkl", "rb"))
	for cookie in cookies:
		driver.add_cookie(cookie)

def zoom_out():
	pyautogui.keyDown("ctrl")
	pyautogui.press("-")
	pyautogui.keyUp("ctrl")

def click_element(selector):
	print("auto_sw: click_element: selector: ", selector)
	driver.find_element(By.CSS_SELECTOR, selector).click()
	time.sleep(2)

def key_entry(key_value):
	actions = ActionChains(driver) 
	actions.send_keys(key_value)
	actions.perform()

def type_input(string_value):
	for character in string_value:
		key_speed = random.uniform(1/6.8, 1/8.0)
		if character == "." or character == "@" or character.isdigit():
			key_speed = random.uniform(1/5.04, 1/6.5)
		print("auto_sw: login: key_speed: ", key_speed)
		print("auto_sw: login: character: ", character)
		key_entry(character)
		time.sleep(key_speed)

def login():
	###################################
	click_element("#input-email")
	type_input(username)
	key_entry(Keys.TAB)
	type_input(password)
	key_entry(Keys.ENTER)
	###################################

def get_page(url):
	driver.get(url)
	time.sleep(1)
	a = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
	return a

def click_country_dropdown(new_state):
	print("auto_sw: click_country_dropdown: new_state: ", new_state)
	driver.find_element_by_css_selector(".DropdownButton--filtersBarDropdownButton--country").click()
	time.sleep(1)
	click_element(".DropdownContent-search")
	time.sleep(1)
	type_input(new_state)
	time.sleep(1)
	dropdown_items = driver.find_elements_by_css_selector('[data-automation="country-text"]')
	print("auto_sw: click_country_dropdown: dropdown_items: ", dropdown_items)
	for a in dropdown_items:
		try:
			if a.text.lower() == new_state.lower():
				a.click()
				print("auto_sw: click_country_dropdown: a: ", a)
		except:
			print("!!! auto_sw: click_country_dropdown: a: failed !!!")
			pass

def click_websource_dropdown(websource):
	country_dropdown = driver.find_element_by_css_selector(".WebSourceFilter-dropdownButton").click()
	time.sleep(1)
	dropdown_items = driver.find_elements_by_css_selector(".WebSourceDropdownItem")
	for a in dropdown_items:
		try:
			if a.text.lower() == websource.lower():
				a.click()
				print("auto_sw: click_websource_dropdown: a: ", a)
		except:
			print("!!! auto_sw: click_websource_dropdown: a: failed !!!")
			pass

def wait_main_page():
	main_loaded = False
	while main_loaded == False:
		greeting_text = driver.find_elements(By.CSS_SELECTOR, "div")
		for div in greeting_text:
			try:
				if div.text == "Hi User" or "Hi, Welcome to Similarweb" in div.text:
					main_loaded = True
					print("auto_sw: wait_main_page: div.text: ", div.text)
					time.sleep(1)
			except:
				pass

def wait_website(website_url):
	main_loaded = False
	while main_loaded == False:
		greeting_text = driver.find_elements(By.CSS_SELECTOR, ".wwo-widgets span")
		for div in greeting_text:
			time.sleep(2)
			try:
				if str(website_url) in div.text:
					main_loaded = True
					print("auto_sw: wait_website: div.text: ", div.text)
					print("auto_sw: wait_website: div.text: fuckkkkkkkkkk")
					return
			except:
				pass

def cycle_websource(timewait):
	for z in sources:
		time.sleep(timewait)
		click_websource_dropdown(z)
	
def cycle_menu(active_state):
	global duration_checked
	# 1 download for channel traffic = 5 seconds after clicking
	click_element('[data-automation-item="analysis.traffic.engagement.title"]')
	
	if duration_checked == False:	
		time.sleep(3)
		duration_select()
		time.sleep(1)
		click_apply()
		duration_checked = True

	if active_state == "united states":
		cycle_websource(3)
	time.sleep(3)
	
	# 1 download for channel traffic = 2 seconds after clicking
	# 1 download for traffic sources = 15 seconds after clicking
	click_element('[data-automation-item="analysis.traffic.marketing.channels.title"]')
	if active_state == "united states":
		cycle_websource(3)
	time.sleep(3)

	# 1 download for audience interests = 25-30 seconds after clicking
	# LONG TIME TO LOAD PAGE
	click_element('[data-automation-item="analysis.audience.interests.title"]')
	if active_state == "united states":
		cycle_websource(10)
	time.sleep(10)

def duration_select():
	duration_dropdown = driver.find_elements_by_css_selector(".DropdownButton--filtersBarDropdownButton")
	for a in duration_dropdown:
		if "months" in a.text.lower() and "12 months" not in a.text.lower():
			a.click()
			time.sleep(2)
			month_buttons = driver.find_elements_by_css_selector("#calendar-presets-container div div")
			for b in month_buttons:
				if "last 12 months" in b.text.lower():
					print("auto_sw: duration_select: b.text.lower(): ", b.text.lower())
					b.click()

def click_apply():
	time.sleep(1)
	try:
		apply_button = driver.find_element_by_css_selector(".DurationSelector-container .DurationSelector-action-submit")
		apply_button.click()
	except:
		pass

def check_sites(site_list):
	###################################
	for a, b in enumerate(site_list):
		###################################
		if a == 0:
			###################################
			click_element(".input-container")
			type_input(b)
			time.sleep(1)
			click_element(".ListItemWebsite")
			###################################
		else:
			###################################
			try:
				click_element('[data-automation="query-bar-item-text"]')
			except:
				pass			
			###################################
			try:
				click_element('[data-automation="query-bar-item-text"]')
			except:
				pass
			###################################
			type_input(b)
			time.sleep(1)
			key_entry(Keys.ENTER)
			key_entry(Keys.ENTER)
			time.sleep(1)
			click_element('[data-automation-item="analysis.overview.performance.title"]')
			###################################
		###################################
		time.sleep(2)
		wait_website(b)
		print("auto_sw: wait_website: PASSED")
		###################################
		for x in states:
			###################################
			print("auto_sw: check_sites: x: ", x)
			###################################
			time.sleep(3)
			click_country_dropdown(x)
			time.sleep(3)
			###################################
			cycle_menu(x)
			###################################

		# 1 download for demographics = 2 seconds after clicking
		# NO STATES
		click_element('[data-automation-item="analysis.audience.demo.title"]')
		time.sleep(3)
		cycle_websource(3)
		time.sleep(3)
		time.sleep(3)

def init_manual():
	###################################
	login_url = "https://pro.similarweb.com/"
	get_page(login_url)
	###################################
	zoom_out()
	zoom_out()
	zoom_out()
	###################################
	login()
	###################################
	wait_main_page()
	###################################
	time.sleep(1)
	zoom_out()
	time.sleep(0.15)
	zoom_out()
	time.sleep(0.15)
	zoom_out()
	time.sleep(1)
	###################################
	# Example site list
	site_list = ["example.com", "example.org"]
	check_sites(site_list)
	###################################

def get_files(url):
	driver.execute_script("window.open('');")
	time.sleep(0.5)
	driver.switch_to.window(driver.window_handles[1])
	time.sleep(0.5)
	print("auto_sw: get_files: url: ", str(url))
	driver.get(url)
	time.sleep(0.5)
	driver.close()
	driver.switch_to.window(driver.window_handles[0])

def get_ids(filename):
	a = open(filename+".csv", "r", encoding="utf-8", newline="", errors="ignore")
	b = csv.reader(a)
	c = [c[0] for c in b]
	a.close()
	return c

def download_app_files(app_list):
	###################################
	sleep_from = 0.3
	sleep_to = 1.25
	###################################
	for a, b in enumerate(app_list):
		###################################
		print("auto_sw: wait_website: PASSED")
		###################################
		print("download_app_files: Store Downloads: ", )
		get_files("https://pro.similarweb.com/api/AppAnnie/StoreDownloads/Excel?%23&changedDuration=true&country=999&device=Total&from=2021%7C12%7C01&isWindow=false&keys="+str(b)+"&store=google&to=2023%7C02%7C28")
		time.sleep(random.uniform(sleep_from, sleep_to))

		print("download_app_files: "+str(b)+": INSTALL BASE")
		get_files("https://pro.similarweb.com/api/AppAnnie/InstallBase/Graph/Excel?%23&country=840&device=Combined&from=2021%7C12%7C01&keys="+str(b)+"&store=google&to=2023%7C02%7C28")
		time.sleep(random.uniform(sleep_from, sleep_to))
		
		print("download_app_files: "+str(b)+": INSTALL BASE GROWTH")
		get_files("https://pro.similarweb.com/api/AppAnnie/InstallBase/Delta/Excel?%23&country=840&device=total&from=2022%7C02%7C01&keys="+str(b)+"&store=google&to=2023%7C02%7C28")
		time.sleep(random.uniform(sleep_from, sleep_to))

		print("download_app_files: "+str(b)+": MONTHLY ACTIVE USERS (MAU) and OPEN RATE")
		get_files("https://pro.similarweb.com/api/AppAnnie/Engagement/Mau/Excel?country=840&from=2021%7C12%7C01&to=2023%7C02%7C28&keys="+str(b)+"&store=google&timeGranularity=Monthly&isWindow=false&device=Combined")
		time.sleep(random.uniform(sleep_from, sleep_to))

		print("download_app_files: "+str(b)+": TOTAL SESSIONS")
		get_files("https://pro.similarweb.com/api/AppAnnie/Engagement/Excel?country=840&from=2021%7C12%7C01&to=2023%7C02%7C28&keys="+str(b)+"&store=google&timeGranularity=Monthly&isWindow=false&device=Combined")
		time.sleep(random.uniform(sleep_from, sleep_to))
		
		print("download_app_files: "+str(b)+": RETENTION")
		get_files("https://pro.similarweb.com/api/AppAnnie/Retention/OverTimePerDayExcel?%23&country=840&device=Total&from=2021%7C12%7C01&keys="+str(b)+"&store=google&to=2023%7C02%7C28")
		time.sleep(random.uniform(sleep_from, sleep_to))
		
		print("download_app_files: "+str(b)+": DEMOGRAPHICS")
		get_files("https://pro.similarweb.com/api/AppAnnie/AppDemographics/appsAndCategories/Excel?country=840&from=2021%7C12%7C01&includeSubDomains=true&isWindow=false&keys="+str(b)+"&store=google&timeGranularity=Monthly&to=2023%7C02%7C28")
		time.sleep(random.uniform(sleep_from, sleep_to))

def init_headless():
	###################################
	login_url = "https://pro.similarweb.com/"
	get_page(login_url)
	###################################
	login()
	###################################
	wait_main_page()
	###################################
	time.sleep(1)
	###################################
	app_list = get_ids("add_ids_0403_similarwebscroll")
	print(app_list)
	download_app_files(app_list)
	###################################

init_headless()