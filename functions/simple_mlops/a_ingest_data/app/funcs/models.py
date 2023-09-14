"""Models for the ingest_data function. Simplifies type hinting."""
from dataclasses import dataclass
from typing import Any, Dict, NamedTuple

from google.cloud import bigquery, pubsub, storage


class GCPClients(NamedTuple):
    """A named tuple that contains GCP client objects for Storage, BigQuery, and Pub/Sub.

    Attributes:
        storage_client (google.cloud.storage.Client): A client object for Google Cloud Storage.
        bigquery_client (google.cloud.bigquery.Client): A client object for Google BigQuery.
        publisher (google.cloud.pubsub_v1.PublisherClient): A client object for Google Cloud Pub/Sub.
    """
    storage_client: storage.Client
    bigquery_client: bigquery.Client
    publisher: pubsub.PublisherClient


class EnvVars(NamedTuple):
    """A named tuple representing environment variables required for data ingestion.

    Attributes:
        gcp_project_id (str): The ID of the Google Cloud Platform project.
        bq_table_fqn (str): The fully-qualified name of the BigQuery table.
        topic_ingestion_complete (str): The name of the Pub/Sub topic for ingestion completion notifications.
    """
    gcp_project_id: str
    bq_table_fqn: str
    topic_ingestion_complete: str


@dataclass(kw_only=True, frozen=True)
class TitanicData():
    """A class representing the data for the titanic dataset.

    Attributes:
        PassengerId (str | None): The ID of the passenger.
        Survived (str | None): Whether the passenger survived or not.
        Pclass (str | None): The class of the passenger's ticket.
        Name (str | None): The name of the passenger.
        Sex (str | None): The gender of the passenger.
        Age (str | None): The age of the passenger.
        SibSp (str | None): The number of siblings/spouses aboard the Titanic.
        Parch (str | None): The number of parents/children aboard the Titanic.
        Ticket (str | None): The ticket number of the passenger.
        Fare (str | None): The fare paid by the passenger.
        Cabin (str | None): The cabin number of the passenger.
        Embarked (str | None): The port of embarkation of the passenger.
    """
    PassengerId: str | None
    Survived: str | None
    Pclass: str | None
    Name: str | None
    Sex: str | None
    Age: str | None
    SibSp: str | None
    Parch: str | None
    Ticket: str | None
    Fare: str | None
    Cabin: str | None
    Embarked: str | None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TitanicData':
        """Creates a new instance of the TitanicData class from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing the data for a single passenger.

        Returns:
            TitanicData: A new instance of the TitanicData class.
        """
        # Convert the Survived column to a boolean
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        """Converts the TitanicData instance to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary containing the data for a single passenger.
        """
        return {
            'PassengerId': self.PassengerId,
            'Survived': self.Survived,
            'Pclass': self.Pclass,
            'Name': self.Name,
            'Sex': self.Sex,
            'Age': self.Age,
            'SibSp': self.SibSp,
            'Parch': self.Parch,
            'Ticket': self.Ticket,
            'Fare': self.Fare,
            'Cabin': self.Cabin,
            'Embarked': self.Embarked
        }
