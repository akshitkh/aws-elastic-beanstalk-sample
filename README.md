###################################################################
################### EB Sample App Downloader ######################
###################### Akshit Khanna ##############################
########################## AWS Tools ##############################


Downloads the Elastic Beanstalk sample application for any solution stack to the current directory. I find this very useful to quickly download the sample application, extract it, delete the archive, all at once from the command line. Deploying sample applications is a recommended troubleshooting step that can also be used to test ebextensions on an Elastic Beanstalk environment. 


Installation:

1. Install BeautifulSoup

"pip3 install BeautifulSoup"

Usage: (Auto Complete should work for ebsample)

1. "python ebsample.py -h" : Help

2. "python ebsample.py <Platform Keyword> -e" : Extracts the zip and deletes it


-> Platform Keywords:
tomcat
java
sdocker
mdocker
java
python
windows
php
node
go
passenger
puma

Release Notes:

-- Parses the documentation and downloads the sample app to the PWD
-- "-e" flag will unzip the archive and delete it
