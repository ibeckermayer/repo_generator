import requests
import lxml.html
import sys
import os
import glob
import repo_gen_utils as rgu

login_url = 'https://intranet.hbtn.io/auth/sign_in'
request_url = sys.argv[1]

s = requests.session()          # start new session
login = s.get(login_url)        # get html
login_html = lxml.html.fromstring(login.text)  # reformat url into list
hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')  # get all necessary hidden inputs
form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}  # put them into dictionary

form['user[login]'] = os.environ['HOLB_USERNAME']  # username (make sure env variable is set)
form['user[password]'] = os.environ['HOLB_PASS']  # password (make sure env variable is set)
response = s.post(login_url, data=form)  # login to holberton intranet

page = s.get(request_url)  # now that we're logged in, get the url we really want
root = lxml.html.fromstring(page.text)  # turn it into lxml html

# find and make the directory:
directory = root.xpath("//ul/li[contains(., 'Directory:')]/code")[0].text.strip()
try:
    os.mkdir(directory)
except FileExistsError as e:
    print("[WARNING]: Directory already exists")

# change to directory
os.chdir(directory)

# find and make all files and directories to be graded
files = root.xpath("//ul/li[contains(., 'File:')]/code")
for f in files:
    rgu.file_handle(f.text.strip())

# get code snippets with files displayed by cat
code_snippets = root.xpath("//pre/code[contains(., 'cat')]")
for snippet in code_snippets:
    rgu.snippet_handle(snippet.text)

# make all the main files executable
for f in glob.glob("*main.py"):
    os.chmod(f, 0o764)

rgu.generate_readme(sys.argv[1])
