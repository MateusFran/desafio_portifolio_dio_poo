class Foo:
    def __init__(self, x=None):
        self._x = x

        @property
        def x(self):
            return self._x or 0
        
        @x.setter
        def x(self, value):
            _x = self._x or 0
            _value = value or 0
            self._x = _x + value

        @x.deleter
        def x(self):
            self._x = -1

foo = Foo()
print(foo.x)  # Output: 0
foo.x = 5
print(foo.x)  # Output: 5