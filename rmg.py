import requests
import lxml.html
import html2text

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

page = s.get(request_url)       # get the url we really want
page_html = lxml.html.fromstring(page.text) # turn it into lxml html

# headers = page_html.xpath(r'//div[@class=" clearfix gap"]/h4[@class="task"]') # get all the header names
# for elem in headers:
#     print("######")
#     print(lxml.html.tostring(elem, pretty_print=True))
# headers = [x.strip(' \t\n\r') for x in headers] # remove spaces and extra lines
# headers = filter(None, headers) # filter out blank entries    

desc =  page_html.xpath(r'//div[@class=" clearfix gap"]/h4[@class="task"]|//div[@class=" clearfix gap"]/p|//div[@class=" clearfix gap"]/pre|//div[@class=" clearfix gap"]/ul') # get all the relevant values from the descriptions
readme_html = open('README.html', 'w')
for elem in desc:
    readme_html.write(lxml.html.tostring(elem, pretty_print=True))
readme_html.close()

readme_html = open('README.html', 'r').read()
readme = open('README.md_g', 'w')
text_maker = html2text.HTML2Text()
# text_maker.mark_code = True

readme.write(text_maker.handle(readme_html).encode('utf-8'))
readme.close()
# print desc
