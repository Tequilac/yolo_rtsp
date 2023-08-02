import threading
from datetime import datetime

from paho.mqtt import client as mqtt_client

from ..config.types import FrameStrategy, MqttInfo
from .frame import FrameInfo
from .yolo import Yolo

from ..logger import logger


def generate_detected_objects_info(result):
    info = []
    classes, confidences, boxes = result
    for class_name, confidence, box in zip(classes, confidences, boxes):
        info.append({
            'class': class_name,
            'confidence': confidence,
            'box': {
                'upperLeft': (box[0], box[1]),
                'lowerRight': (box[0] + box[2], box[1] + box[3])
            }
        })
    return info


class FramesManager:
    def __init__(self, frame_strategy: FrameStrategy, mqtt_info: MqttInfo):
        self._stored_frames = []
        self._yolo = Yolo(self._stored_frames, self.result_callback)
        self._frame_strategy = frame_strategy
        self._mqtt_info = mqtt_info
        self._mqtt_client = self.connect_mqtt() if mqtt_info else None
        self._yolo_thread = threading.Thread(target=self._yolo.run_analyzing, args=())
        self._yolo_thread.start()

    def stop_yolo(self):
        if self._yolo_thread:
            self._yolo.stop()
            self._yolo_thread.join()

    def handle_frame(self, frame):
        time = datetime.now()
        frame_info = FrameInfo(frame=frame, timestamp=time)
        if self._frame_strategy == FrameStrategy.DROP:
            if not self._yolo.is_running():
                self._stored_frames.append(frame_info)
            else:
                logger.info(f"Dropping frame")
        elif self._frame_strategy == FrameStrategy.STORE:
            self._stored_frames.append(frame_info)

    def connect_mqtt(self):
        def on_connect(client_instance, userdata, flags, rc):
            if rc == 0:
                logger.info("Connected to MQTT broker")
            else:
                logger.warning("Failed to connect to MQTT broker, return code %d\n", rc)
        # Set Connecting Client ID
        try:
            client = mqtt_client.Client(self._mqtt_info.client_id)
            client.username_pw_set(self._mqtt_info.username, self._mqtt_info.password)
            client.on_connect = on_connect
            client.connect(self._mqtt_info.broker, self._mqtt_info.port)
            return client
        except Exception:
            return None

    def result_callback(self, frame_info: FrameInfo, result):
        msg = {
            'timestamp': frame_info.timestamp,
            'detected_objects': generate_detected_objects_info(result)
        }
        if self._mqtt_client:
            result = self._mqtt_client.publish(self._mqtt_info.topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                logger.info(f"Send message to MQTT topic")
            else:
                logger.warning(f"Failed to send message to MQTT topic")
                logger.info(msg)
        else:
            logger.info(msg)

    def stop(self):
        self.stop_yolo()
        if self._mqtt_client:
            self._mqtt_client.disconnect()
