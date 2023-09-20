import pytest
import math
import numpy as np

from src.services.forest_analyzer import ForestAnalyzer, ForestClassifier


class FakeClassifier:
    def __init__(self, class_count: int):
        self._ret_value = np.array([float('0.5' + str(item)) for item in range(class_count)])
    
    def predict(self, image: np.ndarray) -> np.ndarray:
        return self._ret_value
    

@pytest.mark.parametrize(
    'class_list,thresholds_val,expected_tags',
    [
        (['cat', 'dog', 'orange'], [0.5, 0.5, 0.5], ['cat', 'dog', 'orange']),
        (['cat', 'dog', 'orange'], [0.5, 0.6, 0.5], ['cat', 'orange']),
        (['cat', 'dog', 'orange'], [0.6, 0.5, 0.5], ['dog', 'orange']),
        (['cat', 'dog', 'orange'], [0.5, 0.5, 0.6], ['cat', 'dog']),
        (['cat', 'dog', 'orange'], [0.5, 0.6, 0.6], ['cat']),
        (['cat', 'dog', 'orange'], [0.6, 0.6, 0.6], []),
    ]
)
def test_predict(class_list: list[str], thresholds_val: list[float], expected_tags: list[str]):
    analyzer = ForestAnalyzer(
        config={'class_names': class_list, 'tags_thresholds': thresholds_val},
        classifier=FakeClassifier(len(class_list))
    )

    assert analyzer.predict(np.ones((10, 10, 3))) == expected_tags


def test_predict_proba():
    class_names_list = ['cat', 'dog', 'orange']
    threshold_list = [0.5 for _ in range(len(class_names_list))]

    analyzer = ForestAnalyzer(
        config={'class_names': class_names_list, 'tags_thresholds': threshold_list},
        classifier=FakeClassifier(len(class_names_list))
    )

    expected_dict = {
        'cat': 0.5,
        'dog': 0.51,
        'orange': 0.52,
    }

    predicted_probs = analyzer.predict_proba(np.ones((10, 10, 3)))

    assert all([abs(expected_dict[tag_name] - predicted_probs[tag_name]) < 1e-5 for tag_name in predicted_probs])


@pytest.mark.parametrize(
    'class_list,thresholds_val',
    [
        (['cat', 'dog'], [0.5, 0.5, 0.5]),
        (['cat', 'dog', 'orange'], [0.5, 0.5]),
        ([], [0.6, 0.5, 0.5]),
        (['cat', 'dog', 'orange'], []),
    ]
)
def test_wrong_vals(class_list: list[str], thresholds_val: list[float]):

    with pytest.raises(ValueError):
        analyzer = ForestAnalyzer(
            config={'class_names': class_list, 'tags_thresholds': thresholds_val},
            classifier=FakeClassifier(len(class_list))
        )
