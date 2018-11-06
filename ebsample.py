#!/usr/bin/env python

##################################################################
############################  EB Sample  ##########################
###########################Akshit Khanna###########################

import argparse
from urllib2 import urlopen, URLError, HTTPError
from bs4 import BeautifulSoup
import re
import urllib2
import os
import zipfile


regex = {'java':'java-se-jetty-gradle-v.\.zip',
'tomcat':'java-tomcat-v.\.zip',
'node':'nodejs-v.\.zip',
'sdocker':'docker-singlecontainer-v.\.zip',
'mdocker':'docker-multicontainer-v.\.zip',
'go':'go-v.\.zip',
'passenger':'ruby-passenger-v.\.zip',
'puma':'ruby-puma-v.\.zip',
'windows':'dotnet-asp-v.\.zip',
'php':'php-v.\.zip',
'python':'python-v.\.zip'}


class ebGetSrce:
    def __init__(self, _sol_stack, _extract_flag):

        self._sol_stack         = _sol_stack.strip()
        self._extract_flag      = _extract_flag   #indicates if user wants to extract the downloaded source bundle
        self._sample_page       = "http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/tutorials.html"
        self._sample_url_page   = "http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/samples/"
        self._links             = []
        self._bundle_name       = ""

    def get_sg_id(self):
        try:
            _command_output = subprocess.check_output(["aws", "ec2", "describe-security-groups", "--group-names", self._sg_name, "--region", self._region, "--query", "SecurityGroups[0].GroupId", "--output", "text" ],stderr=subprocess.STDOUT)
            self._sg_id     = _command_output.strip()
            return 0
        except subprocess.CalledProcessError, e:
            print ("Unable to find a Security Group with the Name: " + self._sg_name + " in the region: " + self._region + "\n")
            return 1

    def get_urls(self):
        conn = urllib2.urlopen(self._sample_page)
        html = conn.read()
        soup = BeautifulSoup(html, "html.parser")
        pattern = re.compile("samples/")         #get only those URLs that match this pattern
        links = soup.find_all('a', {'href': pattern})
        self.retrieve_sample_name(links)

    def retrieve_sample_name(self, links):
        _bundles = []
        for i in links:
            _parts       = str(i).split('"')
            _name_string = _parts[1]
            _bundle_name = _name_string.split('samples/')[1]
            _bundles.append(_bundle_name)
        self.generate_url(_bundles)

    def generate_url(self, bundles):
        _regex         = regex[self._sol_stack]
        reg            = re.compile(_regex)
        self._bundle_name   = str([m.group(0) for l in bundles for m in [reg.search(l)] if m][0]).strip()
        _download_link = "http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/samples/" + self._bundle_name
        self.download_bundle(_download_link)

    def download_bundle(self, _download_link):

        try:
            f = urlopen(_download_link)
            print "Downloading " + _download_link

            # Open our local file for writing
            with open(os.path.basename(_download_link), "wb") as local_file:
                local_file.write(f.read())

            #handle errors
        except HTTPError, e:
            print "HTTP Error:", e.code, _download_link
        except URLError, e:
            print "URL Error:", e.reason, _download_link

    def extract_and_delete(self):
        if (self._extract_flag):
            with zipfile.ZipFile(self._bundle_name,"r") as zip_ref:
                zip_ref.extractall(".")
            os.remove(self._bundle_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("solution_stack", help="Enter the name of the Solution Stack", choices=['tomcat','java','sdocker','mdocker','java','python','windows','php','node','go','passenger','puma'])
    parser.add_argument('-e', help="Use this flag to extract archive and delete zip file", action='store_true')
    parser.parse_args()
    args = parser.parse_args()
    parserObject = ebGetSrce(args.solution_stack, args.e)
    parserObject.get_urls()
    parserObject.extract_and_delete()
