import csv
from typing import Generator, List

from . import models


def split_lines(
    content: str,
) -> List[str]:
    """Split the content by lines.

    Args:
        content (str): The content of the file.

    Returns:
        List[str]: The lines of the file.
    """
    return content.strip().split('\n')


def titanic_transform(
    datapoints: List[str],
) -> Generator[models.TitanicData, None, None]:
    """Generator that transforms a CSV datapoint into a titanic data object.

    Args:
        datapoints (List[str]): A list of CSV datapoints.

    Yields:
        models.TitanicData: A titanic data object.
    """
    for datapoint in datapoints:
        datapoint_decoded = list(csv.reader([datapoint]))[0]

        # Zip the headers and values together into a dictionary
        datapoint_obj = models.TitanicData(
            PassengerId=datapoint_decoded[0] if datapoint_decoded[0] else '',
            Survived=datapoint_decoded[1] if datapoint_decoded[1] else '',
            Pclass=datapoint_decoded[2] if datapoint_decoded[2] else '',
            Name=datapoint_decoded[3] if datapoint_decoded[3] else '',
            Sex=datapoint_decoded[4] if datapoint_decoded[4] else '',
            Age=datapoint_decoded[5] if datapoint_decoded[5] else '',
            SibSp=datapoint_decoded[6] if datapoint_decoded[6] else '',
            Parch=datapoint_decoded[7] if datapoint_decoded[7] else '',
            Ticket=datapoint_decoded[8] if datapoint_decoded[8] else '',
            Fare=datapoint_decoded[9] if datapoint_decoded[9] else '',
            Cabin=datapoint_decoded[10] if datapoint_decoded[10] else '',
            Embarked=datapoint_decoded[11] if datapoint_decoded[11] else '',
        )

        # Yield the datapoint object
        yield datapoint_obj
