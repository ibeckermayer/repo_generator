import requests, lxml.html, html2text, fileinput, sys, os

# ignore warnings
import warnings
warnings.filterwarnings("ignore")

OUTPUT_FILE_NAME = 'README.md_generated'

login_url = 'https://intranet.hbtn.io/auth/sign_in'
request_url = sys.argv[1]

s = requests.session()          # start new session
login = s.get(login_url)        # get html
login_html = lxml.html.fromstring(login.text) # reformat url into list
hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]') # get all necessary hidden inputs
form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs} # put them into dictionary

form['user[login]'] = os.environ['HOLB_USERNAME'] # username (make sure env variable is set)
form['user[password]'] = os.environ['HOLB_PASS']  # password (make sure env variable is set)
response = s.post(login_url, data=form) #login to holberton intranet

page = s.get(request_url)       # now that we're logged in, get the url we really want
page_html = lxml.html.fromstring(page.text) # turn it into lxml html

# get all the relevant values from the descriptions
desc =  page_html.xpath(r'//div[@class=" clearfix gap"]/h4[@class="task"]|//div[@class=" clearfix gap"]/p|//div[@class=" clearfix gap"]/pre|//div[@class=" clearfix gap"]/ul') 

readme_html_ = open('README.html_', 'w') # create temporary html file
from lxml.html.clean import Cleaner 
cleaner = Cleaner(kill_tags=['span']) 
for elem in desc:
    elem = cleaner.clean_html(elem) # kills <span> mandatory </span> or <span> advanced <span>
    readme_html_.write(lxml.html.tostring(elem, pretty_print=True)) # write to file
readme_html_.close()

# replace h4 with h2 (this looks nicer)
readme_html_ = open('README.html_')
readme_html = open('README.html', 'w') # final html file
for s in readme_html_.xreadlines():
    readme_html.write(s.replace('h4','h2'))
readme_html_.close()
readme_html.close()

# convert html to markdown
readme_html = open('README.html', 'r').read()
readme = open(OUTPUT_FILE_NAME, 'w')
text_maker = html2text.HTML2Text()
readme.write(text_maker.handle(readme_html).encode('utf-8'))
readme.close()

# remove tmp files
os.remove('README.html')
os.remove('README.html_')

# output file called OUTPUT_FILE_NAME
