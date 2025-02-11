import h5py

filename = './data/NEON.D18.BARR.DP4.00200.001.nsae.2023-02.basic.20240122T085248Z.h5'

with h5py.File(filename, "r") as f:
    # Print all root level object names (aka keys) 
    # these can be group or dataset names 
    print("Keys: %s" % f.keys())
    # get first object name/key; may or may NOT be a group
    a_group_key = list(f.keys())[0]

    # get the object type for a_group_key: usually group or dataset
    print(a_group_key) 

    # If a_group_key is a group name, 
    # this gets the object names in the group and returns as a list
    data = list(f[a_group_key])

    # If a_group_key is a dataset name, 
    # this gets the dataset values and returns as a list
    data = list(f[a_group_key])
    # preferred methods to get dataset values:

    ds_obj = f[a_group_key]      # returns as a h5py dataset object
    print(ds_obj['dp04']['data'].keys())
