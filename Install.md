## Install instructions
#### 1 - Get Apache working and point a server to your hazc/web folder

If you know how to get apache to execute python scripts, skip to step 2. This is one way to enable it in Ubuntu:

##### 1A - Create new server config file, in this case hazc.conf:
```
#/etc/apache2/sites-available/hazc.conf
Listen 8080
<VirtualHost *:8080>
	DocumentRoot /home/ArcAwe/Documents/hazc/web

	<Directory "/">
		Options +ExecCGI
		AddHandler cgi-script .py
		Require all granted
	</Directory>

	LogLevel notice

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

##### 1B - Then execute the following commands:

sudo a2enmod cgi

sudo a2ensite hazc

sudo service apache2 restart

