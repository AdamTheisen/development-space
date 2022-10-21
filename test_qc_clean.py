import act
import pandas as pd
import numpy as np
import xarray as xr
import datetime

n_variables = 100
n_samples = 100

time = pd.date_range(
    start="2022-02-17 00:00:00",
    end="2022-02-18 00:00:00",
    periods=n_samples + 1,
)

# Create data variables and initialize QC variables to 0
noisy_data_mapping = {f"data_var_{i}": np.random.random(time.shape) for i in range(n_variables)}
qc_vars = {f"qc_data_var_{i}": np.zeros(time.shape) for i in range(n_variables)}
qc_vars.update(noisy_data_mapping)

ds = xr.Dataset(
    data_vars={name: ("time", data) for name, data in noisy_data_mapping.items()},
    coords={"time": time},
)


start = datetime.datetime.now()
for name, var in noisy_data_mapping.items():
    failed_qc = var > 0.75  # Consider data above 0.75 as bad. Negligible time here.
    ds.qcfilter.add_test(
        name,
        index=failed_qc,
        test_number=1,
        test_meaning="Value above threshold.",
        test_assessment="Bad",
    )
end = datetime.datetime.now()
print(f"Time elapsed = {(end-start)}")
