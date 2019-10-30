#!/bin/bash
startTime=$SECONDS
echo "Starting..." > /var/log/build.log
python3 /usr/local/bin/docsToMarkdown.py -c /var/local/docsToMarkdown.json -i /mnt/content -o /var/local/jekyll -t /mnt/jekyll >> /var/log/build.log 2>&1
docsToMarkdownRuntime=$(( SECONDS - startTime ))
echo "DocsToMarkdown run time: $docsToMarkdownRuntime seconds." >> /var/log/build.log
export LC_ALL="en_US.UTF-8"
export LANG="en_US.UTF-8"
cd /var/local/jekyll; bundle exec jekyll build --destination /var/www/html --incremental >> /var/log/build.log 2>&1; cd
jekyllRuntime=$(( SECONDS - docsToMarkdownRuntime ))
echo "Jekyll run time: $jekyllRuntime seconds." >> /var/log/build.log
/usr/local/bin/tidyHTML.py /var/www/html >> /var/log/build.log 2>&1
tidyRuntime=$(( SECONDS - jekyllRuntime ))
totalRuntime=$(( SECONDS - startTime ))
echo "Tidy run time: $tidyRuntime seconds." >> /var/log/build.log
echo "Done! Total run time: $totalRuntime seconds." >> /var/log/build.log
