import warnings

import cv2
from simple_pyspin import Camera as PySpinCam
from PySpin import SpinnakerException
import time
from pathlib import Path


class Camera:

    _params = {
        "frame_rate": "AcquisitionFrameRate",
        "exposure": "ExposureTime",
        "frame_size": ("Width", "Height"),
        "offsets": ("OffsetX", "OffsetY")
    }

    def __init__(self, camera_id=0):
        self.camera_id = camera_id

    def __enter__(self):
        print("Starting camera")
        self.setup()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()
        print("Shutting down camera")

    def setup(self):
        self.camera = PySpinCam(self.camera_id)  # Acquire Camera
        self.camera.init()  # Initialize camera
        # Enable manual frame rate control
        self.camera.AcquisitionFrameRateAuto = 'Off'
        self.camera.AcquisitionFrameRateEnabled = True
        # Enable manual gain control
        self.camera.GainAuto = 'Off'
        # Enable manual exposure control
        self.camera.ExposureAuto = 'Off'
        # Start the camera
        self.camera.start()

    def read(self):
        return self.camera.get_array()

    def shutdown(self):
        if self.camera:
            self.camera.stop()  # Stop recording
            self.camera.close()  # You should explicitly clean up

    def set(self, param, val):
        """Set parameter on the camera. Valid parameters are:
        - frame_rate (float, fps)
        - exposure (int, microseconds)
        - frame_size (tuple, xy)
        - offsets (tuple, xy)
        """
        if param not in self._params:
            raise KeyError(f"Invalid camera parameter: {param}")
        attr = self._params[param]
        self.camera.stop()
        if isinstance(attr, tuple):
            try:
                vals = iter(val)
            except TypeError:
                raise ValueError(f"Value {param} must be a tuple")
            for a, val in zip(attr, vals):
                try:
                    setattr(self.camera, a, val)
                except SpinnakerException as e:
                    print(e)
                except TypeError:
                    warnings.warn(f"Incorrect type, {type(val)}, for parameter {param}")
        else:
            try:
                setattr(self.camera, attr, val)
            except SpinnakerException as e:
                print(e)
            except TypeError:
                warnings.warn(f"Incorrect type, {type(val)}, for parameter {param}")
        self.camera.start()

    def get(self, param):
        if param not in self._params:
            raise KeyError(f"Invalid camera parameter: {param}")
        attr = self._params[param]
        if isinstance(attr, tuple):
            return tuple(getattr(self.camera, a) for a in attr)
        return getattr(self.camera, attr)


def check_camera_params(camera_id=0, **camera_params):
    """Check camera with given parameters."""
    camera = Camera(camera_id)
    with camera as cam:
        for param, val in camera_params.items():
            cam.set(param, val)
        cam.read()
        frame = cam.read()
        cv2.imshow("check_params", frame)
        print("Press any key to exit")
        cv2.waitKey(0)
        cv2.destroyWindow("check_params")


class Infinity(float):

    def __lt__(self, other):
        return False

    def __gt__(self, other):
        return True


class DummyWriter:

    def write(self, *args):
        return

    def release(self):
        return


def record_video(output_path, duration, camera_id=0, display_video=False, codec="XVID", **camera_params):
    """Record a video for the given duration (seconds)."""
    camera = Camera(camera_id)
    with camera as cam:
        for param, val in camera_params.items():
            cam.set(param, val)
        frame_rate = cam.get("frame_rate")
        frame_size = cam.get("frame_size")
        # create output video
        if output_path:
            output_path = str(output_path)
            fourcc = cv2.VideoWriter_fourcc(*codec)
            writer = cv2.VideoWriter(str(output_path), fourcc, frame_rate, frame_size, False)
            print("Starting recording:", Path(output_path).name)
        else:
            writer = DummyWriter()
            display_video = True
        if duration is None:
            display_video = True
        t_end = time.time() + duration if duration is not None else Infinity()
        if display_video:
            print("Press any key to exit")
        while time.time() < t_end:
            frame = camera.read()
            writer.write(frame)
            if display_video:
                cv2.imshow(str(output_path), frame[::2, ::2])
                k = cv2.waitKey(1)
                if k > 0:
                    print("Keyboard interrupt")
                    break
        cv2.destroyAllWindows()
        writer.release()
        if output_path:
            print("Recording finished")
