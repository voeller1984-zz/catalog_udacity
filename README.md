## Item Catalog Project

This repository includes Udacity project unit 5: Linux Server Configuration

A user of this project can add, edit, and delete items belonging to a particular category.

You can visit http://18.194.205.178/ for the website deployed.

## Prerequisites

Requires Python, and git, an Ubuntu Linux Server Istance on Amazon Lightsail

## Tasks

Get your server.
1. Start a new Ubuntu Linux server instance on Amazon Lightsail. There are full details on setting up your Lightsail instance on the next page.
2. Follow the instructions provided to SSH into your server.

Secure your server.
3. Update all currently installed packages.
4. Change the SSH port from 22 to 2200. Make sure to configure the Lightsail firewall to allow it.
5. Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123).

Give grader access.
In order for your project to be reviewed, the grader needs to be able to log in to your server.

6. Create a new user account named grader.
7. Give grader the permission to sudo.
8. Create an SSH key pair for grader using the ssh-keygen tool.

Prepare to deploy your project.
9. Configure the local timezone to UTC.
10. Install and configure Apache to serve a Python mod_wsgi application.

If you built your project with Python 3, you will need to install the Python 3 mod_wsgi package on your server: sudo apt-get install libapache2-mod-wsgi-py3.
11. Install and configure PostgreSQL:

Do not allow remote connections
Create a new database user named catalog that has limited permissions to your catalog application database.
12. Install git.

### Launch virtual machine

### Connect through ssh to ubuntu linux server
Download private key (for grader see notes)
Move your key into authorized_keys directory or similar
adapt access rights to authorized_keys on your local machine:
Example: `chmod 600 .ssh/authorized_keys`
connect: `ssh grader@18.194.205.178 -i udacity_grader2.pem`

IP: 18.194.205.178
User name: grader
SSH private Key: may be downloaded from "notes to reviewer" field
SSH pubblic key: already set on server

### update Ubuntu software
sudo apt-get update
sudo apt-get upgrade


### Create new user
sudo adduser bob --disabled --password
connect to bob account: `sudo su - bob` 
mkdir .ssh
chmod 700 .ssh
create a directory for all authorized keys: `touch .ssh/authorized_keys`
limit access to directory: chmod 600 .ssh/authorized_keys`
make new ssh -key in AWS lightsail console
download private key and install on local server (e.g. udacity_grader2.pem)
copy pubblic key into .ssh/authorized_keys:
	`sudo su - bob`
	`cat >> .ssh/authorized_keys`
from MacOS connect as bob:
	`ssh bob@18.194.205.178 -i udacity_grader2.pem`

### change SSH port to 2200
change to root user: `sudo su -`
update ssh port in config file:	`nano /etc/ssh/ssh_config`
restart service	`service ssh restart`

*Note: for lightsail users, make sure additional Firewall setting under Networking allows SSH connection on port 2200*

### configure UFW
`sudo ufw allow 2200/tcp`
`sudo ufw allow 80/tcp`
`sudo ufw allow 123/udp`
`sudo ufw enable`

*Note: from now on you will connect using ssh -p2200*
example: `ssh ubuntu@18.194.205.178 -i udacity.pem -p2200`

### set timezone to UTC
`sudo dpkg-reconfigure tzdata`

### Install Apache
`sugo apt-get install Apache2`
`sudo apt-get -H install python libapache2-mod-wsgi`
`sudo service apache2 restart`

*Note: -H is only required to install packages on route directory and not only for a specific user*


### Install & Configure PSQL
`sudo apt-get -H install postgre sql`
create DB user called catalog
`sudo su - postgres`
`psql`
`CREATE DATABASE catalog;`
`CREATE USER catalog;`
`ALTER ROLE catalog WITH PASSWORD `foo`; `
`GRANT ALL PRIVILEGES ON DATABASE catalog TO catalog;`
quit postgreSQL: `⁄q`
exit from psql: `exit`

### install GIT
`sudo apt-get install git`
`sudo git clone "https://github_catalog_link" destionation_directory`

### install PIP and Python
`sudo apt-get -H install python-pip`
`sudo -H pip install Flask`

### install and enable wsgi mode
`sudo nano myapp.wsgi`
`sudo -H apt-get install libapache2.mod-wsgi python-dev`
`sudo a2enmod wsgi`

#### wsgi content
```
import sys
import logging
sys.path.insert(0, "/var/www/FlaskApp/")

from catalogUdacity import app as application 
```

### configure and enable virtual Host
configure: `sudo nano /etc/apache2/sites-available/xxx.conf`
enable: `sudo a2ensite FlaskApp`

#### configuration file structure

Note: make sure git directory and childrens are not accessible from client

```
<VirtualHost *>
        ServerName 18.194.205.178
        WSGIDaemonProcess FlaskApp
        WSGIScriptAlias /  /var/www/FlaskApp/myapp.wsgi
        <Directory /var/www/FlaskApp>
            WSGIProcessGroup FlaskApp
            WSGIApplicationGroup %{GLOBAL}
            Order deny,allow
            Allow from all
        </Directory>
        <Directorymatch "^/.*/\.git/">
                Order deny,allow
                Deny from all
        </Directorymatch>
</VirtualHost>
```


#### Flask App structure
```
	FlaskApp
	├── catalogUdacity
	│   ├── database_setup.py
	│   ├── fb_client_secrets.json
	│   ├── __init__.py
	│   ├── lots_of_menus.py
	│   ├── README.md
	│   ├── static
	│   │   └── styles.css
	│   └── templates
	│       ├── add_item.html
	│       ├── catalog.html
	│       ├── delete_item.html
	│       ├── edit_item.html
	│       ├── header.html
	│       ├── item_description.html
	│       ├── login.html
	│       └── specific_category.html
	└── myapp.wsgi
	```

#### restart Apache
`sudo service apache2 restart`


#### how to access Apache logs for errors
`sudo tail /var/log/apache2/error.log`

#### how to get your ubuntu version
`lsb_release -a`
