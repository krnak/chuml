import selenium
import selenium.webdriver #some __init__.py fail in selenium
from selenium.common.exceptions import NoSuchElementException, InvalidElementStateException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import http
import json
import urllib
import sys
import requests

url = None
# load
def load():
	for elem in d.find_elements_by_xpath(
		'//div[@title="Collapse Post"]'):
		# len("javascript:") == 11
		command = elem.get_attribute("onclick")[11:]
		d.execute_script(command)

# read mesages
def messages():
	msgs = []
	levels = 100*[None]

	for elem in d.find_elements_by_xpath(
		'//div[@class="message-wrapper-inner"]/..'):
		iid = elem.get_attribute("id")
		name = elem.find_element_by_xpath(
			'.//span[@class="profileCardAvatarThumb"]').text
		try:
			text = elem.find_element_by_xpath(
				'.//div[@class="vtbegenerated"]'
				).get_attribute('innerHTML')
		except selenium.common.exceptions.NoSuchElementException:
			text = ""

		time = int(
			elem.find_element_by_xpath(
			'.//span[@postedtimeinmillis]'
			).get_attribute("postedtimeinmillis"))

		lvl = int("".join(
			[i for i in elem.get_attribute("class")
				   if i.isdigit()]))

		levels[lvl] = iid
		if lvl > 0:
			prev = levels[lvl - 1]
		else:
			prev = None


		msgs.append({
			"id"  : iid,
			"name": name,
			"text": text,
			"time": time,
			"prev": prev,
			"repl": url + '#' + iid
		})

	return msgs


if __name__ == "__main__":
	d = selenium.webdriver.Firefox()
	d.get("https://toledo.kuleuven.be/")

	url = input("Insert url after login: ")
	secret = input("Secret:")
	d.get(url)

	ids = set()

	while True:
		print("refresh")
		d.refresh()
		sleep(2)

		print("load")
		load()
		sleep(6)

		print("read")
		msgs = messages()

		for m in msgs:
			if not m["id"] in ids:
				print("====== NEW POST ======")
				for k, v in m.items():
					print(k, ":", v)
				ids.add(m["id"])
				requests.post("https://flask.krnak.cz/forum/feed",
					json=m, params={"secret":secret})
