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

An example in the Cesium ION can be accessed via this url:

https://sandcastle.cesium.com/#c=pVRrb9owFP0rFh+mICEH2nUdLa3W0YmFFbaWtBso0mSSC3h17Mx2oGTqf58dB9qu7R7ap+Drc84992F8H/Uk4Rp1QdE87Y8QiWNQCmmB1iKXiAqOiFKgVcQdBgeC4wRmJGf6pASH4ho4OkJRDdb9xbQX04+0H1wWQWtIAxXwi724G7wKrrMvV91+GxvQ96R3bUFsmAYvh58vFpNRc29cjHfOwvPWMB3rcXq+GqybxSQdt4Y774phL2hNvgX0rNvPJkZsUJw3h4URT9kisedwvBqcDprDML4Z7DaxVu1+N2zRnX1SdHVb0JuvcjB9uSjeLpLeW7hM+L6eX7yf5Pwyqh1GPOJLItGSwgqkqYTDquoIvipjXlSLy3NXcE0oBxnVGuhHxBHSIKWJfJJiSROQB/fJ7hM+RHglDaFcsgN019MLUKbhMeCZFOmJbXmQeK16w4Jv7ee2bow6i1jFwAHPmZiCmUWmFyEofTI3WZSu0pkytMxhW5ymDIyoCT/QyCRNqaZLUJgkiWezPSpg9zR05H+xvtfabbe3/iNeL51ULrAEkqxNR1KqwCKwXgD3ZjmPtV05r46qVJXZQog0FF5Fd1r22vfRSZaxNTJ8VG0lUnrNANEZohrBDVV2eUst0wa40ZIo25zKSbnd2IUPHc4wPfcLbao00mbqiedwdfTixW8B2BTxV6DNSxpZy3UH39aOtiZdRUfPjaZkP6taVXW7mYTptjDtkivT+3stN2sj5DZ3LLgSDDAT8+rm0PHL1ruVytz8jK8/7UKz3X7drj81aFnht4kl6FzyjeKHlJ0STUZOkwmSbBmNuzbFJAVJDh5utgs27jDGs3qEscEKc7sp8SmfydbFr04rwTuAe0n3CP8jWy3+M2r/N8dao9YpN+vYht7QNBNS28ftYexrSDNGNCh/msfXZgdjpSyp428onYQuEU2OnvhvRDEz78rczHLGRrSAqHbc8Q3+Ac2Ok/L5xyVIRtYGYm10Fq3jM3eBMe745miT/srVQrApkfd0fwI