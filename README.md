# repo_generator
generate directories for Holberton School repositories

## Setup
### Python Environment
This program is written and tested with `Python 3.4.3`
I manage my python environments using `virtualenv` and `virtualenvwrapper` so instructions will be written assuming you have those installed.
First set up a new environment and install the requirements:
```
mkvirtualenv repo_generator
pip install -r requirements.txt
```
if you choose not to use `virtualenv` and `virtualenvwrapper` then just run the `pip install` line above.
### Environment Variables
The best way I've found so far to avoid typing your intranet username and password each time the program runs is to set environment variables with your Holberton username and password. 
If anybody has suggestions for a better way to do this feel free to suggest it to me.

Add the following to your `.bashrc`:
```
export HOLB_USERNAME='<username>'
export HOLB_PASS='<password>'
```
### genrepo script
I wrote a script which I saved in `/usr/local/bin/genrepo` to run the script easily. 
It relies on this repository being in your home (`~`) directory.
Feel free to mess with this, and let me know if there's a better protocol for creating and using scripts in this way.
```
#!/bin/bash
source /usr/local/bin/virtualenvwrapper.sh
workon repo_generator
python ~/repo_generator/repo_gen.py $1
```
If you choose not to use `virtualenv` and `virtualenvwrapper` then the equivalent script is simply
```
#!/bin/bash
python ~/repo_generator/repo_gen.py $1
```
## Use
With everything set up correctly, usage is as simple as
```
genrepo <url>
```
with `<url>` being the url for the project you're generating i.e. `https://intranet.hbtn.io/projects/248`

Make sure you have completed the quiz before generating the repo or it won't know what to generate. 
If you want to also generate advanced tasks then unlock them manually before generating.
Careful about generating a folder you already have, as the program may overwrite your files. 
## Contribute
Please notify me of any bugs by creating an issue in this repository or messaging me on slack. If you want to make the program better by contributing feel free to message me on Slack or come talk to me about improvements. There also may be some issues already listed that you can work on solving if you're interested.
