# Installation steps

## Database
These steps are based on an installation on a RHEL-based distro (Fedora in this case).
All these commands are run from the root of the git clone.

### packages
``` shell
sudo dnf update
sudo dnf install postgresql postgresql-server
sudo postgresql-setup --initdb
```
If you use virtual environments:
``` shell
virtualenv -p python3 venv
source venv/bin/activate
```
If you do not use virtual environments, the following needs to run as root (sudo):
``` shell
pip3 install -r requirements.txt
```

### Database preparation
Run the following in psql:
```
create database tjadb;
create user tjadb with encrypted password 'tjadb';
grant all privileges on database tjadb to tjadb;
\i lib/db_model.sql
```

### Configuration
Next, configure the login config in `/var/lib/pgsql/data/pg_hba.conf`
``` shell
local    all             all                                     md5
host     all             all             127.0.0.1/32            md5

```


## Configuration
This section configures the website from the `etc/configuration.ini` file.

### Web
#### Host & Port
This configures the interface and port the site will run on. `0.0.0.0` means all interfaces

#### URL
Set this to the base url of the website (e.g: `https://example.com`. Don't add the trailing `/`

#### Debug
If you run the website in debug mode, you will receive error messages on the site, when something goes wrong.
If you want to disable this, set the Debug value to False

### Database
#### Host & Port
This configures the host and port of the database. If it runs on the same system, leave it to `127.0.0.1`

#### User & Password
Configures the database user & password that will connect to the DB

#### DBName
The database name of the website. Default is `tjadb`

#### Pepper
This is a fixed string that gets added when encrypting user passwords. This is an extra layer of security in case of a database breach.

### Redis
This is optional. This is only used when you use Redis for caching.

#### Host & Port
Configures the host and port of the database. If it runs on the same system, leave it to `127.0.0.1`

#### Password
Password for the database. Default: no password

#### IDDB
This is the database collection used for the caching. Defaults to `1`. Has to be an integer.

## Website

### Translations
First generate the `/web/translations/` files:
``` shell
python3 bin/localize.py generate
```
Then compile them:
``` shell
pybabel compile -d web/translations/
```

