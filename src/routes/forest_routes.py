import cv2
import numpy as np
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, File

from src.schemas.forest_route import PredictAnswer, PredictProbaAnswer
from src.routes.routers import router
from src.containers.containers import AppContainer
from src.services.forest_analyzer import ForestAnalyzer


@router.post('/predict')
@inject
def predict(
    image: bytes = File(),
    service: ForestAnalyzer = Depends(Provide[AppContainer.forest_analyzer]),
) -> PredictAnswer:
    img = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)

    return PredictAnswer(tags=service.predict(img))


@router.post('/predict_proba')
@inject
def predict_proba(
    image: bytes = File(),
    service: ForestAnalyzer = Depends(Provide[AppContainer.forest_analyzer]),
) -> PredictProbaAnswer:
    img = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)

    return PredictProbaAnswer(tags_probs=service.predict_proba(img))
