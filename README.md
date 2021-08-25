# impeek

A command line function to visualize images in large directories using a regular expression.

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
