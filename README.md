# Labtools

Python toolkit facilitating basic experimantal data processing.

### Setup and Run
---------------
Download repository and start IPython from it's root folder. You can store data and arbitrary files directly in the repository freely, as everything is excluded from the Git by .gitignore. Then you can import `labtools` module, with preffered way via `from labtools import *`.

**Note that Labtools won't run outside from IPython shell (but probably can from Jupyter).** 

**Linux user willing to use _copy_to_clipboard_ feature should install `xclip` package, if not or _using Windows_, one _has_ to delete body of `copy_to_clipboard()` function in `utils.py` module, or the library will fail while using most of the functionality**

The developer is sorry for how inconvenient and arhaic this is and also for the lack of documentation, theese problems are due to the library being originally intended solely for personal use

### Features
-------------

This part describes main functions and applications of labtools package.

### Val

Labtools provides Val (shorthand for value) class for storing numbers with associated experimental error estimate. Several operation overloads are provided to enable arithmetic, as well as string representations for convinient view as a cell output; also Latex string is automatically copied to the clipboard when Val is a cell output (via `__repr__()` method).

Note that numpy arrays automatically provide vectorization even for ndarrays with _object_ dtype.

### Formatting

Labtools can provide string representation of numbers and automatically choose normal or scientific notation. This feature is deeply integrated with Vals, as their number of significant digits is deduced automatically from margins of error, so every time they are printed or converted to a Latex string, it is done with accordance with common physical practices

### Data parsing

Labtools uses it's own format similar to CSV. It also assumes that data file is named `data` and would automatically try to read from it when filename is not provided.

### Latex tables

Arrays of numbers can be converted to tables (booktab tables specifically) and copied to clipboard. This feature is _not maintained_ currently, so expect anything. 

### Plotting

Labtools provides Plot class, which is a higher-level matplotlib.pyplot.error_bar() builder. It can accept data as an arbitrary array (including numpy), valarray and even can directly read from file via Plot.load(). 

One of advantages of a Plot is the ability to pass any meta setting (font sizes, color, labels, e.t.c.) to most of the functions as an optional named argument and it will be stored in the class, giving great flexibility in writing code to customize your plots. 

The other one is atomatic line fitting. It can be done by passing `xrange` to the constructor specifying the range to plot approximation, or by manual function call to `trend()`. Coefficient of a resulting fitting are stored in the `k` member as a Val object.

### Script execution

The preferred way of using labtools is by importing it in the IPython shell running from root repo directory, and putting in that directory (probably creating another folder in it and `cd`-ing into it from the IPython) `data` file. Capabilities of IPython such as cells, magics, In and Out dictionaries, various shortcuts and hotkeys play very well with the typicall workflow of data processing for the report preparation. If willing to store some code for even easier reuse, one can found usefull to store it in `cache.py` file to copy partially from, or to execute with the pseudo command `run`. This prompt (just plain `>>> run`, without any brackets or '%' signs, needs labtools imported) executes `cache.py` and puts global variables from that file (which are considered local relative to the main execution flow) into the working global namescope, making them easily accessible. When name (or relative path) specification is needed, use `run()` function instead

