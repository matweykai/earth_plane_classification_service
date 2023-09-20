from pydantic import BaseModel


class PredictAnswer(BaseModel):
    tags: list[str]


class PredictProbaAnswer(BaseModel):
    tags_probs: dict[str, float]
