# LMS
A python script that keeps your local directory in sync with your LMS account, so you never have to check it!

## Get Started

Clone _lms_ repository:
    
    git clone https://github.com/usmanwardag/lms
    
Go to config.yml and change _user_, _password_ and _local_ parameters. Keep the other parameters unchanged.
    
    login:
         user: 'your_usernamae_here'
         password: 'your_password_here'
         
    directory:
         local: 'your_local_directory_here'
         
Run script.py file:
    
    python script.py
    
Done! You will now see a progress report on your terminal as all of your files are downloaded.
