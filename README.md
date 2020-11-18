# RAPID access to the National Water Model
[![Documentation Status](https://readthedocs.org/projects/nwm/badge/?version=latest)](https://nwm.readthedocs.io/en/latest/?badge=latest)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/gantian127/nwm/blob/master/LICENSE.txt)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/rapid-research/rapid-nationalwatermodel/master?filepath=notebooks%2Fnwm-harvey.ipynb)

These examples Python library to fetch and process the National Water Model (NWM) NetCDF datasets. 

If you have any suggestion to improve the current function of the NWM python library, please create a github issue to connect with Tian
[here](https://github.com/gantian127/nwm/issues).
If you have any suggestion to improve the Notebooks used to customize access to NWM data, please create a github issue to connect with Christina [here](https://github.com/cband/nwm/issues).

## Online Resources and Steps to Get Oriented to the National Water Model

The [Story Map was developed for Hurricane Harvey](https://www.hydroshare.org/resource/8161a96a08474d12bba219852409be61/) to show  usable National Water Model results and provides access to operational forecasts ([learn more about this resource on HydroShare](https://www.hydroshare.org/resource/8161a96a08474d12bba219852409be61/).   

Here is a [National Water Model User Story](
https://www.esri.com/en-us/industries/water/segments/water-resources/national-water-model) with narrative description of how and why to use the National Water Model, provided by ESRI Water. 

[The U.S. Climate Resilence Toolkit uses the National Water Model to assess vulnerability and risk](https://toolkit.climate.gov/tool/national-water-model) and provides a helpful orientation to the model features. 

[National Water Model interactive Map](https://water.noaa.gov/map) is provided by the Office of Water Prediction (OWP) National Water Center provides water information products from version 2.0 of the National Water Model (NWM). Information about NWM products available through the OWP website can be found in this [Product Description Document](https://water.noaa.gov/documents/OWP-interface-PDD.pdf). Advisory: NWM products do not yet incorporate anthropogenic influence and should be used with some caution. The NWM is currently undergoing extensive validation and verification to identify where scientific updates to the model can make the most improvement. The next version of the NWM will be released in the late spring 2020 time frame. [Click here for more information about the NWM.](https://water.noaa.gov/about/nwm)

[WRF-Hydro HydroInspector](https://ral.ucar.edu/solutions/products/hydroinspector) is a state-of-the-art Web Mapping Service (WMS) that allows users to manipulate and interact with a host of hydrologic observation and hydrologic model output data. WRF-Hydro is the model used to generate National Water Model simulations. 

[Intelligent Earth Collective Notebooks](https://www.hydroshare.org/resource/86bf0fc015af49c49805b56f5a13bf21/)
are designed for developers and instructors of interactive curriculum for research and education using Python, Jupyter, and HydroShare.

Download subset maps and time series using the [National Water Model Data Viewer on HydroShare App](https://hs-apps.hydroshare.org/apps/nwm-forecasts/).

## Technical Steps to Get Started 

### Notebook User Instructions for interactive compute [CUAHSI Compute]

Go to HydroShare.org and login at www.hydroshare.org  

Do one time: Go to Collaborate, Find the CUAHSI Compute Group, Ask to Join.

Next time: Go directly to https://jupyterhub.cuahsi.org

New users: Get familiar with JupyterHub platform with [Juptyer Notebook new user instructions] and [JuptyerHub Documentation](https://jupyterhub.readthedocs.io/en/stable/index.html)

3. Launch CUAHSI JupyterHub (or go to jupyterhub.cuahsi.org) and choose the WaterHackWeek 2020 environment profile.
This environment will contain all the libraries that we need.

4. In the Jupyterlab view,  Create a new folder called "Github"` (this creates a folder in /home/jovyan/data)

5. Open an new "Terminal" session and clone the github repository by running the command:

The terminal opens in /home/jovyan/

```
> cd data

```
Make a new directory specific to your Github repositories on this server. 

```
> mkdir Github   

```
Clone the github repository by running the command:

```
> git clone https://github.com/christinab/nwm.git

```
### Notebook User Instructions for interactive compute on [CSDMS JupyterHub](https://www)
Work in Progress.

### Notebook User Instructions for interactive compute on [CyberGIS for Water](https://www.hydroshare.org/group/157)
Work in Progress.
 
### Developer Instructions

#### Install package

```
$ pip install nwm
```

#### Download NWM Data
You can launch binder to test and run the code below.

##### Example 1: use NwmHs class to download data (Recommended method)

```python
import matplotlib.pyplot as plt
from nwm import NwmHs

# get data from National water model HydroShare App
nwm_data = NwmHs()
dataset = nwm_data.get_data(archive='harvey', config='short_range', geom='channel_rt', variable='streamflow',
                           comid=[5781915], init_time=0, start_date='2017-08-23')

# show metadata
dataset.attrs

# plot data
plt.figure(figsize=(9,5))
dataset.plot()
plt.xlabel('Year 2017')
plt.ylabel('{} ({})'.format(dataset.variable_name,dataset.variable_unit))
plt.title('Short range streamflow forecast for Channel 5781915 during Harvey Hurricane Event')
```
![ts_plot](docs/source/_static/ts_plot.png)

##### Example 2: use BmiNwmHs class to download data (Demonstration of how to use BMI)

```python
import matplotlib.pyplot as plt
import numpy as np
import cftime

from nwm import BmiNwmHs


# initiate a data component
data_comp = BmiNwmHs()
data_comp.initialize('config_file.yaml')

# get variable info
var_name = data_comp.get_output_var_names()[0]
var_unit = data_comp.get_var_units(var_name)
print(' variable_name: {}\n var_unit: {}\n'.format(var_name, var_unit))

# get time info
start_time = data_comp.get_start_time()
end_time = data_comp.get_end_time()
time_step = data_comp.get_time_step()
time_unit = data_comp.get_time_units()
time_steps = int((end_time - start_time)/time_step) + 1
print(' start_time:{}\n end_time:{}\n time_step:{}\n time_unit:{}\n time_steps:{}\n'.format(start_time, end_time, time_step, time_unit, time_steps))

# initiate numpy arrays to store data
stream_value = np.empty(1)
stream_array = np.empty(time_steps)
cftime_array = np.empty(time_steps)

for i in range(0, time_steps):
    data_comp.get_value(var_name, stream_value)
    stream_array[i] = stream_value
    cftime_array[i] = data_comp.get_current_time()
    data_comp.update()

time_array = cftime.num2date(cftime_array, time_unit, only_use_cftime_datetimes=False, only_use_python_datetimes=True)

# plot data
plt.figure(figsize=(9,5))
plt.plot(time_array, stream_array)
plt.xlabel('Year 2017')
plt.ylabel('{} ({})'.format(var_name, var_unit))
plt.title('Short range streamflow forecast for Channel 5781915 during Harvey Hurricane Event')
```

We agree that the resulting products from work would be issued under a Creative Commons License Attribution-NonCommercial 4.0 International. 

We agreed to add language to any contract (below) that provides for me a non-exclusive, irrevocable, global, royalty-free license to the work produced, and that all publicly distributed copies of work prepared under this contract shall indicate the names of the author(s) [based on these community instructions]. 

The CONTRACTOR shall have a non-exclusive, irrevocable, global, royalty-free license to translate, reproduce and publicly distribute articles, reports, books, Powerpoint slides, Jupyter notebooks, videos, webcasts and any such material arising under this Contract for non-commercial purposes.

The CONTRACTOR agrees that payment listed purchases all print and electronic rights including electronic reproduction, transmission, display or distribution of work prepared under this Contract.  All publicly distributed copies of a copyrighted work prepared under this Contract shall indicate the name(s) of the author(s) of the work.


```

# REFERENCES

Arctur, D., E. Boghici (2018). Hurricane Harvey 2017 Story Map, HydroShare, https://doi.org/10.4211/hs.8161a96a08474d12bba219852409be61
