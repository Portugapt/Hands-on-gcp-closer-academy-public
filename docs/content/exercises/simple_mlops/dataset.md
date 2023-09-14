# Meet the dataset

We will use the [Titanic Dataset](https://github.com/datasciencedojo/datasets/blob/master/titanic.csv) available pretty much anywhere.

The columns and their types are the following

| Column name    | Python data type | Bigquery data type | Description                                               |
|----------------|------------------|--------------------|-----------------------------------------------------------|
| PassengerId    | int              | INT64             | Unique identifier for each passenger                      |
| Survived       | bool              | BOOLEAN             | Survival status (False = No, True = Yes)                         |
| Pclass         | int              | INT64             | Ticket class (1 = 1st, 2 = 2nd, 3 = 3rd)                  |
| Name           | str              | STRING            | Full name of the passenger                                |
| Sex            | str              | STRING            | Gender (male or female)                                   |
| Age            | float            | FLOAT64           | Age in years                                              |
| SibSp          | int              | INT64             | Number of siblings/spouses aboard the Titanic             |
| Parch          | int              | INT64             | Number of parents/children aboard the Titanic             |
| Ticket         | str              | STRING            | Ticket number                                             |
| Fare           | float            | FLOAT64           | Passenger fare                                            |
| Cabin          | str              | STRING            | Cabin number                                              |
| Embarked       | str              | STRING            | Port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton) |
| OPTIONAL: set_type | str | STRING | Set type (Train / Test / Validation) |


So, when creating the Tables, you have to create the schema accodingly. 

The dataset is available at `./dataset/titanic.csv`.
