#! /usr/bin/env python3

import numpy as np
import numpy.ma as ma
import warnings
import argparse
from scipy.optimize import brent, brentq
import copy
from dqlib.io.data import read_arm_data_act
import xarray as xr
from os import environ
from datetime import datetime
from datetime import timedelta
import time
from pathlib import Path

def get_irt_coeff():

    data = [[84713.3,0.00000],
        [84761.5,0.00174289],
        [84809.7,0.00710459],
        [84857.9,0.0124663],
        [84906.1,0.0178273],
        [84954.3,0.0231883],
        [85002.6,0.0285500],
        [85050.8,0.0339117],
        [85099.0,0.0392728],
        [85147.2,0.0446338],
        [85195.4,0.0499646],
        [85243.6,0.0552360],
        [85291.8,0.0605068],
        [85340.1,0.0657776],
        [85388.3,0.0710491],
        [85436.5,0.0763205],
        [85484.7,0.0815913],
        [85532.9,0.0868621],
        [85581.1,0.0921336],
        [85629.3,0.0974050],
        [85677.6,0.102676],
        [85725.8,0.107947],
        [85774.0,0.113218],
        [85822.2,0.118490],
        [85870.4,0.123760],
        [85918.6,0.129031],
        [85966.8,0.134303],
        [86015.1,0.139574],
        [86063.3,0.145822],
        [86111.5,0.160960],
        [86159.7,0.176101],
        [86207.9,0.191241],
        [86256.1,0.206380],
        [86304.3,0.221519],
        [86352.6,0.236659],
        [86400.8,0.251800],
        [86449.0,0.266938],
        [86497.2,0.282077],
        [86545.4,0.297217],
        [86593.6,0.312358],
        [86641.9,0.327496],
        [86690.1,0.342635],
        [86738.3,0.357776],
        [86786.5,0.372916],
        [86834.7,0.388055],
        [86882.9,0.403193],
        [86931.1,0.418334],
        [86979.4,0.432545],
        [87027.6,0.445724],
        [87075.8,0.458903],
        [87124.0,0.472084],
        [87172.2,0.485265],
        [87220.4,0.498444],
        [87268.6,0.511623],
        [87316.9,0.524804],
        [87365.1,0.537984],
        [87413.3,0.551163],
        [87461.5,0.564343],
        [87509.7,0.577523],
        [87557.9,0.590704],
        [87606.1,0.603883],
        [87654.4,0.617062],
        [87702.6,0.630243],
        [87750.8,0.643424],
        [87799.0,0.656603],
        [87847.2,0.669782],
        [87895.4,0.676795],
        [87943.7,0.676418],
        [87991.9,0.676041],
        [88040.1,0.675665],
        [88088.3,0.675288],
        [88136.5,0.674911],
        [88184.7,0.674534],
        [88232.9,0.674158],
        [88281.2,0.673781],
        [88329.4,0.673404],
        [88377.6,0.673028],
        [88425.8,0.672651],
        [88474.0,0.672274],
        [88522.2,0.671898],
        [88570.4,0.671521],
        [88618.7,0.671144],
        [88666.9,0.670767],
        [88715.1,0.670391],
        [88763.3,0.670014],
        [88811.5,0.669627],
        [88859.7,0.668940],
        [88907.9,0.668252],
        [88956.2,0.667565],
        [89004.4,0.666878],
        [89052.6,0.666190],
        [89100.8,0.665503],
        [89149.0,0.664816],
        [89197.2,0.664129],
        [89245.4,0.663441],
        [89293.7,0.662754],
        [89341.9,0.662067],
        [89390.1,0.661379],
        [89438.3,0.660692],
        [89486.5,0.660005],
        [89534.7,0.659317],
        [89582.9,0.658630],
        [89631.2,0.657943],
        [89679.4,0.657255],
        [89727.6,0.656568],
        [89775.8,0.656010],
        [89824.0,0.655997],
        [89872.2,0.655984],
        [89920.5,0.655972],
        [89968.7,0.655959],
        [90016.9,0.655947],
        [90065.1,0.655934],
        [90113.3,0.655922],
        [90161.5,0.655909],
        [90209.7,0.655896],
        [90258.0,0.655884],
        [90306.2,0.655871],
        [90354.4,0.655859],
        [90402.6,0.655846],
        [90450.8,0.655834],
        [90499.0,0.655821],
        [90547.2,0.655808],
        [90595.5,0.655796],
        [90643.7,0.655783],
        [90691.9,0.655771],
        [90740.1,0.655758],
        [90788.3,0.656199],
        [90836.5,0.656682],
        [90884.7,0.657164],
        [90933.0,0.657646],
        [90981.2,0.658129],
        [91029.4,0.658611],
        [91077.6,0.659093],
        [91125.8,0.659576],
        [91174.0,0.660058],
        [91222.3,0.660540],
        [91270.5,0.661023],
        [91318.7,0.661505],
        [91366.9,0.661987],
        [91415.1,0.662470],
        [91463.3,0.662952],
        [91511.5,0.663434],
        [91559.8,0.663917],
        [91608.0,0.664399],
        [91656.2,0.664881],
        [91704.4,0.665364],
        [91752.6,0.665817],
        [91800.8,0.666153],
        [91849.0,0.666489],
        [91897.3,0.666824],
        [91945.5,0.667160],
        [91993.7,0.667496],
        [92041.9,0.667832],
        [92090.1,0.668167],
        [92138.3,0.668503],
        [92186.5,0.668839],
        [92234.8,0.669175],
        [92283.0,0.669510],
        [92331.2,0.669846],
        [92379.4,0.670182],
        [92427.6,0.670518],
        [92475.8,0.670853],
        [92524.0,0.671189],
        [92572.3,0.671525],
        [92620.5,0.671861],
        [92668.7,0.672197],
        [92716.9,0.672532],
        [92765.1,0.672856],
        [92813.3,0.672365],
        [92861.5,0.671875],
        [92909.8,0.671384],
        [92958.0,0.670894],
        [93006.2,0.670403],
        [93054.4,0.669913],
        [93102.6,0.669422],
        [93150.8,0.668932],
        [93199.1,0.668441],
        [93247.3,0.667951],
        [93295.5,0.667460],
        [93343.7,0.666970],
        [93391.9,0.666479],
        [93440.1,0.665989],
        [93488.3,0.665498],
        [93536.6,0.665008],
        [93584.8,0.664517],
        [93633.0,0.664027],
        [93681.2,0.663536],
        [93729.4,0.663046],
        [93777.6,0.662555],
        [93825.8,0.662009],
        [93874.1,0.661364],
        [93922.3,0.660719],
        [93970.5,0.660074],
        [94018.7,0.659428],
        [94066.9,0.658783],
        [94115.1,0.658138],
        [94163.3,0.657493],
        [94211.6,0.656847],
        [94259.8,0.656202],
        [94308.0,0.655557],
        [94356.2,0.654912],
        [94404.4,0.654266],
        [94452.6,0.653621],
        [94500.9,0.652976],
        [94549.1,0.652331],
        [94597.3,0.651685],
        [94645.5,0.651040],
        [94693.7,0.650395],
        [94741.9,0.649750],
        [94790.1,0.649104],
        [94838.4,0.648459],
        [94886.6,0.647795],
        [94934.8,0.647056],
        [94983.0,0.646317],
        [95031.2,0.645579],
        [95079.4,0.644840],
        [95127.6,0.644101],
        [95175.9,0.643362],
        [95224.1,0.642624],
        [95272.3,0.641885],
        [95320.5,0.641146],
        [95368.7,0.640407],
        [95416.9,0.639669],
        [95465.1,0.638930],
        [95513.4,0.638191],
        [95561.6,0.637452],
        [95609.8,0.636714],
        [95658.0,0.635975],
        [95706.2,0.635236],
        [95754.4,0.634497],
        [95802.6,0.633758],
        [95850.9,0.633020],
        [95899.1,0.632281],
        [95947.3,0.631542],
        [95995.5,0.630741],
        [96043.7,0.629888],
        [96091.9,0.629034],
        [96140.1,0.628181],
        [96188.4,0.627327],
        [96236.6,0.626474],
        [96284.8,0.625620],
        [96333.0,0.624767],
        [96381.2,0.623913],
        [96429.4,0.623060],
        [96477.7,0.622206],
        [96525.9,0.621353],
        [96574.1,0.620499],
        [96622.3,0.619646],
        [96670.5,0.618793],
        [96718.7,0.617939],
        [96766.9,0.617086],
        [96815.2,0.616232],
        [96863.4,0.615379],
        [96911.6,0.614525],
        [96959.8,0.613672],
        [97008.0,0.612818],
        [97056.2,0.611965],
        [97104.4,0.611181],
        [97152.7,0.610524],
        [97200.9,0.609867],
        [97249.1,0.609211],
        [97297.3,0.608554],
        [97345.5,0.607897],
        [97393.7,0.607241],
        [97441.9,0.606584],
        [97490.2,0.605927],
        [97538.4,0.605271],
        [97586.6,0.604614],
        [97634.8,0.603957],
        [97683.0,0.603301],
        [97731.2,0.602644],
        [97779.5,0.601987],
        [97827.7,0.601330],
        [97875.9,0.600674],
        [97924.1,0.600017],
        [97972.3,0.599360],
        [98020.5,0.598704],
        [98068.7,0.598047],
        [98117.0,0.597390],
        [98165.2,0.596734],
        [98213.4,0.596077],
        [98261.6,0.595829],
        [98309.8,0.595833],
        [98358.0,0.595837],
        [98406.2,0.595841],
        [98454.5,0.595845],
        [98502.7,0.595850],
        [98550.9,0.595854],
        [98599.1,0.595858],
        [98647.3,0.595862],
        [98695.5,0.595866],
        [98743.8,0.595871],
        [98792.0,0.595875],
        [98840.2,0.595879],
        [98888.4,0.595883],
        [98936.6,0.595887],
        [98984.8,0.595892],
        [99033.0,0.595896],
        [99081.2,0.595900],
        [99129.5,0.595904],
        [99177.7,0.595908],
        [99225.9,0.595913],
        [99274.1,0.595917],
        [99322.3,0.595921],
        [99370.5,0.595925],
        [99418.8,0.595476],
        [99467.0,0.594039],
        [99515.2,0.592601],
        [99563.4,0.591164],
        [99611.6,0.589727],
        [99659.8,0.588289],
        [99708.0,0.586852],
        [99756.3,0.585414],
        [99804.5,0.583977],
        [99852.7,0.582540],
        [99900.9,0.581102],
        [99949.1,0.579665],
        [99997.3,0.578228],
        [100046.,0.576790],
        [100094.,0.575353],
        [100142.,0.573915],
        [100190.,0.572478],
        [100238.,0.571040],
        [100287.,0.569603],
        [100335.,0.568166],
        [100383.,0.566728],
        [100431.,0.565291],
        [100480.,0.563853],
        [100528.,0.562416],
        [100576.,0.560979],
        [100624.,0.558845],
        [100672.,0.555772],
        [100721.,0.552700],
        [100769.,0.549627],
        [100817.,0.546554],
        [100865.,0.543481],
        [100913.,0.540409],
        [100962.,0.537336],
        [101010.,0.534263],
        [101058.,0.531190],
        [101106.,0.528117],
        [101154.,0.525045],
        [101203.,0.521972],
        [101251.,0.518899],
        [101299.,0.515826],
        [101347.,0.512754],
        [101396.,0.509681],
        [101444.,0.506608],
        [101492.,0.503535],
        [101540.,0.500463],
        [101588.,0.497390],
        [101637.,0.494317],
        [101685.,0.491244],
        [101733.,0.488172],
        [101781.,0.485099],
        [101829.,0.482026],
        [101878.,0.475226],
        [101926.,0.468134],
        [101974.,0.461041],
        [102022.,0.453948],
        [102071.,0.446856],
        [102119.,0.439764],
        [102167.,0.432671],
        [102215.,0.425578],
        [102263.,0.418486],
        [102312.,0.411394],
        [102360.,0.404301],
        [102408.,0.397208],
        [102456.,0.390116],
        [102504.,0.383023],
        [102553.,0.375930],
        [102601.,0.368837],
        [102649.,0.361744],
        [102697.,0.354653],
        [102746.,0.347560],
        [102794.,0.340467],
        [102842.,0.333376],
        [102890.,0.326283],
        [102938.,0.319190],
        [102987.,0.312097],
        [103035.,0.305004],
        [103083.,0.297913],
        [103131.,0.291300],
        [103180.,0.284812],
        [103228.,0.278325],
        [103276.,0.271837],
        [103324.,0.265349],
        [103372.,0.258860],
        [103421.,0.252372],
        [103469.,0.245886],
        [103517.,0.239397],
        [103565.,0.232909],
        [103613.,0.226422],
        [103662.,0.219934],
        [103710.,0.213446],
        [103758.,0.206958],
        [103806.,0.200470],
        [103855.,0.193983],
        [103903.,0.187495],
        [103951.,0.181007],
        [103999.,0.174520],
        [104047.,0.168032],
        [104096.,0.161543],
        [104144.,0.155055],
        [104192.,0.148567],
        [104240.,0.142080],
        [104288.,0.135592],
        [104337.,0.129104],
        [104385.,0.122684],
        [104433.,0.119882],
        [104481.,0.117080],
        [104530.,0.114279],
        [104578.,0.111477],
        [104626.,0.108676],
        [104674.,0.105874],
        [104722.,0.103072],
        [104771.,0.100271],
        [104819.,0.0974696],
        [104867.,0.0946679],
        [104915.,0.0918662],
        [104963.,0.0890645],
        [105012.,0.0862635],
        [105060.,0.0834618],
        [105108.,0.0806601],
        [105156.,0.0778591],
        [105205.,0.0750574],
        [105253.,0.0722556],
        [105301.,0.0694539],
        [105349.,0.0666522],
        [105397.,0.0638512],
        [105446.,0.0610495],
        [105494.,0.0582478],
        [105542.,0.0554468],
        [105590.,0.0526451],
        [105638.,0.0498433],
        [105687.,0.0470416],
        [105735.,0.0439777],
        [105783.,0.0407067],
        [105831.,0.0374349],
        [105880.,0.0341630],
        [105928.,0.0308920],
        [105976.,0.0276202],
        [106024.,0.0243483],
        [106072.,0.0210765],
        [106121.,0.0178046],
        [106169.,0.0145336],
        [106217.,0.0112618],
        [106265.,0.00798992],
        [106313.,0.00471891],
        [106362.,0.00144707],
        [106410.,0.00000]]

    return np.array(data, dtype=np.float32)

def planck_function(temperature=np.array([])):
    """
    Convert surface temperature into radiances useing IRT response function
    """

    try:
        temperature.size
        temp = copy.copy(temperature)
    except AttributeError:
        temp = np.array([temperature])

    if False:
        coeff = get_irt_coeff()
        dtype = coeff.dtype # Data type set from coeff data type. All values are converted to that.
        v = coeff[:,0]  # Wavenumber in 1/m
        S = coeff[:,1]  # Response function
        C1 = 1.191062E-16  # 2*hc^2  [W m^2]
        C2 = 1.438786E-2  # hc/kb   [m K]
        bshape = (temp.size, v.size)

        # Calculate numerator of function broadcaseted to (temp size, wavenum size)
        planck_num = np.broadcast_to(C1 * v**3, bshape).astype(dtype)
        planck_dem = np.broadcast_to(C2 * v, bshape).astype(dtype)

        # Calculate the demoninator using temperature broadcasted to (temp size, wavenum size)
        # Ensure datatype stats to dtype
        planck_dem = np.exp(planck_dem / (temp.reshape(temp.size, 1).astype(dtype) - 1.0))
        planck = planck_num / planck_dem
        planck = np.broadcast_to(S, bshape) * planck

        # Sum along temperature dimension
        planck = np.nansum(planck, axis=1)

    else:
        coeff = get_irt_coeff()
        dtype = coeff.dtype # Data type set from coeff data type. All values are converted to that.
        v = coeff[:,0]  # Wavenumber in 1/m
        S = coeff[:,1]  # Response function
        L = np.full(temp.size, np.nan)
        C1 = 1.191062E-16  # 2*hc^2  [W m^2]
        C2 = 1.438786E-2  # hc/kb   [m K]

        for jj in range(temp.size):
            planck = (C1 * v**3) / (np.exp(C2 * v / temp[jj]) - 1.0)
            L[jj] = np.sum(S * planck)
        planck = L

    return planck.astype(dtype)


def calculate_sst(sky_ir_temp, sea_ir_temp, emis, maxit=500, tempLow=250,
                  tempHigh=350, tol=0.1):

    # Convert IR temperatures into radiance
    Lsurf = planck_function(sea_ir_temp)
    Lsky = planck_function(sky_ir_temp)

    # Correct sea surface brightness temperature for sky brightness
    # temperature useing Donlon (2008).
    Lsst = (Lsurf - (1.0 - emis) * Lsky) / emis
    Lsst.astype(Lsurf.dtype)

    # Invert integral to get temperatures
    sst = np.full(sky_ir_temp.size, np.nan, dtype=Lsurf.dtype)
    min_function = lambda x, y: planck_function(x) - y
    for ii in range(Lsst.size):
        if np.isnan(Lsst[ii]):
            continue
#            sst[ii] = Lsst[ii]
        else:
            sst[ii] = brentq(min_function, tempLow, tempHigh,
                             args=(Lsst[ii],), xtol=tol, maxiter=maxit)

    return sst.astype(Lsurf.dtype)


def parse_arguments():
    """Configure and return command line arguments"""
    parser = argparse.ArgumentParser(
            description="A description for this script",
            epilog="An epilog for the help")

#    parser.add_argument("requiredArg")
    parser.add_argument("-s", "--startdate",
                        type=str,
                        default=None,
                        help='Startdate in YYYYMMDD format')
    parser.add_argument("-e", "--enddate",
                        type=str,
                        default=None,
                        help='Enddate in YYYYMMDD format')
    parser.add_argument("-r", "--readpath",
                        type=str,
                        default='.',
                        help='Data file location full path')
    parser.add_argument("-w", "--writepath",
                        type=str,
                        default='.',
                        help='Output file location full path')
    parser.add_argument("-D", "--datastream",
                        type=str,
                        help='ARM Datastream name')

    emis = 0.986
    parser.add_argument("-E", "--emissivity",
                        default=emis,
                        type=float,
                        help=f"Optional, set emissivity for calculations. "
                             f"Default is {emis} .")

    args = parser.parse_args()

    return args

def update_attributes(ds_object):

    for var_name in ds_object.data_vars:
        for att_name in ['flag_meanings', 'flag_assessments']:

            try:
                att_value = [att.replace(' ', '-') for att in
                                 ds_object[var_name].attrs[att_name]]
                att_value = ' '.join(att_value)
                ds_object[var_name].attrs[att_name] = att_value
            except KeyError:
                pass

def main():
    """
    Program to calculate Skin Sea Surface Temperature from IRT data
    """
    # Get arguments from command line
    args=parse_arguments()

    readpath = Path(args.readpath)
    files = sorted(readpath.glob('*.nc'))
    files.extend(sorted(readpath.glob('*.cdf')))
    if len(files) == 0:
        print(f"\nNo data files for '{args.datastream}' in path '{readpath}'\n")
        return

    sd = datetime.strptime(args.startdate, "%Y%m%d")
    rundate = sd
    if args.enddate is None:
        ed = copy.copy(sd)
    else:
        ed = datetime.strptime(args.enddate, "%Y%m%d")

    for fl in files:
        date = fl.name.split('.')[2]
        rundate = datetime.strptime(date, "%Y%m%d")

        if rundate < sd or rundate > ed:
            continue

        ds_object = read_arm_data_act(filename=str(fl))

        if ds_object is None:
            continue

        print(f"Processing data for {fl.name}")

        for attrs in ['file_dates', 'file_times', 'arm_standards_flag', '__source_files',
                      '_file_dates', '_file_times', '_arm_standards_flag',
                      '_source_files']:
            try:
                del ds_object.attrs[attrs]
            except KeyError:
                pass

       # Reduce size for testing
#        ds_object = ds_object.isel(time=slice(None, 5))

        sst = calculate_sst(ds_object['sky_ir_temp'].values,
                            ds_object['sfc_ir_temp'].values, args.emissivity)

        new_var_name = 'sea_surface_temp'
        ds_object[new_var_name] = (
            'time', sst, {'long_name': 'Derived sea surface temperature', 'units': 'K'}
        )

        hist_name = 'history'
        try:
            machine = environ['HOST']
        except KeyError:
            machine = 'HOST'

        try:
            user = environ['USER']
        except KeyError:
            user = 'USER'

        history = ds_object.attrs[hist_name]
        history = (history + f" ;\n Updated to include {new_var_name} "
                   f"by {user} on machine {machine} at "
                   f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        ds_object.attrs[hist_name] = history

        writepath = Path(args.writepath)
        writepath.mkdir(parents=True, exist_ok=True)
        time = ds_object['time'].values[0].astype('datetime64[s]').astype(int)
        time = datetime.utcfromtimestamp(time).strftime("%H%M%S")
        filename = '.'.join((args.datastream, date, time,'nc'))
        filename = Path(writepath, filename)
        print(f"Writing {filename}")
        update_attributes(ds_object)
        encoding = {'time': {'_FillValue': None}}
        ds_object.to_netcdf(path=filename, mode='w', format='NETCDF4',
                            engine='netcdf4', encoding=encoding)
        del ds_object


if __name__ == '__main__':
    start_time = time.time()
    main()
    print(time.time() - start_time)
