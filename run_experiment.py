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

    # Get params
    camera_params = data["camera_params"]
    video_params = data["video_params"]
    display_video = video_params["display_video"]
    codec = video_params["codec"]
    extension = video_params["file_extension"]

    # Set directory and check file exists
    directory = Path(data["working_directory"])
    if not directory.exists():
        directory.mkdir(parents=True)
    path = directory.joinpath(filename).with_suffix("." + extension)
    if path.exists():
        print("File already exists!")
        sys.exit(1)

    duration_seconds = int(duration_minutes * 60) if duration_minutes else None

    # Record
    record_video(path, duration_seconds, display_video=display_video, **camera_params)
