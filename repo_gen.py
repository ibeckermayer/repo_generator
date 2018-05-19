import requests
import lxml.html
import html2text
import sys
import os
import traceback
import repo_gen_utils as rgu

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
root = lxml.html.fromstring(page.text)  # turn it into lxml html

# make a temporary directory
# os.mkdir("tmp")

# find and make the directory:
directory = root.xpath("//ul/li[contains(., 'Directory:')]/code")[0].text.strip()
try:
    os.mkdir(directory)
except FileExistsError as e:
    print("[WARNING]: Directory already exists")

os.chdir(directory)             # change to directory

# find and make files to be graded
files = root.xpath("//ul/li[contains(., 'File:')]/code")

# make all the graded files and necessary directories
for f in files:
    rgu.file_handle(f.text.strip())


# get all the relevant values from the descriptions
#desc =  page_html.xpath(r'//div[@class=" clearfix gap"]/h4[@class="task"]|//div[@class=" clearfix gap"]/p|//div[@class=" clearfix gap"]/pre|//div[@class=" clearfix gap"]/ul')
# desc =  page_html.xpath(r'//div[@class=" clearfix gap"]/h4[@class="task"]')

# readme_html_ = open('README.html_', 'wb') # create temporary html file
# from lxml.html.clean import Cleaner
# cleaner = Cleaner(kill_tags=['span'])
# for elem in desc:
#     elem = cleaner.clean_html(elem) # kills <span> mandatory </span> or <span> advanced <span>
    # readme_html_.write(lxml.html.tostring(elem, pretty_print=True)) # write to file
#     readme_html_.write(lxml.html.tostring(elem, pretty_print=True))
# readme_html_.close()

# replace h4 with h2 (this looks nicer)
# readme_html_ = open('README.html_')
# readme_html = open('README.html', 'w') # final html file
# for s in readme_html_.xreadlines():
#     readme_html.write(s.replace('h4','h2'))
# readme_html_.close()
# readme_html.close()

# convert html to markdown
# readme_html = open('README.html', 'r').read()
# readme = open(OUTPUT_FILE_NAME, 'w')
# text_maker = html2text.HTML2Text()
# text_maker.mark_code = True
# readme.write(text_maker.handle(readme_html).encode('utf-8'))
# readme.close()

# # remove tmp files
# os.remove('README.html')
# os.remove('README.html_')

# output file called OUTPUT_FILE_NAME
