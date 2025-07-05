class Person:
    def __init__(self, fam='', name='', otchestvo='', year='', city='', sb_inf='', sb_math=''):
        self.fam = fam
        self.name = name
        self.otchestvo = otchestvo
        self.year = year
        self.city = city
        self.sb_inf = sb_inf
        self.sb_math = sb_math

    def getPerson_forTable(self):
        return [
            self.fam,
            self.name,
            self.otchestvo,
            self.year,
            self.city,
            self.sb_inf,
            self.sb_math
        ]

    def equval_Person(self, B):
        return (
            self.fam == B.fam and
            self.name == B.name and
            self.otchestvo == B.otchestvo and
            self.year == B.year and
            self.city == B.city and
            self.sb_inf == B.sb_inf and
            self.sb_math == B.sb_math
        )

class Grup:
    def __init__(self):
        self.A = {}
        self.count = 0

    def __str__(self):
        s = ''
        for x in range(len(self.A)):
            if x in self.A:
                s += f'Person {x+1}:\n'
                s += str(self.A[x])
                s += '\n'
        return s

    def appendPerson(self, List):
        new_Person = Person(*List)
        self.A[self.count] = new_Person
        self.count += 1

    def editPerson(self, x, List):
        P = Person(*List)
        self.A[x] = P

    def Str_Person(self, line):
        if line[-1] == '\n':
            line = line[:-1]
        parts = line.strip().split("&")
        return Person(*parts)

    def read_data_from_file(self, filename):
        self.A = {}
        self.count = 0
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    self.A[self.count] = self.Str_Person(line)
                    self.count += 1
        except FileNotFoundError:
            pass

    def write_data_to_file(self, filename):
        with open(filename, "w", encoding="utf-8") as file:
            for x in range(self.count):
                p = self.A[x]
                line = "&".join(p.getPerson_forTable())
                file.write(line + "\n")

    def find_keyPerson(self, List):
        P = Person(*List)
        for x in self.A:
            if self.A[x].equval_Person(P):
                return x
        return -1

    def delPerson(self, List):
        P = Person(*List)
        for x in self.A:
            if self.A[x].equval_Person(P):
                del self.A[x]
                self.count -= 1
                break

       
