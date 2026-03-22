class Temperatura:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, valor):
        if valor < -273.15:
            raise ValueError("Temperatura abaixo do zero absoluto!")
        self._celsius = valor

    @property
    def fahrenheit(self):  # Somente leitura
        return self._celsius * 9/5 + 32

    @property
    def kelvin(self):  # Somente leitura
        return self._celsius + 273.15
    
    def str(self):
        return f"{self._celsius}°C = {self.fahrenheit}°F = {self.kelvin}K"

temp = Temperatura(25)
print(f"{temp.celsius}°C = {temp.fahrenheit}°F = {temp.kelvin}K")
# 25°C = 77.0°F = 298.15K

print(temp.str())  # 25°C = 77.0°F = 298.15K