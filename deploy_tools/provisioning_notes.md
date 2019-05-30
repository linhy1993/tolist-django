Provisioning a new site
=======================

## Required packages
* nginx
* python3.6
* virtualenv + pip
* Git

eg, on Ubuntu
    
    sudo add-apt repository ppa:fkrull/deadsnakes
    sudo apt-get install nginx git python3.6 python3.6-venv

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