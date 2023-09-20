import cv2
import numpy as np
import onnxruntime as ort

from src.services.classifier_utils import normalize_cv2, sigmoid


class ForestClassifier:
    def __init__(self, config: dict) -> None:
        """Inits ForestClassifier class with ONNX model

        Args:
            weights_path (str): path to onnx model
            img_size (tuple[int, int]): image size for the model
        """
        weights_path = config['weights']
        img_size = config['img_size']

        self.session = ort.InferenceSession(
            path_or_bytes=weights_path,
            providers=['CPUExecutionProvider'],
        )
        self._img_size = img_size

    def predict(self, image: np.ndarray) -> np.ndarray:
        """Predicts tags array for this image

        Args:
            image (np.ndarray): input image

        Returns:
            np.ndarray: array of probabilities for tags
        """
        preprocessed_image = self._preprocess_image(image)

        prediction = self.session.run(None, {'input': preprocessed_image})

        return sigmoid(prediction)

    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Prepare image for model inference. It includes convertion from BGR to RGB, normalization and resizing

        Args:
            image (np.ndarray): input image

        Returns:
            np.ndarray: preprocessed image
        """
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, self._img_size)

        img_max_value = 255.0

        # Normalize image
        mean = np.array((0.485, 0.456, 0.406), dtype=np.float32)
        mean *= img_max_value

        std = np.array((0.229, 0.224, 0.225), dtype=np.float32)
        std *= img_max_value

        denominator = np.reciprocal(std, dtype=np.float32)

        image = normalize_cv2(image, mean, denominator)

        # Convert HWC to CWH
        image = image.transpose(2, 0, 1)
        return image[np.newaxis, :, :, :].astype(np.float32)
