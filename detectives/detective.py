from abc import ABC, abstractmethod


# No Money no Job -
class NoPaycheck(Exception):
    pass


# Detective has to implement methods for every input-format
class Detective(ABC):

    def __init__(self, content):
        self.input = content
        super().__init__()

    @abstractmethod
    def audio(self, sr):
        raise NoPaycheck

    @abstractmethod
    def midi(self):
        raise NoPaycheck

    @abstractmethod
    def text(self):
        raise NoPaycheck
