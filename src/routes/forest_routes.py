import cv2
import numpy as np
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, File

from src.routes.routers import router
from src.containers.containers import AppContainer
from src.services.forest_analyzer import ForestAnalyzer


@router.get('/predict')
@inject
def predict(
    image: bytes = File(),
    service: ForestAnalyzer = Depends(Provide[AppContainer.forest_analyzer]),
):
    img = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)

    return {
        'tags': service.predict(img),
    }


@router.get('/predict_proba')
@inject
def predict_proba(
    image: bytes = File(),
    service: ForestAnalyzer = Depends(Provide[AppContainer.forest_analyzer]),
):
    img = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)

    return {
        'tags_probs': service.predict_proba(img),
    }
