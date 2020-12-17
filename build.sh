#!/bin/bash
startTime=$SECONDS
echo "Starting..."
#python3 /usr/local/bin/docsToMarkdown.py -produceFolderIndexes -c /var/local/docsToMarkdown.json -i /mnt/content -o /var/local/jekyll -t /mnt/jekyll 2>&1
docsToMarkdownRuntime=$(( SECONDS - startTime ))
echo "DocsToMarkdown run time: $docsToMarkdownRuntime seconds."

exit

export LC_ALL="en_US.UTF-8"
export LANG="en_US.UTF-8"
cd /var/local/jekyll; bundle exec jekyll build --destination /var/www/html --incremental >> /var/log/build.log 2>&1; cd
jekyllRuntime=$(( SECONDS - (startTime + docsToMarkdownRuntime) ))
echo "Jekyll run time: $jekyllRuntime seconds." >> /var/log/build.log
/usr/local/bin/tidyHTML.py /var/www/html >> /var/log/build.log 2>&1
tidyRuntime=$(( SECONDS - (startTime + docsToMarkdownRuntime + jekyllRuntime) ))
totalRuntime=$(( SECONDS - startTime ))
echo "Tidy run time: $tidyRuntime seconds." >> /var/log/build.log
echo "Done! Total run time: $totalRuntime seconds." >> /var/log/build.log
