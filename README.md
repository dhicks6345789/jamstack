# JAMStack
Template JAMStack project built on:
* Linux (or Windows, MacOS)
* RClone (Google Drive, OneDrive, DropBox, etc)
* Flask / Python3
* Apache (or NGINX)
* Pandoc (via [DocsToMarkdown](https://github.com/dhicks6345789/docs-to-markdown))
* Jekyll (or Hugo)
* GOV.UK Design System (or other template)

## Installation

On a Linux server (currently tested on Debian 10), you can clone the project and run the install script:
```
git clone https://github.com/dhicks6345789/jamstack.git
cd jamstack
sudo python3 install.py
```
This will step through the installation and configuration of your system with the above packages, leaving you with a basic template website to start adding content and functionality to.

The recommended approach is to duplicate this project so you have your own editable version you can extend to add any further requiremnets or content to.

## Main Points Of Interest

After installation, your server will be running Apache webserver configured with a free SSL certificate from Let's Encrypt. It will only accept HTTPS connections, HTTP connections will simply be redirected to HTTPS.

Static content will be served from Apache's standard /var/www/html folder. The content in that folder is built by Jekyll from content stored in Google Drive (mounted locally via rclone) and converted via Pandoc into Markdown. This means your end users can edit content via Google Docs / Sheets / etc, or via the desktop versions of Word / Excel if you set them up with the Google Drive file sync / streaming utility on their machine.

A basic API will be created, served at yourdomain/api. Edit the "api.py" file to add calls.
