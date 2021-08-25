# impeek

Script to quickly 'peek' at images on disk.

## Installation 

Installation is easy! Just use pip: 

```
pip install impeek
```

impeek has been tested with Ubuntu 18.04 and python 3.6. 

## Usage

To peek a directory, run impeek as a module and pass a regular expression. Enclose the regular expression in double quotes to prevent the os from expanding it.

```
python -m impeek "*.png"
```

To peek recursively, use double quotes.

```
python -m impeek "**/*.png"
```

impeek will only display image files so it can be passed very general regular expressions.

```
python -m impeek "**/*"
```

impeek can automatically rescale images that are difficult to see, like thermal or depth images.

```
python -m impeek "*.png" --rescale 
```

For a full list of arguments pass the help flag.

```
python -m impeek -h
```

```
usage: __main__.py [-h] [--vmin VMIN] [--vmax VMAX] [--cmap CMAP] [--rescale]
                   [--scale SCALE] [--use_mpl] [--debug] [--quiet]
                   input

Script to quickly 'peek' at images on disk. Call with a regular expression to traverse multiple directories or traverse directories recursively. Call with '--rescale' to automatically rescale the pixel values such that they fall between 0 and 255. Call with a '--cmap' to apply a colormap to single-channel images. Call with '--use_mpl' to use the matplotlib backend which will display raw color values with a colorbar. Must be called as a module.

example: python -m impeek "../**/*.png" --cmap fire
  Display all png images in any directory rooted above the current directory, using fire colormap.

positional arguments:
  input          A regular expression used to find files. If you use the '*' operator you will need to enclose this argument in double quotes.

optional arguments:
  -h, --help     show this help message and exit
  --vmin VMIN    Minimum pixel intensity value to display. All pixel values lower than this will be clipped to 0.
  --vmax VMAX    Maximum pixel intensity value to display. All pixel values higher than this will be clipped to 255.
  --cmap CMAP    Colormap to use. Single channel images will be converted to RGB using this colormap. Has no effect on multi-channel (color) images.
  --rescale      If passed will rescale the pixel values such that they fall between 0 and 255. By default uses the min and max values of the image to scale the pixel values. If vmin or vmax are passed these are used instead.
  --scale SCALE  Apply a dimensional scale to the image. Default is 1.0.
  --use_mpl      If true will use the matplotlib engine to display the image. See the documentation for matplotlib.imshow for more information. This will also display a colorbar with the raw pixel values before rescaling.
  --debug        If set, debugging messages will be printed.
  --quiet        If set, only warnings will be printed.
```
