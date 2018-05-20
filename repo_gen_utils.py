import re
import os
import requests
from lxml import html


def file_handle(f):
    # split into list of individual files
    files = re.split(r'[,]', f)
    for fi in files:

        # split into list of directories follow by file
        dirs_and_file = re.split(r'[/]', fi)

        # make any necessary directories
        for directory in dirs_and_file[:-1]:
            try:
                os.mkdir(directory.strip())
            except FileExistsError:
                pass

        # now make all the files
        try:
            os.mknod(fi.strip())
        except FileExistsError:
            pass


def snippet_handle(s):
    l = 0
    lines = s.splitlines()
    # code.interact(local=locals())
    while l < len(lines):
        words = re.split(r'[ ]', lines[l])
        i = 0
        while i < len(words):
            if words[i] == "cat":
                i+=1
                l+=1
                if i < len(words):
                    while words[i][0] == "-":  # skip options
                        i+=1
                    filename = words[i]
                    try:            # make the file
                        os.mknod(filename.strip())
                    except FileExistsError:
                        pass
                    while l < len(lines):  # continue down line by line
                        if '@' not in lines[l] and '$' not in lines[l]:
                            with open(filename, 'a') as f:
                                f.write(lines[l] + '\n')
                            l+=1
                        else:
                            break
                    break
            else:
                i+=1
        l+=1



def generate_readme(webpage=''):
    LOGIN_URL = "https://intranet.hbtn.io/auth/sign_in"
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
