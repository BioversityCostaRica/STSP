# - *- coding: utf- 8 - *-

#pip install numpy==1.16.2
#pip install GDAL==$(gdal-config --version) --global-option=build_ext --global-option="-I/usr/include/gdal"

import getopt
import sys
from downloadDataWeb import downloadData
import uuid
import os
import shutil
#Print the help of the script
def usage():
    helptext = 'STSP\n\n'
    helptext = helptext + 'This script downloads the monthly information of: Normalized Difference Vegetation Indices (NDVI), projected to a country shapefile over a range of dates.. \n'
    helptext = helptext + 'Parameters:\n'
    helptext = helptext + '-s --start : From the year of which the data is required (Example: 2018-05). \n'
    helptext = helptext + '-f --finish : Until the year the data is required (Example: 2019-06)\n'
    helptext = helptext + '-c --country : Country code for cut the information \n'
    helptext = helptext + '-u --user : NASA Earthdata Username for app Daac2Disk_ubuntu \n'
    helptext = helptext + '-p --password : NASA Earthdata Password for app Daac2Disk_ubuntu \n'
    helptext = helptext + '-d --directory : Path of the folder "Countries" and "Data" \n'
    helptext = helptext + '-o --output : Path of the folder for save the .zip \n'
    helptext = helptext + '-v --version : Software version \n'
    helptext = helptext + '-h --help : Print this help \n\n'
    helptext = helptext + ".STSP (c) Bioversity International, 2019\n"
    helptext = helptext + "Author: Brandon Madriz. b.madriz@cgiar.org / bmadriz@mrbotcr.com"
    print(helptext)

# Main function
def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:s:f:c:u:p:d:o:v", ["help", "start=", "finish=", "country=","user=","password=","directory=","output=","version="])

    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(1)

    if len(opts) == 0:
        usage()
        sys.exit(1)

    start     = ""
    finish    = ""
    country   = ""
    user      = ""
    password  = ""
    directory = ""
    output    = ""

    optsRequired = ["[-s --start]","[-f --finish]","[-c --country]","[-u --user]","[-p --password]","[-d --directory]","[-o --output]"]
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-s", "--start"):
            #del optsRequired[0]
            optsRequired.remove("[-s --start]")
            if len(a.split('-')) == 2:
                try:
                    if int(a.split('-')[1]) >= 1:
                        if int(a.split('-')[1]) <= 12:
                            start = a
                        else:
                            print("")
                            print("Error parameter -s: The month has to be less than 12.")
                            sys.exit(1)
                    else:
                        print("")
                        print("Error parameter -s: The month has to be greater than 1.")
                        sys.exit(1)
                except:
                    print("")
                    print("Error: You have one error in the parameter -s. Example: 2019-01.")
                    sys.exit(1)
            else:
                print("")
                print("Error parameter -s: The date requires the year and the month separated by '-'. Example: 2019-01")
                sys.exit(1)
        elif o in ("-f", "--finish"):
            optsRequired.remove("[-f --finish]")
            if len(a.split('-')) == 2:
                try:
                    if int(a.split('-')[1]) >= 1:
                        if int(a.split('-')[1]) <= 12:
                            if int(start.split('-')[0]) <= int(a.split('-')[0]):

                                if int(start.split('-')[0]) == int(a.split('-')[0]):
                                    if int(start.split('-')[1]) <= int(a.split('-')[1]):
                                        finish = a
                                    else:
                                        print("")
                                        print("The parameter: \"-s\" must be less than the parameter: \"-f\". In the case of the month.")
                                        sys.exit(1)
                                else:
                                    finish = a
                            else:
                                print("")
                                print("The parameter: \"-s\" must be less than the parameter: \"-f\". In the case of the year.")
                                sys.exit(1)
                        else:
                            print("")
                            print("Error parameter -f: The month has to be less than 12.")
                            sys.exit(1)
                    else:
                        print("")
                        print("Error parameter -f: The month has to be greater than 1.")
                        sys.exit(1)
                except:
                    print("")
                    print("Error: You have one error in the parameter -f. Example: 2019-01.")
                    sys.exit(1)
            else:
                print("")
                print("Error parameter -f: The date requires the year and the month separated by '-'. Example: 2019-01")
                sys.exit(1)

        elif o in ("-c", "--country"):
            optsRequired.remove("[-c --country]")
            country = a
        elif o in ("-u", "--user"):
            optsRequired.remove("[-u --user]")
            user = a
        elif o in ("-p", "--password"):
            optsRequired.remove("[-p --password]")
            password = a
        elif o in ("-d", "--directory"):
            optsRequired.remove("[-d --directory]")
            directory = a
        elif o in ("-o", "--output"):
            optsRequired.remove("[-o --output]")
            if a[-4:] == ".zip":
                output = a
            else:
                print("")
                print("Error parameter -o: The output have to finish in '.zip'. Example: YOUR/PATH/FOR/output.zip")
                sys.exit(1)
        else:
            assert False, "unhandled option"

    try:
        if not optsRequired:
            print("Start: "+str(start))
            print("Finish: "+str(finish))
            print("Country: "+country)
            print("User: "+user)
            print("Password: "+password)
            print("Directory: "+ directory)
            print("Output:" +output)
            datesRequired = []

            print("")
            print("")
            print("*************GET THE DIFFERENTS DATES*************")
            for year in range(int(start.split('-')[0]),int(finish.split('-')[0])+1):
                ini = 1
                if year == int(start.split('-')[0]):
                    ini = int(start.split('-')[1])

                fin = 13
                if year == int(finish.split('-')[0]):
                    fin = int(finish.split('-')[1]) + 1

                for x in range(ini, fin):
                    datesRequired.append(str(year)+'-'+str(x)+'-01')

            uniqueId = str(uuid.uuid4())
            downloadData(datesRequired,user, password, directory, country, uniqueId)

            print("**********Creating output zip**********")
            shutil.make_archive(output[:-4],'zip', directory+ "/"+uniqueId+"/"+country+"Data")
            print("**************Download completed*************")
        else:
            sep = ", "
            print("PARSE ERROR:")
            print("\t Required arguments mising: "+sep.join(optsRequired))
            print("See the use: ")
            print("")
            usage()

    except Exception as e:
        print(e)
        sys.exit(1)


# Load the main function at start
if __name__ == "__main__":
    main()