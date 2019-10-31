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

On a Linux server (currently tested on Debian 10), you can clone the project and run the install script as root:
```
git clone https://github.com/dhicks6345789/jamstack.git
cd jamstack
python3 install.py
```
This will step through the installation and configuration of your system with the above packages, leaving you with a basic template website to start adding content and functionality to.

The recommended approach is to duplicate this project so you have your own editable version you can extend to add any further requiremnets or content to.

## Main Points Of Interest

The installation will ask you for a few inputs along the way:

* To connect to Google Drive, you will need to provide Client ID and Secret values from your project account on the [Google Developers Console](https://console.developers.google.com/apis/credentials). If you're just testing, you can use the default values provided with rclone (just hit "enter" in both cases), although performance will probably be better with your own values. After testing, if you want to clear the existing values used and re-enter your own, simply remove the "/root/.config/rclone" folder and re-run install.py.
* The install script will set up an SSL-only configuration for Apache, with an SSL certificate provided by Let's Encrypt. You will need to have a domain name of some kind pointing at your server for that process to work, so if you're just testing you can skip the SSL setup until you have a DNS entry set up. Just re-running install.py will prompt again for SSL configuration.
* There will be a "Rebuild Site" page at http(s)://yourdomian.whatever/api/build. You will be asked to set a password to use on this page by the install script. The password is stored hashed. To change the password at a later date, simply erase "/var/local/buildPassword.txt".

Static content will be served from Apache's standard "/var/www/html" folder. The content in that folder is built by Jekyll from content stored in Google Drive (mounted locally via rclone) and converted via Pandoc / [DocsToMarkdown](https://github.com/dhicks6345789/docs-to-markdown) into Markdown. This means your end users can edit content via Google Docs / Sheets / etc, or via the desktop versions of Word / Excel if you set them up with the Google Drive file sync / streaming utility on their machine.

A basic API will be created, served at http(s)://yourdomian.whatever/api. Edit the "api.py" file to add calls.
