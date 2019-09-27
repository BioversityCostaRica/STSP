from datetime import datetime
import os
from glob import glob
from subprocess import run, PIPE
from gobletFunctions import importDataSet
from calcBoundingBoxes import getBBox
countriesPath = os.path.dirname(os.path.abspath(__file__))
#box_array = ['-86.049', '8.038', '-82.484', '11.192']

def downloadData(listOfRequired, user, password, localPath, country, uuid):

    minLong, maxLong, minLat, maxLat = getBBox(countriesPath + "/Countries/"+country+"/"+country+".shp")
    box_array = [str(minLong), str(minLat),str(maxLong), str(maxLat)]
    #print(box_array)
    pathForProcessed = localPath + "/"+uuid+"/"+country+"Data"
    if not os.path.exists(pathForProcessed):
        os.makedirs(pathForProcessed)

    for required in listOfRequired:

        print("*Date: "+required)
        workingWithDate = datetime.strptime(required,"%Y-%m-%d")
        pathPerMonth = workingWithDate.strftime("%Y/%m")
        pathOutputForHDF = localPath + "/"+uuid+"/"+country+"/" + pathPerMonth + "/hdf"
        pathOutputForASC = localPath + "/"+uuid+"/"+country+"/" + pathPerMonth + "/asc"

        if not os.path.exists(pathOutputForASC+"/ndvi.asc"):

            if not os.path.exists(pathOutputForHDF):
                os.makedirs(pathOutputForHDF)
                #print("aqui")

            args = ['./Daac2Disk_ubuntu', '--shortname', 'MOD13A3', '--versionid', '006', '--begin',
                    workingWithDate.strftime("%Y-%m-%d"),
                    '--end', workingWithDate.strftime("%Y-%m-%d"), '--bbox', box_array[0], box_array[1], box_array[2],
                    box_array[3],
                    '--output', pathOutputForHDF]
            print("***Downloading NDVI")
            p = run(args, stdout=PIPE, input='y\n'+user+'\n'+password+'\n', encoding='ascii')
            result = p.returncode
            if result == 0:
                print("*****Processing with GDAL")
                pathOutputForTIF = localPath + "/"+uuid+"/"+country+"/" + pathPerMonth + "/tif"

                if not os.path.exists(pathOutputForTIF):
                    os.makedirs(pathOutputForTIF)

                error = False
                hdfs = glob(pathOutputForHDF + "/*.hdf")
                for hdf in hdfs:
                    args = ["gdal_translate", "-of", "GTiff",
                            'HDF4_EOS:EOS_GRID:' + hdf + ':MOD_Grid_monthly_1km_VI:1 km monthly NDVI',
                            hdf.replace("hdf", "tif")]
                    p = run(args, stdout=PIPE, encoding='ascii')
                    if p.returncode != 0:
                        error = True
                if not error:
                    pathOutputForMERGE = localPath + "/"+uuid+"/"+country+"/" + pathPerMonth + "/merge"

                    if not os.path.exists(pathOutputForMERGE):
                        os.makedirs(pathOutputForMERGE)

                    args = ['gdal_merge.py', '-n', '-3000', '-a_nodata', '-3000', '-of', 'GTiff', '-o',
                            pathOutputForMERGE + "/merge.tif"]
                    tifs = glob(pathOutputForTIF + "/*.tif")
                    if len(tifs) > 0:
                        for file in tifs:
                            args.append(file)
                        p = run(args, stdout=PIPE, encoding='ascii')
                        if p.returncode == 0:
                            args = ['gdalwarp', '-overwrite', '-t_srs', 'EPSG:4326', '-of', 'GTiff',
                                    pathOutputForMERGE + "/merge.tif",
                                    pathOutputForMERGE + "/merge_reproj.tif"]
                            p = run(args, stdout=PIPE, encoding='ascii')
                            if p.returncode == 0:
                                pathOutputForCLIPPER = localPath + "/"+uuid+"/"+country+"/" + pathPerMonth + "/clipper"
                                if not os.path.exists(pathOutputForCLIPPER):
                                    os.makedirs(pathOutputForCLIPPER)

                                args = ['gdalwarp', '-q', '-cutline', countriesPath + "/Countries/"+country+"/"+country+".shp",
                                        '-crop_to_cutline',
                                        '-tr',
                                        '0.00949328827817', '0.00949328827817', '-of', 'GTiff',
                                        pathOutputForMERGE + "/merge_reproj.tif",
                                        pathOutputForCLIPPER + "/clipper.tif"]
                                p = run(args, stdout=PIPE, encoding='ascii')
                                if p.returncode == 0:
                                    # pathOutputForASC = localPath + "/Data/" + pathPerMonth + "/asc"
                                    if not os.path.exists(pathOutputForASC):
                                        os.makedirs(pathOutputForASC)
                                    args = ['gdal_translate', '-a_nodata', '-3000', '-of', 'AAIGrid',
                                            pathOutputForCLIPPER + "/clipper.tif", pathOutputForASC + '/ndvi.asc']
                                    p = run(args, stdout=PIPE, encoding='ascii')
                                    if p.returncode == 0:
                                        print("*******Done processing with GDAL")
                                        importDataSet(required,pathOutputForASC+"/ndvi.asc",country)
                                        os.system("cp " + pathOutputForASC+"/ndvi.asc" + " " + pathForProcessed+"/"+required+".asc")
                                        print("")
                                        print("")
                                    else:
                                        print("Unable to convert final TIFF to ASCII. " + " ".join(args))
                                else:
                                    print("Unable to clip CR. " + " ".join(args))
                            else:
                                print("Unable to re-project Merge to Lat/Long. " + " ".join(args))
                        else:
                            print("Unable to merge TIFFs. " + " ".join(args))
                    else:
                        print("Warning no TIFFs to merge at " + pathOutputForTIF + "/*.tif")
                else:
                    print("Error converting HDF to TIFF. " + " ".join(args))
        else:
            print("Already exists the ndvi for the date: "+required)
            


