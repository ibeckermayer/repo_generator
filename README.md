# README_generator
Generate README's for Holberton projects

## Setup
Make sure you have python installed. Consider using a [virtualenv](http://exponential.io/blog/2015/02/10/install-virtualenv-and-virtualenvwrapper-on-mac-os-x/)

Make sure you have [pip](https://www.liquidweb.com/kb/how-to-install-pip-on-ubuntu-14-04-lts/) installed

Finally, run `pip install -r requirements.txt` in your shell to get all the required python packages

## Usage
Create the environment variables `HOLB_USERNAME` and `HOLB_PASS` to refer to your holberton intranet username and password respectively. If you plan to use this script repeatedly, it's a good idea to put these definitions in you .bashrc:

```
export HOLB_USERNAME='username'
export HOLB_PASS='password'
```

Run the script as follows:
```
python rmg.py [url]
```
substiting [url] with the url of the target project's page

## Output
The script will output a file called *README.md_generated* which you can then use as your README for the project
