# HuskyHunt
Providing a secure network for MTU students and the surrounding community to safely buy/sell items.
Similar to BarkBoard (now discontinued), and somewhat similar to Craigslist.

## Excluded Files
**All project files are now in the template, the previously excluded files have been added to the repository.**

# Setup Process:
## Prereqs
### Git needs to be setup
Follow the instructions in [this Doc](https://docs.google.com/document/d/1E2wAXAIfVQe39cs4nv5TfXGxbGzUXE5yun1oFoxynLc/edit).

Note: Please read and follow the Doc carefully to prevent potential data loss when you try to push, particularly Part 3!

When you're done with that, you'll have (pretty much) an empty HuskyHunt folder because you're defaulted into the master branch. Our codebase lives in the dev branch. To fix this:  
... 1: In the command line, go into your GitHub folder, then your HuskyHunt folder.  
... 2: Still in command line, run this command: git checkout dev  
... 3: You should now have the project files downloaded.  

### Python needs to be installed
Python should be installed, versions __Python 3.5 or later__
1. [Download Python](https://www.python.org/downloads/)
2. Add python to your system environment variables called **_PATH_**.  

_________________
**REALLY IMPORTANT PART OF PYTHON INSTALLATION PROCESS:**
... During installation, make sure to **check the bottom box** marked _Add Python 3.X to PATH_.
... ![alt text](https://docs.python.org/3/_images/win_installer.png "The bottom box")
_________________

... After this you should be able to open a command prompt and type __python__ and it will launch the interpreter.
3. Check to make sure both python works and it was added to PATH properly.  If you run the `python` command and it doens't recognize the command or says it's missing, the following instructions found [here](https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation) might help fill in the gaps.

... If the following fails, seek out help in _Slack_ or via _e-mail_ from one of your fellow team members.
```python
c:\>python --version
Python 3.6.6  

c:\>python
Python 3.6.6 (v3.6.6:4cf1f54eb7, Jun 27 2018, 03:37:03) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import platform
>>> platform.python_version()
'3.6.6'
>>> exit()
```
_If you're using python 3.5+ you will be fine_

### PIP needs to be installed
Pip is pythons way to manage packages (installing and removing modules like _django_)
1. Make sure _pip_ works by running the `pip -V` or `pip --version` command.
2. Pip will likely require an initial update which can be done with `pip install --upgrade pip`.
3. You can check what is installed with pip using `pip list`.
```
C:\>pip list
Package    Version
---------- -------
Django     2.1.1
pip        18.1
pytz       2018.5
setuptools 39.0.1
virtualenv 16.0.0
```

[//]: # (<#### MySQL Client is required to connect to the database>)

[//]: # (Long and short of this is that the mysqlclient module for python is extremely particular so make sure you install the correct version:)

[//]: # (**`pip install mysqlclient==1.3.12`**)

### Django needs to be installed
1. Using _pip_, you will need to install __Django__.
... You can do this with `pip install django`. 

[//]: # (**Be aware that the version matters [Django 2.1.1]**)

[//]: # (... To specify the version you can use `pip install django==2.1.1`.)

2. Similarly, use pip to install __Pillow__.
... Run `pip install pillow` in command line.

3. Run the local server.  
... Using the command line, cd into GitHub/HuskyHunt/mainsite.  
... Also in command line, run `python manage.py runserver`.  
... Attempt to go to localhost:8000 in your web browser.  
You should see the HuskyHunt homepage. Done  
  
4. **_There is no shortcut to learning, only to do_** so I would recommend going through Django's expansive documentation.  
... Start with the [Tutorial](https://docs.djangoproject.com/en/2.1/intro/install/) section to get a feel of how it works which will walk you through setting up a _polls app_. **Read through it carefully, and don't skip any steps.**

Here is a tutorial video to help visual how Django concepts and structure.  _Sentdex_ is a great python programmer and has a variety of tutorials on topics from beginners to the more advanced, but be aware some of these are related to older versions of python or django:
https://www.youtube.com/embed/FNQxxpM1yOs?list=PLQVvvaa0QuDeA05ZouE4OzDYLHY-XH-Nd

### Knowing where and who to seek out help from
Knowing where to get help is important, make sure you're in slack.
1. Get contact details from your team members, usernames, emails, phone numbers.
2. Message members of your HIDE team in _Slack_ or via _e-mail_.
3. Understanding your question thoroughly before asking it will often lead you to asking the proper question or even directly to the answer itself.
... This is instrumental in getting the help you need.  Asking overly complex questions (too many thoughts conjoined into one) may lead to an overly complex answer.  Asking an extremely focused question, may lead you to an answer that is out of context and may ultimately be inappropriate for what you're trying to accomplish.  _Google is an artform, and the queries are your brushes. Use the appropriate tool for the task_
4. Places like _stackoverflow_ are a great wealth of knowledge, but much is outdated so be paying attention to versions and dates when applicable.
5. Sometimes just getting started can be a trial in itself, sites like [Code Academy](https://www.codecademy.com/) (Free and **highly** recommended), and [DataCamp](https://www.datacamp.com/courses/q:python) (Free Trial) or sites that teach general coding concepts like [Code Combat](https://codecombat.com) (Free, some content behind paywall).

# Features
<...to be continued>
