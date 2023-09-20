import numpy as np

from src.services.forest_classifier import ForestClassifier


class ForestAnalyzer:
    def __init__(self, config: dict, classifier: ForestClassifier) -> None:
        """Inits Forest analyzer service

        Args:
            classes_list (list[str]): class names list
            thresholds_list (list[float]): list of thresholds for each tag
            classifier (ForestClassifier): classifier object for making predictions
        """
        self._class_names_list = config['class_names']
        self._thresholds = config['tags_thresholds']
        self._classifier = classifier

    def predict(self, image: np.ndarray) -> list[str]:
        """Returns tag names for the specified image

        Args:
            image (np.ndarray): input image in BGR format

        Returns:
            list[str]: list of tags
        """
        raw_prediction = self._classifier.predict(image)
        filtered_pred_arr = np.where(raw_prediction >= self._thresholds)[0]

        return [self._class_names_list[class_ind] for class_ind in filtered_pred_arr]

    def predict_proba(self, image: np.ndarray) -> dict[str, float]:
        """Predicts probabilities of each tag for this image

        Args:
            image (np.ndarray): input image in BGR format

        Returns:
            dict[str, float]: dictionary of {tag: score} items
        """
        raw_prediction = self._classifier.predict(image)

        return {self._class_names_list[class_ind]: class_prob for class_ind, class_prob in enumerate(raw_prediction)}
