import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from robobrowser import RoboBrowser
import smtplib
import logging
import local_config
import random

LiveDomainBoxList = {"COM_hotmail":"hotmail.com",
	"COM_outlook":"outlook.com", 
	"DE_outlook":"outlook.de"}

first = ("Super", "Retarded", "Great", "Sexy", "Vegan", "Brave", "Shy", "Cool", "Poor", "Rich", "Fast", "Gummy", "Yummy", "Masked", "Unusual", "American", "Bisexual", "MLG", "Mlg", "lil", "Lil")
second = ("Coder", "Vegan", "Man", "Hacker", "Horse", "Bear", "Goat", "Goblin", "Learner", "Killer", "Woman", "Programmer", "Spy", "Stalker", "Spooderman", "Carrot", "Goat", "Quickscoper", "Quickscoper")

if __name__ == "__main__":
	print("Start")
	start_url = "https://signup.live.com/signup?"

	browser = RoboBrowser()
	browser.open(start_url)
	form = browser.get_form()
	name = (random.choice(first) + "_" + random.choice(second) + str(random.randint(1,100)) + str(random.randint(1,100))+ str(random.randint(1,100)))

	form['MemberName'].value = name
	form['LiveDomainBoxList'].option = LiveDomainBoxList.get("DE_outlook")

	print(name + "@" + LiveDomainBoxList.get("COM_hotmail"))

	browser.submit_form(form)

	src = str(browser.parsed())
	soup = BeautifulSoup(src, 'html.parser')
	print(soup)