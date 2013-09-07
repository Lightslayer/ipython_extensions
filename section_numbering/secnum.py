"""IPython Notebook magic for numbering sections

%load_ext secnum
%secnum

to have automatic section numbering

Based on MinRK's nbtoc magic

"""

import io
import os
import urllib2

from IPython.display import display_html, display_javascript

here = os.path.abspath(os.path.dirname(__file__))
nbtoc_js = ""
nbtoc_html = ""

def download(fname, redownload=False):
    """download a file
    
    if redownload=False, the file will not be downloaded if it already exists.
    """
    dest = os.path.join(here, fname)
    if os.path.exists(dest) and not redownload:
        return
    url = 'https://raw.github.com/minrk/ipython_extensions/master/' + fname
    print("Downloading %s to %s" % (url, dest))
    
    filein  = urllib2.urlopen(url)
    fileout = open(dest, "wb")
    chunk = filein.read(1024)
    while chunk:
        fileout.write(chunk)
        chunk = filein.read(1024)
    filein.close()
    fileout.close()

def load_file(fname, redownload=False):
    """load global variable from a file"""
    download(fname, redownload)
    with io.open(os.path.join(here, fname)) as f:
        globals()[fname.replace('.', '_')] = f.read()

load_file('nbtoc.js')
load_file('nbtoc.html')

def nbtoc(line):
    """add a table of contents to an IPython Notebook"""
    display_html(nbtoc_html, raw=True)
    display_javascript(nbtoc_js, raw=True)

def update_nbtoc(line):
    """download the latest version of the nbtoc extension from GitHub"""
    download('nbtoc.py', True)
    download('nbtoc.js', True)
    download('nbtoc.html', True)
    get_ipython().extension_manager.reload_extension("nbtoc")
    
def load_ipython_extension(ip):
    ip.magics_manager.register_function(nbtoc)
    ip.magics_manager.register_function(update_nbtoc)

