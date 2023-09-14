import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from c_train_model.app.funcs.train_models import titanic_train


def test_titanic_train_rfc() -> None:
    """Test the titanic_train function with Random Forest Classifier.

    This function creates a test dataframe and uses it to train a machine learning model
    with the titanic_train function. Then, it creates a test dataset and uses the trained
    model to make predictions. Finally, it checks that the predictions have the expected
    length.

    Raises:
        AssertionError: If the length of the predictions is not 2.
    """
    # Create a test dataframe
    df = pd.DataFrame({
        'Survived': [True, False, True, False],
        'PassengerId': [1, 2, 3, 4],
        'Name': ['John Doe', 'Jane Doe', 'Bob Smith', 'Alice Smith'],
        'Sex': ['male', 'female', 'male', 'female'],
        'Pclass': [1, 2, 3, 1],
        'Age': [30, 25, 40, 35],
        'SibSp': [1, 0, 1, 0],
        'Parch': [0, 1, 0, 1],
        'Ticket': ['1234', '5678', '9101', '1121'],
        'Fare': [10.0, 20.0, 30.0, 40.0],
        'Cabin': ['A1', 'B2', 'C3', 'D4'],
        'Embarked': ['S', 'C', 'S', 'C']
    })

    # Train the model
    pipeline = titanic_train(df, classifier=RandomForestClassifier())

    # Test the model
    X_test = pd.DataFrame({
        'Sex': ['male', 'female'],
        'Age': [20, 50],
        'SibSp': [0, 1],
        'Parch': [1, 0],
        'Fare': [15.0, 25.0],
        'Embarked': ['S', 'C'],
        'Pclass': [1, 2]
    })
    y_pred = pipeline.predict(X_test)
    assert len(y_pred) == 2
    for y in y_pred:
        assert y in [True, False]


def test_titanic_train_svm() -> None:
    """Test the titanic_train function with Support Vector Machine.

    This function creates a test dataframe and uses it to train a machine learning model
    with the titanic_train function. Then, it creates a test dataset and uses the trained
    model to make predictions. Finally, it checks that the predictions have the expected
    length.

    Raises:
        AssertionError: If the length of the predictions is not 2.
    """
    # Create a test dataframe
    df = pd.DataFrame({
        'Survived': [True, False, True, False],
        'PassengerId': [1, 2, 3, 4],
        'Name': ['John Doe', 'Jane Doe', 'Bob Smith', 'Alice Smith'],
        'Sex': ['male', 'female', 'male', 'female'],
        'Pclass': [1, 2, 3, 1],
        'Age': [30, 25, 40, 35],
        'SibSp': [1, 0, 1, 0],
        'Parch': [0, 1, 0, 1],
        'Ticket': ['1234', '5678', '9101', '1121'],
        'Fare': [10.0, 20.0, 30.0, 40.0],
        'Cabin': ['A1', 'B2', 'C3', 'D4'],
        'Embarked': ['S', 'C', 'S', 'C']
    })

    # Train the model
    pipeline = titanic_train(df, classifier=SVC())

    # Test the model
    X_test = pd.DataFrame({
        'Sex': ['male', 'female'],
        'Age': [20, 50],
        'SibSp': [0, 1],
        'Parch': [1, 0],
        'Fare': [15.0, 25.0],
        'Embarked': ['S', 'C'],
        'Pclass': [1, 2]
    })
    y_pred = pipeline.predict(X_test)
    assert len(y_pred) == 2
    for y in y_pred:
        assert y in [True, False]
