import argparse
import math

import matplotlib as mpl
import pandas as pd
import simplekml
from polycircles import polycircles

LATITUDE_COL = "Latitude"
LONGITUDE_COL = "Longitude"
ALTITUDE_COL = "Altitude"


def parseArgs():
    parser = argparse.ArgumentParser(
        description='Generates a KML file from a CSV file \
                                given a target field. Assumes the presence of columns named "time", "Latitude", "Longitude", "Altitude".'
    )
    parser.add_argument("--target", nargs=1, help="target field to plot from the CSV file", required=True)
    parser.add_argument("--targetUnits", nargs="?", type=str, default=" ", help="units of the target field, displayed along with target value at each data point.", required=False)
    parser.add_argument("--colorMin", nargs="?", type=float, default=None, help="min value of the target field, used as lower limit to clip the color map.", required=False)
    parser.add_argument("--colorMax", nargs="?", type=float, default=None, help="max value of the target field, used as upper limit to clip the color map.", required=False)
    parser.add_argument(
        "--output",
        nargs="?",
        help="kml output file - \
                        default is same as target string",
        required=False,
    )
    parser.add_argument("--colormap", nargs="?", default="jet", required=False, help="colormap to use - default is jet")
    parser.add_argument("--smooth", nargs="?", type=int, default=1, required=False, help="colormap to use - default is jet")
    parser.add_argument("--linewidth", nargs="?", type=int, default=10, required=False, help="linewidth for the kml file - default is 10")
    parser.add_argument("--customLabel", nargs="?", type=str, default=None, help="custom text label attached to each geometry in the KML and displayed on click.", required=False)
    parser.add_argument("--labelCols", nargs="+", default=[], help="Fields to display in the pop-up label. Please also provide --labelUnits along with --labelCols.")
    parser.add_argument("--labelUnits", nargs="+", default=[], help="Units of the fields to display in the pop-up label.")

    parser.add_argument("csvFile", nargs=1, type=argparse.FileType("r"), help="CSV Log File")

    args = parser.parse_args()
    if args.output == None:
        args.output = args.target[0] + ".kml"
    return vars(args)


# Reads the csv file (needs to have headers) and returns a pandas data frame
def readCSV(csvFile):
    csvFileData = pd.read_csv(csvFile, index_col="time", parse_dates=True)
    return csvFileData


# Creates a popup label, given the
# row
# label fields
# corresponding label field units
# target value
# target units
# any custom label
def createGeomDescription(row, labelCols, labelUnits, targetString, targetUnits, customLabel):
    lat = row[LATITUDE_COL]
    lon = row[LONGITUDE_COL]
    alt = row[ALTITUDE_COL]
    description = f"<p><strong>{customLabel}</strong></p>" if customLabel else ""
    description += f"<p>{targetString} = {row[targetString]} {targetUnits}</p>\
                    <p>(lat, lon) = ({lat},{lon})</p><p> altitude = {alt} m</p>"

    if len(labelUnits) != len(labelCols):
        raise Exception("Length of label units should be equal to length of label fields.")

    for labelField, labelUnit in zip(labelCols, labelUnits):
        description += f"<p>{labelField} = {row[labelField]} {labelUnit}</p>"

    return description


# Generates and saves a KML file given
#  - the data in the csvFileData (a pandas dataframe)
#  - the target string (what column to plot)
#  - the target units (optional)
#  - the color bar min value (optional)
#  - the color bar max value (optional)
#  - output file name for the kml file
#  - colorMap
#  - smooth rate
#  - custom label
#  - label fields
#  - label field units
def generateKML(csvFileData, targetString, targetUnits, colorMin, colorMax, outputFileName, colorMap, linewidth, smoothRate, customLabel, labelCols, labelUnits):
    zeColorMap = mpl.colormaps[colorMap]
    kml = simplekml.Kml()

    minVal = colorMin if colorMin else csvFileData[targetString].min()
    maxVal = colorMax if colorMax else csvFileData[targetString].max()

    prev_loc = None
    row_int_pos = 0
    for index, row in csvFileData.iterrows():
        scaledValue = (row[targetString] - minVal) / (maxVal - minVal)
        rgb_r = zeColorMap(scaledValue)
        lon = row[LONGITUDE_COL]
        lat = row[LATITUDE_COL]
        alt = row[ALTITUDE_COL]

        emp = math.isnan(lon) or math.isnan(lat) or math.isnan(alt)

        if emp:
            continue

        zeColor = simplekml.Color.rgb(int(rgb_r[0] * 255), int(rgb_r[1] * 255), int(rgb_r[2] * 255))
        pc = polycircles.Polycircle(latitude=lat, longitude=lon, radius=1, number_of_vertices=12)
        res = pc.to_kml()
        all = []
        for i in res:
            withAlt = list(i)
            withAlt.append(float(alt))
            all.append(withAlt)
        cir = kml.newpolygon(name=row[targetString], outerboundaryis=all)
        cir.style.polystyle.color = zeColor
        cir.altitudemode = simplekml.AltitudeMode.relativetoground
        cir.description = createGeomDescription(row, labelCols, labelUnits, targetString, targetUnits, customLabel)

        #        if False:
        #            pnt = kml.newpoint()
        #            pnt.altitudemode = simplekml.AltitudeMode.relativetoground
        #            pnt.name = row[targetString]
        #            pnt.coords = [(lon, lat, alt)]

        #            pnt.style.balloonstyle.text = row[targetString]
        #            pnt.style.balloonstyle.textcolor = zeColor
        #            pnt.style.balloonstyle.scale = 0.1
        #            pnt.style.balloonstyle.displayMode = simplekml.DisplayMode.hide
        #        pnt.style.labelstyle.color = zeColor  # Make the text match
        #        pnt.style.labelstyle.scale = 0.5  # Make the text twice as big
        #        pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'

        if linewidth > 0:
            ind = csvFileData.index.get_loc(index)
            for step in range(smoothRate):
                ls = kml.newlinestring()
                ls.name = row[targetString]
                ls.label = row[targetString]
                ls.altitudemode = simplekml.AltitudeMode.relativetoground
                ls.style.linestyle.width = linewidth
                ls.style.linestyle.color = zeColor
                ls.style.linestyle.gxlabelvisibility = True

                if not prev_loc:  # first data point is just a point
                    ls.coords = [(lon, lat, alt)]
                    prev_loc = (lon, lat, alt)
                else:  # all the others are segments
                    # Gradient operation
                    if (ind + 1) >= len(csvFileData.index):
                        continue
                    _f_row = csvFileData.iloc[(ind + 1)]
                    _f_loc = (_f_row[LONGITUDE_COL], _f_row[LATITUDE_COL], _f_row[ALTITUDE_COL])
                    _f_val = (_f_row[targetString] - minVal) / (maxVal - minVal)
                    ratio = step / smoothRate

                    _lon = round(lon + (_f_loc[0] - lon) * ratio, 6)
                    _lat = round(lat + (_f_loc[1] - lat) * ratio, 6)
                    _alt = abs(round(alt + (_f_loc[2] - alt) * ratio, 3))

                    _rgb_c = zeColorMap(scaledValue)
                    _rgb_p = zeColorMap(_f_val)

                    _rgb_0 = (_rgb_c[0] + (_rgb_p[0] - _rgb_c[0]) * ratio) * 255
                    _rgb_1 = (_rgb_c[1] + (_rgb_p[1] - _rgb_c[1]) * ratio) * 255
                    _rgb_2 = (_rgb_c[2] + (_rgb_p[2] - _rgb_c[2]) * ratio) * 255

                    zeColor = simplekml.Color.rgb(int(_rgb_0), int(_rgb_1), int(_rgb_2))
                    ls.style.linestyle.color = zeColor
                    ls.coords = [(_lon, _lat, _alt), prev_loc]
                    prev_loc = (_lon, _lat, _alt)

        row_int_pos += 1

    # Saves the kml file
    kml.save(outputFileName)


def main():
    args = parseArgs()
    # Define args for drawtype (line or point or both)
    csvFileData = readCSV(args["csvFile"][0])
    generateKML(csvFileData, args["target"][0], args["targetUnits"], args["colorMin"], args["colorMax"], args["output"], args["colormap"], args["linewidth"], args["smooth"], args["customLabel"], args["labelCols"], args["labelUnits"])


if __name__ == "__main__":
    # testOne()
    main()
