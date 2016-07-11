
   sudo aptitude install python-webpy

   sudo aptitude install apache2 libapache2-mod-wsgi
   sudo a2enmod cgi

   sudo touch /var/log/mimic.log
   sudo chown www-data:www-data /var/log/mimic.log 

   sudo apt-get install libapache2-mod-wsgi

   sudo pip install aiml
   sudo pip install pattern

   # APACHE-CONF
   cat /etc/apache2/sites-available/mimic

   <VirtualHost *:80>
      ServerAdmin webmaster@localhost
      DocumentRoot /data/mega/research/AI/mimic/

      <Directory /data/mega/research/AI/mimic> 
         Require all granted
         Options +ExecCGI                                                                                                   
         DirectoryIndex ws.py                                                                             
         AddHandler cgi-script .py  
      </Directory> 
    
      <Directory /data/mega/research/AI/mimic/ui>
         Require all granted
      </Directory>

      ErrorLog ${APACHE_LOG_DIR}/error.log
      CustomLog ${APACHE_LOG_DIR}/access.log combined
   </VirtualHost>



