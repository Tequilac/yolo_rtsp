import threading

import cv2

from src.frames.frames_manager import FramesManager


class RtspReader:
    def __init__(self, frame_rate: int, rtsp_url: str, frames_manager: FramesManager) -> None:
        self._capture = None
        self._frames = []
        self._frame_rate = frame_rate
        self._rtsp_url = rtsp_url
        self._frames_manager = frames_manager
        self._capture_thread = None
        self._running = True
        self.initialize_capture()

    def initialize_capture(self):
        self._capture = cv2.VideoCapture(self._rtsp_url)
        self._capture_thread = threading.Thread(target=self.run_capture, args=(self,))
        self._capture_thread.run()

    def stop_capture(self):
        if self._capture_thread:
            self._running = False
            self._capture_thread.join()

    def run_capture(self):
        count = 0
        while self._capture.isOpened() and self._running:
            ret, frame = self._capture.read()
            self._frames_manager.handle_frame(frame)

            if ret:
                count += self._frame_rate
                self._capture.set(cv2.CAP_PROP_POS_FRAMES, count)
            else:
                self._capture.release()
                break
