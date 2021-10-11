# Setup

Create an environment to run the script. I used Poetry to create my environment, and I'll include steps for doing so below. If you want to use conda, that will work too.

For these steps, I started in my `~/Code/musa/musa-509/` folder.

```bash
mkdir download_data
cd download_data
poetry init
```

Select the default options while running `poetry init`. The package we'll need in order to run the script is `requests`. To explore the data, we may also want to install `jupyterlab` and `jupyterlab-geojson`. Since I won't need those to run the script, I'll install them as development dependencies.

```bash
poetry add requests
poetry add --dev jupyterlab jupyterlab-geojson
```

Start a Jupyter Lab session by running:

```bash
poetry run jupyter lab
```

Create a file named _download_data.py_.

# Exploration

Data exploration steps are laid out in [data_exploration.ipynb](data_exploration.ipynb).

# Running the script

To run the [download_data.py](download_data.py) script, after setting up your environment, assuming you used poetry as your environment manager, run:

```bash
poetry run python download_data.py
```
