import act
import numpy as np
from xarray_schema import DataArraySchema, DatasetSchema
from xarray_schema.components import (
    DTypeSchema,
    DimsSchema,
    ShapeSchema,
    NameSchema,
    ChunksSchema,
    ArrayTypeSchema,
    AttrSchema,
    AttrsSchema,
)


def time_check(ds):
    err = []
    if 'time' not in list(ds.dims)[0]:
        err += 'Time is required to be the first dimension. S6.1.1'
    for v in ds:
        if (len(ds[v].dims) > 0) and ('time' not in list(ds[v].dims)[0]):
            err += v + ': Time is required to be the first dimension. S6.1.1'
        if (ds[v].size == 1) and (len(ds[v].dims) > 0):
            err += v + ': is not defined as a scalar. S6.1.1'

    for c in list(ds.coords):
        if c not in ds.dims:
            err += c + ': Coordinate is not included in dimensions. S6.1.1'

    if len(ds.dims) > 5:
        err += 'Please review and ensure that all the dimensions used are necessary or if they can be consolidated. S6.1.1'

    if any(np.isnan(ds['time'].values)):
        err += 'Time must not include NaNs'

    return err


ds = act.io.read_netcdf('./Data/sgpmetE13.b1/sgpmetE13.b1.20230322.000000.cdf')
errors = time_check(ds)
print(errors)

#ds['lon'] = ds['lon'].astype(int)
#ds['lat'] = ds['lat'].astype(str)

schema_base_time = DataArraySchema(dtype=np.datetime64, name='base_time')
schema_time_offset = DataArraySchema(dtype=np.datetime64, name='time_offset')
schema_lat = DataArraySchema(name='lat', dtype=np.float32)
schema_lon = DataArraySchema(name='lon', dtype=np.float32)

attr_schema_time = AttrsSchema(['long_name','units'])
schema_ds = DatasetSchema({
    'base_time': schema_base_time,
    'time_offset': schema_time_offset,
    'lat': schema_lat,
    'lon': schema_lon,
}
)

schema_lat.validate(ds['lat'])
schema_ds.validate(ds)
#dims_schema.validate(ds['temp_mean'])
