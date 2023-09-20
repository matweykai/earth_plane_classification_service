from dependency_injector import containers, providers

from src.services.forest_classifier import ForestClassifier
from src.services.forest_analyzer import ForestAnalyzer


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    forest_classifier = providers.Singleton(
        ForestClassifier,
        config=config.services.classifier,
    )

    forest_analyzer = providers.Singleton(
        ForestAnalyzer,
        config=config.services.forest_analyzer,
        classifier=forest_classifier,
    )
