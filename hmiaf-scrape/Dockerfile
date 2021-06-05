FROM amazonlinux:latest
COPY / /scraper/
RUN amazon-linux-extras install epel -y
RUN yum install python3 -y
RUN pip3 install mysql-connector-python beautifulsoup4 requests boto3
RUN python3 /scraper/scraperMain.py