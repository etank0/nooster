<picture>
  <img alt="Nooster logo" src = "https://github.com/etank0/nooster/blob/main/static/nooster-head.png" height = "110px" >
</picture>

News site to find and bookmark top headlines filtered by few parameters.

## Table of Contents

- [Setup](#Setup)
- [TechStack](#TechStack)
- [Requirements](#Requirements)
- [Result](#Result)

## Setup
To deploy the the website(on local server) we need to set up a virtual environment having all the required dependencies. Everything is explained on the Flask website :arrow_down:

<a href="https://flask.palletsprojects.com/en/2.2.x/installation/"><img src = "https://user-images.githubusercontent.com/89385145/231574201-a823f3ec-ff4b-47f0-9677-6eb74c020cfd.png" height = "100px"></a>

## TechStack:
- Python(Flask)
- HTML5
- CSS
- JavaScript
- News API

#### Python-Libraries(to be installed)
- Flask
- Flask-SQLAlchemy
- Requests

## Requirements : 
Here is the quick setup in Windows and Linux/Mac os . First go to any desired directory : 
```
git clone https://github.com/etank0/nooster
```
```
cd nooster
```
Now we have successfully cloned the directory on our local system.
After this let's create a virtual environment to install all the python libraries.

- #### On Linux/Mac:
```
python3 -m venv venv
. venv/bin/activate
```
###### Now we can install all the dependencies / libraries.
```
pip install -r requirements.txt
. venv/bin/activate
```
###### Exporting the API_KEY
We need to export the API KEY provided by News API account into our environment so that modules.py can access the key.
```
export API_KEY=123abcd456
```
- #### Similarly On Windows
```
py -3 -m venv venv
venv\Scripts\activate
```
###### Now we can install all the dependencies / libraries.
```
pip install -r requirements.txt
venv\Scripts\activate
```
- #### Running :
###### Simply run the app.py python file...
```
python3 app.py
```
###### Or
```
flask run
```
###### That's it! Now the web application would be deployed on your local server.
