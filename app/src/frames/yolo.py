import time

import cv2
import numpy as np

from .frame import FrameInfo


class Yolo:
    def __init__(self, frames_to_analyze: list, result_callback) -> None:
        self._classes_file = "/app/res/files/yolov3.txt"
        self._net_config_file = "/app/res/files/yolov3.cfg"
        self._weights_file = "/app/res/files/yolov3.weights"
        self._net = cv2.dnn.readNet(self._weights_file, self._net_config_file)
        self._classes = None
        self._is_running = False
        self._stopped = False
        self._frames_to_analyze = frames_to_analyze
        self._result_callback = result_callback
        with open(self._classes_file, 'r') as f:
            self._classes = [line.strip() for line in f.readlines()]

    def run_analyzing(self):
        while True:
            if not self._is_running and len(self._frames_to_analyze) != 0 and not self._stopped:
                self.analyze_image(self._frames_to_analyze.pop(0))
            elif not self._stopped:
                time.sleep(0.1)
            else:
                return

    def get_output_layers(self):

        layer_names = self._net.getLayerNames()

        output_layers = [layer_names[i - 1] for i in self._net.getUnconnectedOutLayers()]

        return output_layers

    def analyze_image(self, frame_info: FrameInfo):
        self._is_running = True
        image = frame_info.frame

        width = image.shape[1]
        height = image.shape[0]
        scale = 0.00392

        blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)
        self._net.setInput(blob)
        outs = self._net.forward(self.get_output_layers())

        scores = self.get_scores(outs, width, height)
        self._result_callback(frame_info, scores)
        self._is_running = False

    def get_scores(self, outs, width, height):
        classes = []
        confidences = []
        boxes = []
        conf_threshold = 0.5

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > conf_threshold:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    classes.append(self._classes[class_id])
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

        return classes, confidences, boxes

    def is_running(self) -> bool:
        return self._is_running

    def stop(self):
        self._stopped = True
