
from subprocess import run, PIPE
import configparser
config = configparser.ConfigParser()
config.read('mysql.cnf')

def importDataSet(dateString,path,country):


    args = ["goblet-importdataset",
            "-u",config.get('client','user'),
            "-p",config.get('client','password'),
            "-d",config.get('client','schema'),
            "-H",config.get('client','host'),
            "-t",country+dateString.replace("-",""),
            "-s",'"DataSet of '+dateString+'"',
            "-g", path]
    p = run(args, stdout=PIPE, encoding='ascii')
    if p.returncode == 0:
        print("*********Import dataset finished for the date "+dateString)
    else:
        print("Error. " + " ".join(args))
