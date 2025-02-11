import act
import glob
import xarray as xr
import os
print(act.__file__)

files = glob.glob('./data/sgpecorsfE39.b1/*.2023060*')
ds = act.io.arm.read_arm_netcdf(files)
ds = act.utils.datetime_utils.adjust_timestamp(ds)
ds.clean.cleanup()
ds = act.qc.arm.add_dqr_to_qc(ds)
ds.qcfilter.datafilter(del_qc_var=False, rm_assessments=['Bad', 'Incorrect', 'Indeterminate', 'Suspect'])


files = glob.glob('./data/sgpsebsE39.b1/*.2023060*')
ds_sebs = act.io.arm.read_arm_netcdf(files)
ds_sebs = act.utils.datetime_utils.adjust_timestamp(ds_sebs, offset=-30 * 60)
ds_sebs.clean.cleanup()
ds_sebs = act.qc.arm.add_dqr_to_qc(ds_sebs)
ds_sebs.qcfilter.datafilter(del_qc_var=False, rm_assessments=['Bad', 'Incorrect', 'Indeterminate', 'Suspect'])

files = glob.glob('./data/sgpstampE39.b1/*.2023060*')
ds_stamp = act.io.arm.read_arm_netcdf(files)
ds_stamp.clean.cleanup()
ds_stamp = act.qc.arm.add_dqr_to_qc(ds_stamp)
ds_stamp.qcfilter.datafilter(del_qc_var=False, rm_assessments=['Bad', 'Incorrect', 'Indeterminate', 'Suspect'])
#ds_stamp = ds_stamp.resample(time='30Min').mean()

files = glob.glob('./data/sgpstamppcpE39.b1/*.2023060*')
ds_stamppcp = act.io.arm.read_arm_netcdf(files)
ds_stamppcp.clean.cleanup()
ds_stamppcp = act.qc.arm.add_dqr_to_qc(ds_stamppcp)
ds_stamppcp.qcfilter.datafilter(del_qc_var=False, rm_assessments=['Bad', 'Incorrect', 'Indeterminate', 'Suspect'])
ds_stamppcp = ds_stamppcp.resample(time='30Min').sum()

files = glob.glob('./data/sgpamcE39.b1/*.2023060*')
ds_amc = act.io.arm.read_arm_netcdf(files)
ds_amc.clean.cleanup()
ds_amc = act.qc.arm.add_dqr_to_qc(ds_amc)
ds_amc.qcfilter.datafilter(del_qc_var=False, rm_assessments=['Bad', 'Incorrect', 'Indeterminate', 'Suspect'])

ds = xr.merge([ds, ds_sebs, ds_stamp, ds_stamppcp, ds_amc], compat='override')


df = act.io.ameriflux.convert_to_ameriflux(ds)

site = 'US-A14'

directory = './data/' + site + 'mergedflux/'
if not os.path.exists(directory):
    os.makedirs(directory)
filename = site + '_HH' +  str(df['TIMESTAMP_START'].iloc[0]) + '_' + str(df['TIMESTAMP_END'].iloc[-1]) + '.csv'
df.to_csv(directory + filename, index=False)
