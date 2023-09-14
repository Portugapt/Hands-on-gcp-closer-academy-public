
import pandas as pd
from sklearn.base import ClassifierMixin
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def titanic_train(
    df: pd.DataFrame,
    classifier: ClassifierMixin = RandomForestClassifier(
        n_estimators=100, random_state=42),
) -> Pipeline:
    """Train a model into a pipeline

    Args:
        df (pd.Dataframe): The dataframe with the data to train the model.
        classifier (Callable, optional): The classifier to use.
            Defaults to RandomForestClassifier(n_estimators=100, random_state=42).
    """
    # Preprocess the data
    X = df.drop(columns=['Survived', 'PassengerId',
                         'Name', 'Ticket', 'Cabin'])  # OPTIONAL [1]: add 'set_type' or other columns that shouldn't be passed to the model.
    y = df['Survived']

    # Drop rows with missing target values
    missing_target_rows = y.isna()
    X = X[~missing_target_rows]
    y = y[~missing_target_rows]

    # Preprocessing for numerical columns
    numeric_features = ['Age', 'SibSp', 'Parch', 'Fare']
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    # Preprocessing for the 'Sex' column
    sex_feature = ['Sex']
    sex_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='unknown')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    # Preprocessing for the 'Embarked' column
    embarked_feature = ['Embarked']
    embarked_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    # Preprocessing for the 'Pclass' column
    pclass_feature = ['Pclass']
    pclass_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    # Combine transformers into a preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('sex', sex_transformer, sex_feature),
            ('embarked', embarked_transformer, embarked_feature),
            ('pclass', pclass_transformer, pclass_feature)])

    # Create the pipeline with preprocessing and the Random Forest classifier
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', classifier)
    ])

    # Train the model on the training data
    pipeline.fit(X, y)

    return pipeline
