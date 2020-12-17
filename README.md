# JAMStack
Template [JAMStack](https://jamstack.org/)-style project built on:
* Linux ([Debian 10 "Buster"](https://wiki.debian.org/DebianBuster), or Windows, MacOS)
* [RClone](https://rclone.org/) ([Google Drive](https://drive.google.com), [OneDrive](https://onedrive.live.com), [DropBox](https://www.dropbox.com), etc)
* [Flask](https://pypi.org/project/Flask/) / [Python](https://www.python.org/)
* [Apache](https://httpd.apache.org/) (or NGINX)
* [Pandoc](https://pandoc.org/) (via my own [DocsToMarkdown](https://github.com/dhicks6345789/docs-to-markdown))
* [Jekyll](https://jekyllrb.com/) (or Hugo)
* [GOV.UK Design System](https://design-system.service.gov.uk/) (or other template)

## Installation

On a Linux server (currently tested on Debian 10 "Buster"), you can clone the project and run the install script as root:
```
curl -s https://www.sansay.co.uk/jamstack/install.py -o install.py; sudo python3 install.py; rm install.py
```
This will step through the installation and configuration of your system with the above packages, asking you for various values as it goes along, leaving you with a basic template website to start adding content and functionality to.

```
curl -s https://www.sansay.co.uk/jamstack/install.py -o install.py; sudo python3 install.py -domainName YOURSITEDOMAINNAME -contentFolderPath DRIVEPATH -jekyllFolderPath DRIVEPATH -buildPassword PASSWORD; rm install.py
```

The recommended approach is to duplicate this project so you have your own editable version you can extend to add any further requirements or content to.

## Main Points Of Interest

The installation will ask you for a few inputs along the way:

* To connect to Google Drive, you will need to provide Client ID and Secret values from your project account on the [Google Developers Console](https://console.developers.google.com/apis/credentials). If you're just testing, you can use the default values provided by rclone (just hit "enter" in both cases), although performance will probably be better with your own values. After testing, if you want to clear the existing values used and re-enter your own, simply remove the "/root/.config/rclone" folder and re-run install.py.
* The install script will set up an SSL-only configuration for Apache, with an SSL certificate provided by Let's Encrypt. You will need to have a domain name of some kind pointing at your server for that process to work, so if you're just testing you can skip the SSL setup until you have a DNS entry set up. Just re-running install.py will prompt again for SSL configuration.
* There will be a "Rebuild Site" page at http(s)://yourdomian.whatever/api/build. You will be asked to set a password to use on this page by the install script. The password is stored hashed. To change the password at a later date, simply erase "/var/local/buildPassword.txt" and re-run install.py.

Static content will be served from Apache's standard "/var/www/html" folder. The content in that folder is built by Jekyll from content stored in Google Drive (mounted locally via rclone) and converted via Pandoc / [DocsToMarkdown](https://github.com/dhicks6345789/docs-to-markdown) into the [Govspeak](https://github.com/alphagov/govspeak) varient of [Markdown](https://en.wikipedia.org/wiki/Markdown). This means your end users can edit content via GSuite, the online version of Office 365, or via the desktop versions of Word / Excel if you set them up with the Google Drive file sync / streaming utility on their machine.

A basic API will be created, served at http(s)://yourdomian.whatever/api. Edit the "api.py" file to add calls. The default API contains a simple "build" call, accesible via a GET request. You can use this GET request as an endpoint for workflow automation tools such as [Zapier](https://zapier.com/) - just set up your trigger (maybe a file being added or changed in a Google Drive folder) in your tool of choice and point it at ``https://yourdomian.whatever/api/build?action=run&password=yourPassword``.
