from flir_camera import check_camera_params, record_video
from pathlib import Path


if __name__ == '__main__':

    params = {
        "frame_size": (800, 600),
        "frame_rate": 40.,
        "exposure": 20_000,
        "offsets": (200, 450)
    }

    SHOW_VIDEO = True
    RECORDING_TIME = 5  # minutes
    WORKING_DIRECTORY = "D:/d_willistoni/"  # where videos will be saved
    FILENAME = "test"  # basename of the file

    # =============================================

    directory = Path(WORKING_DIRECTORY)
    if not directory.exists():
        directory.mkdir(parents=True)
    path = directory.joinpath(FILENAME)
    path = path.with_suffix(".avi")

    # check_camera_params(**params)
    record_video(path, 10,
                 display_video=SHOW_VIDEO, **params)
