from sys import settrace 
import act
import matplotlib.pyplot as plt
import glob

# local trace function which returns itself 
def my_tracer(frame, event, arg = None): 
    # extracts frame code 
    code = frame.f_code 
  
    # extracts calling function name 
    func_name = code.co_name 
  
    # extracts the line number 
    line_no = frame.f_lineno 
  
    print(f"A {event} encountered in {func_name}() at line number {line_no} ") 
  
    return my_tracer 

settrace(my_tracer) 

file = glob.glob('./data/sgpmetE13.b1/*.202010*.cdf')
ds = act.io.read_arm_netcdf(file)
ds = act.qc.arm.add_dqr_to_qc(ds)

# Create Plot Display
display = act.plotting.TimeSeriesDisplay(ds, figsize=(10, 8), subplot_shape=(2,))

display.plot('temp_mean', subplot_index=(0,))
display.qc_flag_block_plot('temp_mean', subplot_index=(1,))
plt.tight_layout()
plt.show()

