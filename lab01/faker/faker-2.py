'''
Faker - biblioteka do generowania danych testowych
'''

from faker import Faker
from faker.providers import BaseProvider


# Tworzenie dostawcy dla zawodów medycznych
class MedicalProfessionProvider(BaseProvider):
    professions = ["doctor", "nurse", "surgeon", "dentist", "psychiatrist"]

    def medical_profession(self):
        return self.random_element(self.professions)


fake = Faker()

# Dodanie dostawcy do obiektu Faker
fake.add_provider(MedicalProfessionProvider)

for _ in range(10):
    print(fake.medical_profession())
