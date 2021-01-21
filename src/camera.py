import time
import io
import threading
import picamera
from threading import Condition


class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera
    buffer = io.BytesIO()
    thread_lock = Condition()
    camera = None

    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()
            with Camera.thread_lock:
                Camera.thread_lock.wait()

    def get_image(self):
        Camera.last_access = time.time()
        self.initialize()
        buffer = io.BytesIO()
        Camera.camera.capture(buffer, format='jpeg', use_video_port=True)
        buffer.seek(0)
        return buffer

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        with Camera.thread_lock:
            Camera.thread_lock.wait()
        return Camera.frame

    @classmethod
    def write(cls, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            cls.buffer.truncate()
            with cls.thread_lock:
                cls.frame = cls.buffer.getvalue()
                cls.thread_lock.notify_all()
            cls.buffer.seek(0)
        return cls.buffer.write(buf)

    @classmethod
    def _thread(cls):
        print('Starting Camera')
        cls.camera = camera = picamera.PiCamera(resolution='640x480', framerate=30)

        # camera setup
        camera.hflip = False
        camera.vflip = False

        camera.start_recording(cls, format='mjpeg')

        while True:
            if time.time() - Camera.last_access > 5:
                # if there hasn't been any clients asking for frames in
                # the last X seconds stop the thread
                break
            time.sleep(1)

        cls.camera.stop_recording()
        cls.camera.close()
        cls.thread = None
        print('Stopping Camera')