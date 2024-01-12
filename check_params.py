from flir_camera import record_video
import yaml
import sys


if __name__ == "__main__":

    PARAMS_PATH = "params.yml"

    # ============================================

    # Parse arguments from command line (if given)
    args = sys.argv[1:]
    params_path = args[0] if args else PARAMS_PATH

    # Import params
    with open(params_path, "r") as stream:
        data = yaml.safe_load(stream)
    camera_params = data["camera_params"]

    # Check frame from camera with given params
    record_video(None, None, **camera_params)
