from __future__ import annotations

from typing import Optional

from mongoengine.context_managers import switch_db
from pandas import DataFrame
from singleton_decorator import singleton

from database import db_connections
from database.models.tags import TagsModel
from modules.enums import TagsDataFrame
from modules.reducer import Reducer


@singleton
class Tags:
    def __init__(self):
        self.df = DataFrame()

    @property
    def get(self) -> DataFrame:
        """Get the DataFrame of Tags.

        Returns:
            DataFrame: An instance of DataFrame.
        """
        if self.df.empty:
            self.update()

        return self.df

    def copy(self) -> DataFrame:
        """Copy a DataFrame.

        Returns:
            DataFrame: An instance of DataFrame.
        """
        return self.df.copy()

    def update(self) -> Tags:
        """This method reads in the database each tag  properties and updates the dataframe object.

        Returns:
            Tags: Instance of Tags.
        """
        rows = []

        #For each database connected
        for db_alias in db_connections.values():
            #Starting tag collection manipulation through tags_model
            with switch_db(TagsModel, db_alias) as tags_model:
                for document in tags_model.objects:
                    for tag in document.tags:
                        rows.append({
                            TagsDataFrame.ID_COLUMN: tag.tag_id,
                            TagsDataFrame.NAME_COLUMN: tag.tag_name,
                            TagsDataFrame.SERVER_COLUMN: document.server,
                            TagsDataFrame.DB_ALIAS_COLUMN: db_alias,
                        })

        self.df = DataFrame(rows)

        return self

    def where(self, column: str, value: str) -> Optional[Reducer]:
        """Query the columns of a DataFrame with a boolean expression.
            It returns None when there is no tag with value in column, 
            otherwise it returns all tags that have value in column.

        Args:
            column (str): The column to be queried.
            value (str): The value to be queried.

        Returns:
            None: If the column is not found in the DataFrame.
            Reducer: An instance of Reducer.
        """
        if column not in self.get.columns:
            return None

        return Reducer(self.get.query(f'{column} == "{value}"'))

    def empty(self) -> bool:
        """Check if DataFrame is empty.

        Returns:
              Boolean: Return true if DataFrame is empty otherwise false.
        """
        return self.get.empty
