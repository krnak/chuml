import json
import hashlib
import smtplib
from email.mime.text import MIMEText
from flask import render_template, Blueprint, request

from chuml.utils import db

adresa = Blueprint('adresa', __name__,
	template_folder='templates',
	url_prefix="/adresa")

agipybot_passw = db.load_or_write("sensitive", "agipybot_passw")
jmeno = db.load_or_write("sensitive", "jmeno")
muj_email = db.load_or_write("sensitive", "email")
adresa_str = db.load_or_write("sensitive", "adresa")

whitelist = db.table("whitelist")

def hash(str):
	return hashlib.sha256(str.lower().encode("utf-8")).hexdigest()

def add_to_whitelist(email, level=1):
	whitelist[hash(email)] = level
	whitelist.commit()

def level_of(email):
	return whitelist.get(hash(email))

def send_adresa(email):
	try:
		db.log("Zasilam adresu na " + email)
		
		#msg = MIMEText(f"Má poštovní adresa je:\n{adresa}")
		msg = MIMEText("Má poštovní adresa je:\n" + adresa_str)
		#msg['Subject'] = f"{jmeno} - poštovní adresa"
		msg['Subject'] = jmeno + " - poštovní adresa"
		msg['From'] = 'agipybot@gmail.com'

		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.ehlo()
		server.login('agipybot@gmail.com', agipybot_passw)

		server.sendmail('agipybot@gmail.com', email, msg.as_string())
	except:
		#db.log(f"Posilani adresy na {email} selhalo.")
		db.log("Posilani adresy na {} selhalo.".format(email))

def send_zadost(email):
	try:
		db.log("Zasilam zadost od " + email)

		#msg = MIMEText(f"{email} žádá o poštovní adresu.")
		msg = MIMEText("{email} žádá o poštovní adresu.")
		msg['Subject'] = "[agiweb]: Žádost o poštovní adresu"
		msg['From'] = 'agipybot@gmail.com'

		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.ehlo()
		server.login('agipybot@gmail.com', agipybot_passw)

		server.sendmail('agipybot@gmail.com', muj_email, msg.as_string())
	except:
		#db.log(f"Posílani žádosti od {email} selhalo.")
		db.log("Posílani žádosti od {} selhalo.".format(email))

def vyrid_zadost(email):
	if level_of(email):
		send_adresa(email)
		return "Adresa zaslána na " + email
	else:
		send_zadost(email)
		return "Žádost o adresu zaslána na můj email."

@adresa.route("/",methods=['GET', 'POST'])
def adresa_query():
	if "email" in request.args:
		email = request.args.get("email")
		return vyrid_zadost(email)
	else:
		return render_template("adresa.html")
