#!/usr/bin/python3
import requests, os, html2text
from lxml import html

LOGIN_URL = "https://intranet.hbtn.io/auth/sign_in"

def generate_readme(webpage=''):
    session_requests = requests.session()

    # Get login authenticity token
    result = session_requests.get(LOGIN_URL)
    tree = html.fromstring(result.text)
    hidden_inputs = tree.xpath(r'//form//input[@type="hidden"]') # get all necessary hidden inputs
    form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs} # put them into dictionary
    form['user[login]'] = os.environ['HOLB_USERNAME'] # username (make sure env variable is set)
    form['user[password]'] = os.environ['HOLB_PASS']  # password (make sure env variable is set)


    # Perform login
    result = session_requests.post(LOGIN_URL, data = form, headers = dict(referer = LOGIN_URL))

    # Scrape Page
    result = session_requests.get(webpage)
    tree = html.fromstring(result.content)
    for elem in tree.xpath('//div[contains(@class, "clearfix gap")]/p[1]/code'):
        elem.drop_tag()
    project_title = tree.xpath('//h1/text()')[0]
    task_names = list(map(lambda x: x.strip(), tree.xpath('//h4[@class="task"]/text()')))
    task_names = [x  for x in task_names if x is not '']
    task_descriptions = tree.xpath('//div[contains(@class, "clearfix gap")]/p[1]/text()')
    task_constraints = tree.xpath('//div[contains(@class, "clearfix gap")]/ul[1]//text()')

    with open('README.md', 'w') as f:
        f.write("# " + project_title + '\n')
        for elem in zip(task_names, task_descriptions):
            f.write('## ' + elem[0] + '\n')
            f.write('***\n')
            f.write(elem[1] + '\n\n')

if __name__ == '__main__':
    import sys
    generate_readme(sys.argv[1])
