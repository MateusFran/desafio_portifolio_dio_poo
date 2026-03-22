class Student:

    school = "Escola XYZ"  # Variável de classe

    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.registration = f"{name[:3].upper()}{age}"  # Variável de instância

    def __str__(self):
        return f"Student: {self.name}, Age: {self.age}, School: {self.school}, Registration: {self.registration}"

s1 = Student("Alice", 20)
s2 = Student("Bob", 22)

print(s1)  # Student: Alice, Age: 20, School: Escola XYZ, Registration: ALI20
print(s2)  # Student: Bob, Age: 22, School: Escola XYZ, Registration: BOB22