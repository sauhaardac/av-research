import json
import stringcase
from abc import abstractmethod


class Brick:
    def __init__(self, json_dict: dict=None, datastring: str='', beam =None):
        """
        A data structure that encapsulates a trainable moment

        :param json_dict: <dict> data that brick holds
        :param datastring: <str> string serializing the json_dict
        :param beam: <Beam> beam that holds this brick
        """
        super().__init__()
        json_dict = json_dict or {}
        self.frame = 0
        self.truth, self.metadata, self.raw_metadata = {}, {}, {}
        if json_dict:
            self._populate_datad(json_dict)
        elif datastring:
            self._populate_datas(datastring)
        self.beam = beam

    def _populate_datad(self, json_dict: dict):
        """
        Populates this Brick with data given from a string in dict format.

        :param json_dict: <dict> dict serializing the brick.
        :return: self
        """
        self_dict = vars(self)
        for key, value in json_dict.items():
            self_dict[stringcase.snakecase(key)] = value
        return self

    def _populate_datas(self, datastring: str=''):
        """
        Populates this Brick with data given from a string in JSON format.

        :param datastring: <str> string serializing the brick.
        :return: self
        """
        return self._populate_datad(json.loads(datastring))

    def serialized(self) -> dict:
        """Get the serialized representation as a dictionary."""
        dict_repr = {}
        for key, val in vars(self).items():
            dict_repr[stringcase.camelcase(key)] = val
        del dict_repr['beam']
        return dict_repr

    def serializes(self) -> str:
        """Serializes the brick as a JSON string"""
        return json.dumps(self.serialized())

    @staticmethod
    def deserialized(json_dict: dict):
        """
        Deserializes the brick from a dict.

        :param json_dict: <dict> data that brick holds
        """
        return Brick(json_dict=json_dict)

    @staticmethod
    def deserializes(datastring: str=''):
        """
        Deserializes the brick from a string.

        :param datastring: <str> string serializing the json_dict
        """
        return Brick.deserialized(json.loads(datastring))

    def is_valid(self) -> bool:
        return self.valid

    @property
    @abstractmethod
    def valid(self) -> bool:
        pass

    @abstractmethod
    def get_input(self):
        pass

    @abstractmethod
    def get_metadata(self):
        pass

    @abstractmethod
    def get_truth(self):
        pass
