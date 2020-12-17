#!/usr/bin/python3

import os
import sys
import time
import shutil
import hashlib

projectRoot = "https://www.sansay.co.uk/jamstack"

# Parse any options set by the user on the command line.
validBooleanOptions = []
validValueOptions = ["-domainName", "-contentFolderPath", "-jekyllFolderPath", "-buildPassword"]
userOptions = {}
optionCount = 1
while optionCount < len(sys.argv):
    if sys.argv[optionCount] in validBooleanOptions:
        userOptions[sys.argv[optionCount]] = True
    elif sys.argv[optionCount] in validValueOptions:
        userOptions[sys.argv[optionCount]] = sys.argv[optionCount+1]
        optionCount = optionCount + 1
    optionCount = optionCount + 1

def runIfPathMissing(thePath, theCommand):
    if not os.path.exists(thePath):
        print("Running: " + theCommand)
        os.system(theCommand)
        
def downloadFile(src, dest, mode=None):
    print("Copying file " + src + " to " + dest)
    os.system("curl -s " + projectRoot + "/" + src + " -o " + dest)
    if not mode == None:
        os.system("chmod " + mode + " " + dest)

def getUserOption(optionName, theMessage):
    if not optionName in userOptions.keys():
        userOptions[optionName] = input(theMessage + ": ")
    return(userOptions[optionName])

def askUserMenu(theOptions):
    for optionCount in range(0, len(theOptions)):
        print(str(optionCount+1) + ": " + theOptions[optionCount])
    userSelection = input("Selection: ")
    return(int(userSelection))

def readFile(theFilename):
    fileDataHandle = open(theFilename, "r")
    fileData = fileDataHandle.read()
    fileDataHandle.close()
    return(fileData)
    
def writeFile(theFilename, theFileData):
    fileDataHandle = open(theFilename, "w")
    if isinstance(theFileData, list):
        fileDataHandle.write("\n".join(theFileData))
    else:
        fileDataHandle.write(theFileData)
    fileDataHandle.close()
    
def replaceVariables(theFile, theKeyValues):
    fileData = readFile(theFile)
    for keyValue in theKeyValues.keys():
        fileData = fileData.replace("<<" + keyValue + ">>", theKeyValues[keyValue])
    writeFile(theFile, fileData)
    
def runExpect(inputArray):
    writeFile("temp.expect", inputArray)
    os.system("expect temp.expect")
    os.system("rm temp.expect")

print("Installing JAMStack...")

# Make sure dos2unix (line-end conversion utility) is installed.
runIfPathMissing("/usr/bin/dos2unix", "apt-get install -y dos2unix")

# Make sure Pip3 (Python 3 package manager) is installed.
runIfPathMissing("/usr/bin/pip3", "apt-get install -y python3-pip")

# Figure out what version of Python3 we have installed.
pythonVersion = os.popen("ls /usr/local/lib | grep python3").read().strip()

# Make sure Git (source code control client) is installed.
runIfPathMissing("/usr/bin/git", "apt-get install -y git")

# Make sure curl (utility to get files from the web) is installed.
runIfPathMissing("/usr/bin/curl", "apt-get install -y curl")

# Make sure build-essential (Debian build environment, should include most tools you need to build other packages) is installed.
runIfPathMissing("/usr/share/doc/build-essential", "apt-get install -y build-essential")

# Make sure ZLib (compression library, required for building other packages) is installed.
runIfPathMissing("/usr/share/doc/zlib1g-dev", "apt-get install -y zlib1g-dev")

# Make sure ruby-dev (the Ruby development environment, needed for Jekyll) is installed.
runIfPathMissing("/usr/share/doc/ruby-dev", "apt-get install -y ruby-dev")

# Make sure Jekyll (static site generation tool) is installed.
runIfPathMissing("/usr/local/bin/jekyll", "gem install bundler jekyll concurrent-ruby")
runIfPathMissing("/root/.bundle", "bundle install")
os.system("mkdir /.bundle > /dev/null 2>&1")
os.system("chown www-data:www-data /.bundle > /dev/null 2>&1")

# Make sure Pandoc (conversion utility for converting various file formats, in this case DOCX to Markdown) is installed.
# Note that we need at least version 2.7.1, released March 2019, as it contains a bug fix to handle O365-created DOCX files properly - the version included by Debian Stretch is not yet up to date.
runIfPathMissing("/usr/bin/pandoc", "wget https://github.com/jgm/pandoc/releases/download/2.7.1/pandoc-2.7.1-1-amd64.deb; dpkg -i pandoc-2.7.1-1-amd64.deb; rm pandoc-2.7.1-1-amd64.deb")

# Make sure Flask (Python web-publishing framework) is installed.
runIfPathMissing("/usr/local/lib/"+pythonVersion+"/dist-packages/flask", "pip3 install flask")

# Make sure XLRD (Python library for handling Excel files, required for Excel support in Pandas) is installed.
runIfPathMissing("/usr/local/lib/"+pythonVersion+"/dist-packages/xlrd", "pip3 install xlrd")

# Make sure Pandas (Python data-analysis library) is installed.
runIfPathMissing("/usr/local/lib/"+pythonVersion+"/dist-packages/pandas", "pip3 install pandas")

# Make sure Numpy (Python maths library) is installed.
runIfPathMissing("/usr/local/lib/"+pythonVersion+"/dist-packages/numpy", "pip3 install numpy")

# Make sure Expect (command-line automation utility) is installed.
runIfPathMissing("/usr/bin/expect", "apt-get -y install expect")

# Make sure rclone (for mounting cloud-based filesystems such as Google Drive) is installed.
runIfPathMissing("/usr/bin/rclone", "curl https://rclone.org/install.sh | sudo bash")

# Make sure FUSE (for mounting user filesystems, used by rclone) is installed.
runIfPathMissing("/usr/bin/fusermount", "apt-get -y install fuse")

# Make sure Caddy (web server) is installed.
runIfPathMissing("/usr/bin/caddy", "echo \"deb [trusted=yes] https://apt.fury.io/caddy/ /\" | sudo tee -a /etc/apt/sources.list.d/caddy-fury.list; apt-get update; apt-get install caddy")

getUserOption("-domainName", "Please enter this site's domain name")

# Copy over the Caddy configuration file.
downloadFile("Caddyfile", "/etc/caddy/Caddyfile", mode="0744")
replaceVariables("/etc/caddy/Caddyfile", {"DOMAINNAME":userOptions["-domainName"]})

# Make sure Web Console (simple web user interface for command-line applications) is installed...
os.system("curl -s https://www.sansay.co.uk/web-console/install.sh | sudo bash")
# ...and configured.
if not os.path.exists("/etc/webconsole/tasks/build"):
    getUserOption("-buildPassword", "Please enter this site's build password")
    os.system("webconsole --new --newTaskID build --newTaskTitle \"Build Site\" --newTaskSecret " + userOptions["-buildPassword"] + " --newTaskPublic N --newTaskCommand build.sh")
downloadFile("webconsoleConfig.csv", "/etc/webconsole/config.csv", mode="0744")

# Make sure Rclone is set up to connect to the user's cloud storage - we might need to ask the user for some details.
if not os.path.exists("/root/.config/rclone/rclone.conf"):
    print("Configuring rclone...")
    getUserOption("-contentFolderPath", "Please enter the path that contains the content")
    getUserOption("-jekyllFolderPath", "Please enter the path that contains the Jekyll setup")
    runExpect([
        "spawn /usr/bin/rclone config",
        "expect \"n/s/q>\"",
        "send \"n\\r\"",
        "expect \"name>\"",
        "send \"drive\\r\"",
        "expect \"Storage>\"",
        "send \"drive\\r\"",
        "expect \"client_id>\"",
        "expect_user -timeout 3600 -re \"(.*)\\n\"",
        "send \"$expect_out(1,string)\\r\"",
        "expect \"client_secret>\"",
        "expect_user -timeout 3600 -re \"(.*)\\n\"",
        "send \"$expect_out(1,string)\\r\"",
        "expect \"scope>\"",
        "send \"drive.readonly\\r\"",
        "expect \"root_folder_id>\"",
        "send \"\\r\"",
        "expect \"service_account_file>\"",
        "send \"\\r\"",
        "expect \"y/n>\"",
        "send \"n\\r\"",
        "expect \"y/n>\"",
        "send \"n\\r\"",
        "expect \"Enter verification code>\"",
        "expect_user -timeout 3600 -re \"(.*)\\n\"",
        "send \"$expect_out(1,string)\\r\"",
        "expect \"y/n>\"",
        "send \"n\\r\"",
        "expect \"y/e/d>\"",
        "send \"y\\r\"",
      
        "expect \"e/n/d/r/c/s/q>\"",
        "send \"n\\r\"",
        "expect \"name>\"",
        "send \"content\\r\"",
        "expect \"Storage>\"",
        "send \"cache\\r\"",
        "expect \"remote>\"",
        "send \"drive:"+userOptions["-contentFolderPath"]+"\\r\"",
        "expect \"plex_url>\"",
        "send \"\\r\"",
        "expect \"plex_username>\"",
        "send \"\\r\"",
        "expect \"y/g/n>\"",
        "send \"n\\r\"",
        "expect \"chunk_size>\"",
        "send \"10M\\r\"",
        "expect \"info_age>\"",
        "send \"1y\\r\"",
        "expect \"chunk_total_size>\"",
        "send \"1G\\r\"",
        "expect \"y/n>\"",
        "send \"n\\r\"",
        "expect \"y/e/d>\"",
        "send \"y\\r\"",
        
        
        "expect \"e/n/d/r/c/s/q>\"",
        "send \"n\\r\"",
        "expect \"name>\"",
        "send \"jekyll\\r\"",
        "expect \"Storage>\"",
        "send \"cache\\r\"",
        "expect \"remote>\"",
        "send \"drive:"+userOptions["-jekyllFolderPath"]+"\\r\"",
        "expect \"plex_url>\"",
        "send \"\\r\"",
        "expect \"plex_username>\"",
        "send \"\\r\"",
        "expect \"y/g/n>\"",
        "send \"n\\r\"",
        "expect \"chunk_size>\"",
        "send \"10M\\r\"",
        "expect \"info_age>\"",
        "send \"1y\\r\"",
        "expect \"chunk_total_size>\"",
        "send \"1G\\r\"",
        "expect \"y/n>\"",
        "send \"n\\r\"",
        "expect \"y/e/d>\"",
        "send \"y\\r\"",
        
        "send \"q\\r\""
    ])

# Set up rclone to mount the user's cloud storage - first, stop any existing rclone mount process...
os.system("systemctl stop rclone-content")
os.system("systemctl stop rclone-jekyll")
# ...make sure FUSE is configured to allow non-root users to access mounts...
downloadFile("fuse.conf", "/etc/fuse.conf", mode="644")
# ...make sure the mount point and cache folders exist...
os.makedirs("/mnt/content", exist_ok=True)
os.makedirs("/mnt/jekyll", exist_ok=True)
os.makedirs("/var/cache/rclone-content", exist_ok=True)
os.makedirs("/var/cache/rclone-jekyll", exist_ok=True)
# ...then set up systemd to mount the repository.
downloadFile("rclone-content.service", "/etc/systemd/system/rclone-content.service", mode="644")
downloadFile("rclone-jekyll.service", "/etc/systemd/system/rclone-jekyll.service", mode="644")
os.system("systemctl start rclone-content")
os.system("systemctl start rclone-jekyll")
os.system("systemctl enable rclone-content")
os.system("systemctl enable rclone-jekyll")

# Copy accross the build.sh script.
downloadFile("build.sh", "/etc/webconsole/tasks/build/build.sh", mode="755")

# Copy over the Python scipt that cleans up HTML files.
downloadFile("tidyHTML.py", "/usr/local/bin/tidyHTML.py", mode="0755")
os.system("chown www-data:www-data /usr/local/bin/tidyHTML.py")

# Install DocsToMarkdown.
runIfPathMissing("/usr/local/bin/docsToMarkdown.py", "curl https://raw.githubusercontent.com/dhicks6345789/docs-to-markdown/master/docsToMarkdown.py -o /usr/local/bin/docsToMarkdown.py; chmod a+x /usr/local/bin/docsToMarkdown.py; echo > /var/log/build.log; chown www-data:www-data /var/log/build.log")
runIfPathMissing("/var/local/jekyll", "mkdir /var/local/jekyll; chown www-data:www-data /var/local/jekyll")
downloadFile("docsToMarkdown.json", "/var/local/docsToMarkdown.json", mode="644")
os.system("chown www-data:www-data /var/local/docsToMarkdown.json")
