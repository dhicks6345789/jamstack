#!/bin/bash
python3 /usr/local/bin/docsToMarkdown.py -c /var/local/docsToMarkdown.json -i /mnt/content -o /var/local/jekyll -t /mnt/jekyll > /var/log/docsToMarkdown.log 2>&1
#export LC_ALL="en_US.UTF-8"
#export LANG="en_US.UTF-8"
#cd /var/local/accessDisputesCommittee/jekyll; bundle exec jekyll build --destination /var/www/html --incremental >> /var/local/accessDisputesCommittee/log.txt 2>&1; cd
#/usr/local/bin/tidyHTML.py /var/www/html > /var/local/accessDisputesCommittee/log.txt 2>&1