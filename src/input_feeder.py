"""
InputFeeder class is used to feed input from an image, webcam, or video to your model.
"""

import cv2
from utils.log_helper import LogHelper


class InputFeeder:
    def __init__(self, input_type, input_file=None):
        """
        input_type: str, The type of input. Can be 'video' for video file, 'image' for image file,
                    or 'cam' to use webcam feed.
        input_file: str, The file that contains the input image or video file. Leave empty for cam input_type.
        """
        self.loggers = LogHelper()

        self.input_type = input_type
        if input_type == 'video' or input_type == 'image':
            self.input_file = input_file

        self.cap = None

    def load_data(self):
        try:
            if self.input_type == 'video':
                self.cap = cv2.VideoCapture(self.input_file)
            elif self.input_type == 'cam':
                self.cap = cv2.VideoCapture(0)
            else:
                self.cap = cv2.imread(self.input_file)
        except Exception as e:
            self.loggers.main.critical("InputFeeder: error while loading input ({}). Please review your input. "
                                       "Exiting now...".format(self.input_type))

    def next_batch(self):
        """
        Returns the next image from either a video file or webcam.
        If input_type is 'image', then it returns the same image.
        """
        while True:
            for _ in range(5):  # for range(x), x "is like a batch size"
                _, frame = self.cap.read()
            yield frame

    def close(self):
        """
        Closes the VideoCapture.
        """
        if not self.input_type == 'image':
            self.cap.release()
