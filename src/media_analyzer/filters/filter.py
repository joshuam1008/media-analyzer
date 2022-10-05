import abc


class Filter(metaclass=abc.ABCMeta):
    '''Abstract class for filter'''
    @abc.abstractmethod
    def filter(self, content):
        '''Return true if content match with criteria, false otherwise'''
        pass
