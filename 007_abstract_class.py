from abc import ABC, abstractmethod

class RemoteControl(ABC):
    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

    def turn_off(self):
        raise NotImplementedError("Subclasses must implement this method")