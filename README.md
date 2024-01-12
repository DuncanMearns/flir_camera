# Installation

First, install Spinnaker and download PySpin from [FLIR](https://www.flir.com/products/spinnaker-sdk/).

Navigate to the folder containing PySpin and install using pip:
```commandline
pip install <name_of_installation>.whl
```
Install simple pyspin, opencv and pyyaml:
```commandline
pip install simple-pyspin
pip install opencv-python
pip install pyyaml
```

# Usage
Check camera params by running the script ```check_params.py``` or running from the command line:
```commandline
python -m check_params <path_to_params>.yml
```

Record a video by running the script ```run_experiment.py``` or running from the command line:
```commandline
python -m run_experiment <path_to_params>.yml <output_filename> <video_duration_minutes>
```