from typing import List, Union, Optional

from pandas import DataFrame, Series


class Reducer:
    def __init__(self, df: DataFrame):
        """Initialize the class.

        Args:
            df (DataFrame): An instance of DataFrame.
        """
        self.df = df

    def get(self) -> DataFrame:
        """Get the DataFrame.

        Returns:
            DataFrame: The instance of DataFrame.
        """
        return self.df

    def values(self) -> List:
        """Get column values.

        Returns:
            List: An list with values.
        """
        return self.df.values.tolist()

    def unique_values(self) -> List:
        """Get column unique values.

        Returns:
            List: An list with unique values.
        """
        return self.df.unique()

    def pick(self, column: str, as_list=True) -> Optional[Union[List, Series]]:
        """Pick values given an column name.

        Args:
            column (str): The column name.
            as_list (bool, optional): True to return a list or false to return an instance of Series. Defaults to True.

        Returns:
            None: If the column is not found in the DataFrame.
            Union[List, Series]: Returns an list if true or returns an instance of Series if false.
        """
        if column not in self.df.columns:
            return None

        if not as_list:
            return self.df[column]

        return self.df[column].values.tolist()
