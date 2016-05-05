# add this script to crontab
# check job with crontab -l

ymd=`date +"%H-%M-%m%d%y"`
#echo $ymd
cd ~/data/ncep/
scrapy runspider download.py >> log_$ymd 2>&1
