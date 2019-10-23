#!/usr/bin/python3

import os
import time
import shutil

def runIfPathMissing(thePath, theCommand):
    if not os.path.exists(thePath):
        print("Running: " + theCommand)
        os.system(theCommand)
        
def copyfile(src, dest, mode=None):
    srcStat = os.stat(src)
    if (not os.path.exists(dest)) or (not str(srcStat.st_mtime) == str(os.stat(dest).st_mtime)):
        print("Copying file " + src + " to " + dest)
        shutil.copyfile(src, dest)
        os.utime(dest, (srcStat.st_atime, srcStat.st_mtime))
        if not mode == None:
            os.system("chmod " + mode + " " + dest)
            #os.chmod(dest, int(mode))
        return(1)
    return(0)

print("Installing...")

# Make sure dos2unix (line-end conversion utility) is installed.
runIfPathMissing("/usr/bin/dos2unix", "apt-get install -y dos2unix")

# Make sure Pip (Python package manager) is installed.
runIfPathMissing("/usr/bin/pip3", "apt-get install -y python3-pip")

# Make sure Git (source code control client) is installed.
runIfPathMissing("/usr/bin/git", "apt-get install -y git")

# Make sure build-essential (Debian build environment, should include most tools you need to build other packages) is installed.
runIfPathMissing("/usr/share/doc/build-essential", "apt-get install -y build-essential")

# Make sure ZLib (compression library, required for building other packages) is installed.
runIfPathMissing("/usr/share/doc/zlib1g-dev", "apt-get install -y zlib1g-dev")

# Make sure ruby-dev (the Ruby development environment) is installed.
runIfPathMissing("/usr/share/doc/ruby-dev", "apt-get install -y ruby-dev")

# Make sure Jekyll (static site generation tool) is installed.
runIfPathMissing("/usr/local/bin/jekyll", "gem install bundler jekyll")
runIfPathMissing("/root/.bundle", "bundle install")
os.system("mkdir /.bundle > /dev/null 2>&1")
os.system("chown www-data:www-data /.bundle > /dev/null 2>&1")

# Make sure Pandoc (conversion utility for converting various file formats, in this case DOCX to Markdown) is installed.
# Note that we need version 2.7.1, released March 2019, as it contains a bug fix to handle O365-created DOCX files properly - the version included by Debian Stretch is not yet up to date.
runIfPathMissing("/usr/bin/pandoc", "wget https://github.com/jgm/pandoc/releases/download/2.7.1/pandoc-2.7.1-1-amd64.deb; dpkg -i pandoc-2.7.1-1-amd64.deb; rm pandoc-2.7.1-1-amd64.deb")

# Make sure XLRD (Python library for handling Excel files, required for Excel support in Pandas) is installed.
runIfPathMissing("/usr/local/lib/python3.5/dist-packages/xlrd", "pip3 install xlrd")

# Make sure Pandas (Python data-analysis library) is installed.
runIfPathMissing("/usr/local/lib/python3.5/dist-packages/pandas", "pip3 install pandas")

# Make sure Numpy (Python maths library) is installed.
runIfPathMissing("/usr/local/lib/python3.5/dist-packages/numpy", "pip3 install numpy")
