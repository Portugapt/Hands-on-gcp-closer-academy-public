MERGE `{table_target}` AS T
USING (
    SELECT
        PassengerId,
        IF(Survived = 1, True, False) AS Survived,
        Pclass,
        Name,
        Sex,
        Age,
        SibSp,
        Parch,
        Ticket,
        Fare,
        Cabin,
        Embarked
    FROM
        `{table_source}`
    QUALIFY ROW_NUMBER() OVER (PARTITION BY PassengerId ORDER BY Survived DESC) = 1
) S
ON (
    S.PassengerId = T.PassengerId
)
WHEN NOT MATCHED BY TARGET THEN
INSERT (
    PassengerId,
    Survived,
    Pclass,
    Name,
    Sex,
    Age,
    SibSp,
    Parch,
    Ticket,
    Fare,
    Cabin,
    Embarked
)
VALUES (
    PassengerId,
    Survived,
    Pclass,
    Name,
    Sex,
    Age,
    SibSp,
    Parch,
    Ticket,
    Fare,
    Cabin,
    Embarked
)
