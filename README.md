# TF2C-Console-downloader

This will download custom resource files (maps, models, sounds etc) that failed to download directly from a TF2C server.
In TF2C you will need to enable "developer 1" and "download_debug 1". When you fail to download a resource, go to the TF2C console and type "condump". This will dump the output of the console into your \tf2classic\ folder. You must have the following folders already setup in \tf2classic\download:
\maps
\materials
\models
\particles
\sound
The script also expects your TF2C folder is found 'C:\Program Files (x86)\Steam\steamapps\sourcemods\tf2classic'.

Once you run condump, run this python script and the script will attempt to grab .bz2 archives from the URLs provided and download them correctly to the tf2classic\download folder. It will delete the .bz2 archives on successful extraction of the contents.

TF2C does not have to be closed to run this script.
@goddog on discord if you have any questions

"Missing map"
