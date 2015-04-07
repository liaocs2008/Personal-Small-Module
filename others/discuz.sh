sudo rpm -Uvh http://dev.mysql.com/get/mysql-community-release-el7-5.noarch.rpm 
sudo yum install -y httpd php php-fpm mysql mysql-server php-mysql              
sudo service httpd start && sudo service mysqld start && sudo service php-fpm start
