import cv2
import numpy as np


def normalize_cv2(img: np.ndarray, mean: np.ndarray, denominator: np.ndarray) -> np.ndarray:
    """Normalizes image with the specified mean and denominator
    Implementation was taken from Albumentations library

    Args:
        img (np.ndarray): input image
        mean (np.ndarray): vector of means by channels
        denominator (np.ndarray): vector of 1/std by channels

    Returns:
        np.ndarray: normalized image
    """
    if mean.shape and len(mean) != 4 and mean.shape != img.shape:
        mean = np.array(mean.tolist() + [0] * (4 - len(mean)), dtype=np.float64)  # noqa: WPS435, WPS221
    if not denominator.shape:
        denominator = np.array([denominator.tolist()] * 4, dtype=np.float64)  # noqa: WPS435, WPS221
    elif len(denominator) != 4 and denominator.shape != img.shape:
        denominator = np.array(denominator.tolist() + [1] * (4 - len(denominator)), dtype=np.float64)  # noqa: WPS435, WPS221, E501

    img = np.ascontiguousarray(img.astype(np.float32))
    cv2.subtract(img, mean.astype(np.float64), img)
    cv2.multiply(img, denominator.astype(np.float64), img)
    return img


def sigmoid(vector: np.ndarray) -> np.ndarray:
    """Apply sigmoid function to the input vector

    Args:
        vector (np.ndarray): vector of input values

    Returns:
        np.ndarray: vector with values between (0, 1)
    """
    return 1 / (1 + np.exp(-vector))
