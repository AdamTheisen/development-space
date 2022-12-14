import pyproj
projection_string = (
    'PROJCS["NAD_1983_Albers",'
    'GEOGCS["NAD83",'
    'DATUM["North_American_Datum_1983",'
    'SPHEROID["GRS 1980",6378137,298.257222101,'
    'AUTHORITY["EPSG","7019"]],'
    'TOWGS84[0,0,0,0,0,0,0],'
    'AUTHORITY["EPSG","6269"]],'
    'PRIMEM["Greenwich",0,'
    'AUTHORITY["EPSG","8901"]],'
    'UNIT["degree",0.0174532925199433,'
    'AUTHORITY["EPSG","9108"]],'
    'AUTHORITY["EPSG","4269"]],'
    'PROJECTION["Albers_Conic_Equal_Area"],'
    'PARAMETER["standard_parallel_1",29.5],'
    'PARAMETER["standard_parallel_2",45.5],'
    'PARAMETER["latitude_of_center",23],'
    'PARAMETER["longitude_of_center",-96],'
    'PARAMETER["false_easting",0],'
    'PARAMETER["false_northing",0],'
    'UNIT["meters",1]]')

outproj = pyproj.CRS(projection_string)
inproj = pyproj.Proj("+init=EPSG:4326")

lon, lat = (-97.1709,36.8172)

x,y = pyproj.transform(inproj,outproj,lon,lat)


print(x,y)
