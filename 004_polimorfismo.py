class Bird:
    def fly(self):
        print("The bird is flying.")
    
class Arara(Bird):
    def fly(self):
        print("The arara is flying.")

class Pinguim(Bird):
    def fly(self):
        print("The pinguim cannot fly.")

def make_it_fly(bird):
    bird.fly()