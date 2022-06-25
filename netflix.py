import os
import sys
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
if sys.version_info[0] < 3:
    print("Please download Python3 from the link below")
    print("https://www.python.org/downloads/")
    input("Press any key to exit!")
    sys.exit("Python3 not installed")
try:
    os.system("pip3 install -q --disable-pip-version-check --no-cache-dir --no-color --no-warn-conflicts mysql-connector-python")
except:
    sys.exit("Unable to install required dependencies!")
try:
    from mysql.connector import connect
except:
    sys.exit("Unable to import required dependencies")
cdb = connect(host="localhost", user="root", password="17102005")
db = cdb.cursor()
db.execute("CREATE DATABASE IF NOT EXISTS netflix")
cdb.commit()
db.close()
cdb.close()
cdb = connect(host="localhost", user="root", password="17102005", database="netflix")
db = cdb.cursor()
