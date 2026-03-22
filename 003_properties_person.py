import datetime

class Person:
    def __init__(self, name=None, born_year=None):
        self._name = name
        self._born_year = born_year

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def born_year(self):
        return self._born_year

    @born_year.setter
    def born_year(self, value):
        if value < 0 or value > datetime.date.today().year:
            raise ValueError("Born year cannot be negative or in the future!")
        self._born_year = value

    @property
    def age(self):
        return datetime.date.today().year - self._born_year

p1 = Person("Alice", 2029)
print(p1.name)  # Output: Alice

p1.born_year = 2002

print(p1.born_year)   # Output: 2002
print(p1.age)