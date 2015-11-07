## Install instructions
#### 1 - Install required packages
```
pip3 install zeroconf
```

#### 2 - Get Apache working and point a server to your hazc/web folder

If you know how to get apache to execute python scripts, skip to step 3. This is one way to enable it in Ubuntu:

##### 2A - Create new server config file, in this case hazc.conf:
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

##### 2B - Then execute the following commands:
```sh
sudo a2enmod cgi
sudo a2ensite hazc
sudo service apache2 restart
```

##### 2C - You may need to default to Python3
If so, just copy ```alias python=python3``` to the end of your ~/.bashrc or ~/.profile

##### 2D - Test
Point a browser to [your server address]:8080/testpy.py and you should get something like this:

If you get an error, it most likely means you need to run step 1C above, or otherwise configure apache to run python3

#### 3 - Set up your device(s)
