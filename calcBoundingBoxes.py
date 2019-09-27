# calcBoundingBoxes.py

import osgeo.ogr

def getBBox(shapeFile):

    shapefile = osgeo.ogr.Open(shapeFile)
    layer = shapefile.GetLayer(0)

    for i in range(layer.GetFeatureCount()):
        feature = layer.GetFeature(i)

    geometry = feature.GetGeometryRef()

    return geometry.GetEnvelope()
