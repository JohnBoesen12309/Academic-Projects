####### Class Patient ######## 
class Patient:
    def __init__(self, name=None, age=None, DNA=None, has_condition=[]):
        self.n = name
        self.a = age
        self.d = DNA
        self.hc = has_condition
