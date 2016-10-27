# LMS
A python script that keeps your local directory in sync with your LMS account, so you never have to check it!

## Get Started

Clone _lms_ repository:
    
    git clone https://github.com/usmanwardag/lms
    
Go to config.py and change _user_, _password_ and _directory_ parameters. Keep other parameters unchanged.
    
    login = {
         'user' = 'your_usernamae_here'
         'password' = 'your_password_here'
    }
         
    directory = 'your_local_directory_here'
         
Run script.py file:
    
    python script.py
    
Done! You will now see a progress report on your terminal as all of your files are downloaded.

## Make the Script Run Automatically

### On Mac OS

Use _crontab_ to create a job.

    env EDITOR=nano crontab -e
    
Paste the following. After _cd_ enter the directory which you specified above. 

    0 * * * * cd '_enter_lms_folder_directory_here' && /user/local/bin/python script.py
    
This will make your system look for updates each hour. Look for crontab documentation for more details or if you run across any errors.

### On Linux

Coming soon.

### On Windows

Coming soon.

## Bugs

If you find any, please [report an issue](https://github.com/usmanwardag/lms/issues/new)
