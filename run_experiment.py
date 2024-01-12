from flir_camera import record_video
from pathlib import Path
import yaml
import sys


if __name__ == '__main__':

    FILENAME = "test"
    DURATION = 5  # minutes
    PARAMS_PATH = "params.yml"

    # ============================================

    # Parse arguments from command line (if given)
    args = sys.argv[1:]
    params_path = args[0] if args else PARAMS_PATH
    filename = args[1] if args else FILENAME
    duration_minutes = args[2] if args else DURATION

    # Open params
    with open(params_path, "r") as stream:
        data = yaml.safe_load(stream)

    # Set directory and check file exists
    directory = Path(data["working_directory"])
    if not directory.exists():
        directory.mkdir(parents=True)
    path = directory.joinpath(filename).with_suffix(".avi")
    if path.exists():
        print("File already exists!")
        sys.exit(1)

    # Get params
    params = data["camera_params"]
    display_video = data["display_video"]
    duration_seconds = duration_minutes * 60

    # Record
    record_video(path, duration_seconds, display_video=display_video, **params)
