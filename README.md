# las-to-cesium
Getting custom point data into Cesium 

The example should work by running `pip install .` from the root directory and then running `las-to-cesium`.

You might wish to create a virtual environment to install the example into by running 
`
python -m venv env
` 
and activating it by 
`
env/Scripts/activate
`

The resulting LAS file is called `data.las` and it's dumped into the root (or wherever you called the script from). 
It takes a single positional argument which is a path to a folder containing `.kml` files to be parsed.

A sample data file is provided in `data/single-flight`, so it's possible to call

`las-to-cesium data/single-flight` 

from the root directory.

After loading both the `.kml` file and the `data.las` file the positions do not match. 
A screenshot of the result can be found in `result.PNG`. 

I still didn't figure out how to geo-code the las file so the location of the origin of the dataset 
is written to the standard output.