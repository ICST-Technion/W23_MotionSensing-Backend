from imus_handler import ImusHandler
from abc import ABC, abstractmethod
from typing import List, Dict


class Alg(ABC):
    def __init__(self, properties: List[dict], settings: dict, plot_options: Dict[str, List[str]], imus: ImusHandler,
                 name: str):
        """
        :param properties: a list of dicts that describe to the flutter frontend how to display
         the algorithm parameters for the user.
        it has the following format: [
                {"type": "CheckList", "param_name": name_of_param, "default_value": value,
                 "values": ["yes", "no"]},
                {"type": "TextBox", "param_name": name_of_param, "default_value": value}
            ]
        :param settings: a dict of the settings the algorithm will use. it has the following format:
            {
                param_name: value
            }
            where the name of the parameter and the value type must be identical to the
            corresponding parameter in properties.
        :param plot_options: a dict whose keys are the names of each graph
        and the corresponding value is a list of the series name that will be displayed on that graph.
        it has the following format:
        {graph_name: [series1_name, series2_name, series3_name...]}
        :param imus: an ImusHandler object to be used by the algorithm for IMU communication.
        :param name: name of the algorithm.
        """
        self.name = name
        self.imus = imus
        self.plot_options = plot_options
        self.settings = settings
        self.properties = properties

    @abstractmethod
    def set_settings(self, settings):
        pass

    @abstractmethod
    def run(self):
        pass
