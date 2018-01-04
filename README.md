# toilet-business
The future by Lynn, Tracy, Ken

### Developer Tips:
* Clone repository or download zip file directly
>>$ git clone url(git's url)
* Install virtual environment
>> pip install virtualenv
* Create virtualenv in the root(here is called toilet_business) folder
>>$ cd ..... (go into the root folder)  
>>$ virtualenv env
* Activate virtual env
>>$ source env/bin/activate (mac os)  
>>$ env\Scripts\activate (windows)
* Install requirement.txt on virtual environment (pip3 install -r requirement.txt) (for mac os)
  if your os is windows, skip this step and forward to the next step.
>>$ pip3 install -r requirement.txt
* Because of leveldb cannot be install with pip on windows, so copy the leveldb.pyd (doc folder) into YOUR_PYTHON_ROOT/Lib/site-packages,
  here we recommend to use virtual environment, so copy into YOUR_PYTHON_ROOT/env/Lib/site-packages and run commend:
>> pip install -r windows-requirement.txt
* Run main program called app.py to start local development server
>>$ python3 app.py
* Open browser http://127.0.0.1:5000/

### Git Tips:
* Recommend checkout into the branch (develop)
>> git checkout develop
* See now branch state
>> git status

    On branch develop
    nothing to commit, working directory clean
* commit your modify
>> git commit -m 'something about this commit'
* check remote repository
>> git remote -v
* push your modify (we are in the develop branch)
  -u commend is setting the upstream, and you can just use 'git push' next time.
>> git push -u origin develop

### Folder Description:
#### Here are using packages and blueprints for application, and this is call Application Factories
    (root folder)
    /toilet_business
     
        (python package)
        /toilet_business
            (The __init__.py file is required to make Python treat the directories as containing packages, it can just be an empty file, but it can also execute initialization code for the package or set the __all__ variable)
            /__init__.py
            
            (put your static file in here, such as: css, flask will find static file start here)
            /static
                /css
                /icon
                /js
            
            (put your all template file in here, such as: html, flask will find template file start here)
            /templates
                /home   (put blueprint template file we defined in here)
            
            (This is put your blueprint package definition)
            /views
                (The __init__.py file is required to make Python treat the directories as containing packages, it can just be an empty file, but it can also execute initialization code for the package or set the __all__ variable)
                /__init__.py
          
        /app.py (main)
        /requirement.txt (lists of packages to install)