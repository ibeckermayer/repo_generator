import requests
import lxml.html

login_url = 'https://intranet.hbtn.io/auth/sign_in'
request_url = 'https://intranet.hbtn.io/projects/208'

s = requests.session()          # start new session
login = s.get(login_url)        # get html
login_html = lxml.html.fromstring(login.text) # reformat url into list
hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]') # get all necessary hidden inputs
form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs} # put them into dictionary

form['user[login]'] = '320' # username
form['user[password]'] = 'ar7AnbJn9sH#' #password
response = s.post(login_url, data=form)

page = s.get(request_url)

