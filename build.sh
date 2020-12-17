#!/bin/bash
startTime=$SECONDS
echo "STATUS: Running Docs To Markdown..."
python3 /usr/local/bin/docsToMarkdown.py -produceFolderIndexes -c /var/local/docsToMarkdown.json -i /mnt/content -o /var/local/jekyll -t /mnt/jekyll 2>&1
docsToMarkdownRuntime=$(( SECONDS - startTime ))
echo "STATUS: DocsToMarkdown run time: $docsToMarkdownRuntime seconds."

export LC_ALL="en_US.UTF-8"
export LANG="en_US.UTF-8"
echo "STATUS: Running Jekyll..."
cd /var/local/jekyll; bundle exec jekyll build --destination /usr/share/caddy --incremental 2>&1; cd
jekyllRuntime=$(( SECONDS - (startTime + docsToMarkdownRuntime) ))
echo "STATUS: Jekyll run time: $jekyllRuntime seconds."

echo "STATUS: Tidying HTML..."
/usr/local/bin/tidyHTML.py /usr/share/caddy 2>&1
tidyRuntime=$(( SECONDS - (startTime + docsToMarkdownRuntime + jekyllRuntime) ))
totalRuntime=$(( SECONDS - startTime ))
echo "STATUS: Tidy run time: $tidyRuntime seconds."
echo "STATUS: Total run time: $totalRuntime seconds."
echo "STATUS: Done"
