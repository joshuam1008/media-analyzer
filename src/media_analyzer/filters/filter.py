import abc

"""
Abstract class for filter
"""


class Filter(metaclass=abc.ABCMeta):
    """
    return true if content match with criteria, false otherwise
    """

    @abc.abstractmethod
    def filter(self, content):
        pass
