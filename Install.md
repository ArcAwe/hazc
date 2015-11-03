## Install instructions
1 - Get Apache working and point a server to your hazc/web folder

If you know how to get apache to execute python scripts, skip to step 2. This is one way to enable it in Ubuntu:

1A - Create new server config file, in this case hazc.conf:
'''
#/etc/apache2/sites-available/hazc.conf
<VirtualHost 192.168.0.10:8080>
	DocumentRoot /home/ArcAwe/Documents/hazc/web
'''
sudo a2enmod cgi
