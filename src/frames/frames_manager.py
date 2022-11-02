from src.config.types import FrameStrategy
from src.yolo import Yolo


class FramesManager:
    def __init__(self, yolo: Yolo, frame_strategy: FrameStrategy):
        self._stored_frames = []
        self._yolo = yolo
        self._frame_strategy = frame_strategy

    def handle_frame(self, frame):
        if self._frame_strategy == FrameStrategy.DROP:
            if not self._yolo.is_running():
                self._yolo.analyze_image(frame)
        elif self._frame_strategy == FrameStrategy.STORE:
            if self._yolo.is_running():
                self._stored_frames.append(frame)
