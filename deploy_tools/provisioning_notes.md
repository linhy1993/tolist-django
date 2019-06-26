Provisioning a new site
=======================

## Required packages
* nginx
* python3.6
* virtualenv + pip
* Git

eg, on Ubuntu
    
    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get install nginx git python3.6 python3-venv

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with, e.g., staging.my-domain.com

## Systemd service

* see gunicorn-systemd.template.service
* replace SITENAME with, e.g., staging.,my-domain.com

## Folder structure
Assuming we have a user account at /home/username

/home/username
```bash
└── sites
    ├── SITENAME
        ├── databse
        ├── source
        ├── static
        └── virtualenv
```
on local,

     fab deploy:host=ubuntu@YOURHOSTNAME

eg, on AWS

    sed "s/SITENAME/YOURHOSTNAME/g" source/deploy_tools/nginx.template.conf | sudo tee /etc/nginx/sites-available/YOURHOSTNAME

    sudo ln -s ../sites-available/YOURHOSTNAME /etc/nginx/sites-enabled/YOURHOSTNAME
    
    sed "s/SITENAME/YOURHOSTNAME/g" source/deploy_tools/gunicorn-systemd.template.service | sudo tee /etc/systemd/system/gunicorn-YOURHOSTNAME.service
    
    sudo systemctl daemon-reload 
    sudo systemctl reload nginx
    sudo systemctl enable gunicorn-YOURHOSTNAME
    sudo systemctl start gunicorn-YOURHOSTNAME