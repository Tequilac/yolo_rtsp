import cv2

from src.frames.frames_manager import FramesManager


class RtspReader:
    def __init__(self, frame_rate: int, rtsp_url: str, frames_manager: FramesManager) -> None:
        self._capture = None
        self._frames = []
        self._frame_rate = frame_rate
        self._rtsp_url = rtsp_url
        self.initialize_connection()

    def initialize_connection(self):
        self._capture = cv2.VideoCapture(self._rtsp_url)
        count = 0

        while self._capture.isOpened():
            ret, frame = self._capture.read()

            if ret:
                count += self._frame_rate
                self._capture.set(cv2.CAP_PROP_POS_FRAMES, count)
            else:
                self._capture.release()
                break
