intake-coops
==============================

<!-- [![Build Status](https://github.com/axiom-data-science/intake-coops/workflows/Tests/badge.svg)](https://github.com/axiom-data-science/intake-coops/actions)
[![codecov](https://codecov.io/gh/axiom-data-science/intake-coops/branch/main/graph/badge.svg)](https://codecov.io/gh/axiom-data-science/intake-coops) -->
[![License:MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
<!-- [![conda-forge](https://img.shields.io/conda/dn/conda-forge/intake-coops?label=conda-forge)](https://anaconda.org/conda-forge/intake-coops)[![Documentation Status](https://readthedocs.org/projects/intake-coops/badge/?version=latest)](https://intake-coops.readthedocs.io/en/latest/?badge=latest) -->
[![Python Package Index](https://img.shields.io/pypi/v/intake-coops.svg?style=for-the-badge)](https://pypi.org/project/intake-coops)


Intake interface to NOAA CO-OPS data

Uses the [`noaa_coops`](https://github.com/GClunies/noaa_coops) package to read in NOAA CO-OPS data.

Currently limited to currents only with limited selections. Returns an `xarray` Dataset, but there are `intake` Sources for both `DataFrame` and `xarray`.

This is intake v1 still.

--------

<p><small>Project based on the <a target="_blank" href="https://github.com/jbusecke/cookiecutter-science-project">cookiecutter science project template</a>.</small></p>


# Installation

## PyPI

    >>> pip install intake-coops


## Local installation

Clone from github (HTTPS or SSH)

    >>> git clone https://github.com/axiom-data-science/intake-coops.git

Install environment file

    >>> conda env create -f environment.yml

Activate new environment

    >>> conda activate intake-coops

Install package locally in package directory

    >>> pip install -e .


# Example Usage

If you input to `intake.open_coops_cat()` the keyword argument `process_adcp=True`, the ADCP Dataset will contain velocity on u and v components, along- and across-channel components, and along- and across-channel subtidal signal (processed with pl33 tidal filter, also included).

```
import intake

stations = ["COI0302", "COI0512"]
cat = intake.open_coops_cat(stations)

# sources in catalog
print(list(cat))

# look at a source
print(cat["COI0302"])

# read in data to a Dataset
ds = cat["COI0302"].read()
```


### Development

To also develop this package, install additional packages with:
``` bash
$ conda install --file requirements-dev.txt
```

To then check code before committing and pushing it to github, locally run
``` bash
$ pre-commit run --all-files
```
