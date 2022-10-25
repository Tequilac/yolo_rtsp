import cv2
import numpy as np


class Yolo:
    def __init__(self) -> None:
        self._classes_file = "../res/files/yolov3.txt"
        self._net_config_file = "../res/files/yolov3.cfg"
        self._weights_file = "../res/files/yolov3.weights"
        self._net = cv2.dnn.readNet(self._weights_file, self._net_config_file)
        self._classes = None
        self._is_running = False
        with open(self._classes_file, 'r') as f:
            self._classes = [line.strip() for line in f.readlines()]

    def get_output_layers(self):

        layer_names = self._net.getLayerNames()

        output_layers = [layer_names[i - 1] for i in self._net.getUnconnectedOutLayers()]

        return output_layers

    def analyze_image(self, image):
        self._is_running = True
        image = cv2.imread(image)

        Width = image.shape[1]
        Height = image.shape[0]
        scale = 0.00392

        blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)
        self._net.setInput(blob)
        outs = self._net.forward(self.get_output_layers())

        scores = self.get_scores(outs, Width, Height)
        self._is_running = False
        return scores

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
