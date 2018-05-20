import requests
import lxml.html
import sys
import os

login_url = 'https://intranet.hbtn.io/auth/sign_in'
request_url = sys.argv[1]

s = requests.session()          # start new session
login = s.get(login_url)        # get html
login_html = lxml.html.fromstring(login.text) # reformat url into list
hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]') # get all necessary hidden inputs
form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs} # put them into dictionary

form['user[login]'] = os.environ['HOLB_USERNAME'] # username (make sure env variable is set)
form['user[password]'] = os.environ['HOLB_PASS']  # password (make sure env variable is set)
response = s.post(login_url, data=form)  # login to holberton intranet

page = s.get(request_url)  # now that we're logged in, get the url we really want
with open("example_intranet_page.html", 'w') as f:
    f.write(page.text)
