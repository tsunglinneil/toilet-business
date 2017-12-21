# toilet-business
The future

### Developer Tips:
* clone repository or download zip file 
* create virtualenv in the root(here is called toilet_business) folder
* install requirement.txt on virtual environment
* run main program called app.py to start local development server
* open browser 127.0.0.1:5000/

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