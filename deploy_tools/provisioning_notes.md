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

     fab deploy:host=ubuntu@3.13.139.223

eg, on AWS

    sed "s/SITENAME/3.13.139.223/g" source/deploy_tools/nginx.template.conf | sudo tee /etc/nginx/sites-available/3.13.139.223

    sudo ln -s ../sites-available/3.13.139.223 /etc/nginx/sites-enabled/3.13.139.223
    
    sed "s/SITENAME/3.13.139.223/g" source/deploy_tools/gunicorn-systemd.template.service | sudo tee /etc/systemd/system/gunicorn-3.13.139.223.service
    
    sudo systemctl daemon-reload 
    sudo systemctl reload nginx
    sudo systemctl enable gunicorn-3.13.139.223
    sudo systemctl start gunicorn-3.13.139.223