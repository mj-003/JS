from faker import Faker
from faker.providers import BaseProvider

fake = Faker('pl_PL')  # Ustawienie języka na polski

# Tworzenie dostawcy dla zawodów medycznych
class Students(BaseProvider):
    first_names = ["Jan", "Anna", "Piotr", "Katarzyna", "Marcin", "Magdalena"]
    last_names = ["Nowak", "Kowalski", "Wiśniewski", "Wójcik", "Kamińska", "Lewandowski"]

    def first_name(self):
        return self.random_element(self.first_names)

    def last_name(self):
        return self.random_element(self.last_names)


# Tworzenie dostawcy dla zawodów nauczycielskich
class Teachers(BaseProvider):
    first_names = ["Aleksandra", "Michał", "Karolina", "Tomasz", "Monika", "Grzegorz"]
    last_names = ["Dąbrowska", "Zieliński", "Jankowski", "Szymańska", "Woźniak", "Kozłowski"]

    def first_name(self):
        return self.random_element(self.first_names)

    def last_name(self):
        return self.random_element(self.last_names)


fake.add_provider(Students)
fake.add_provider(Teachers)

# Tworzenie listy imion i nazwisk
students_data = [(fake.first_name(), fake.last_name()) for _ in range(5)]
teachers_data = [(fake.first_name(), fake.last_name()) for _ in range(60)]

# Wypisanie danych w formacie do kopiowania do Excela


print("\nImię\tNazwisko")
for first_name, last_name in teachers_data:
    print("{}\t{}".format(first_name, last_name))
