'''
Faker - biblioteka do generowania danych testowych
'''

from faker import Faker

fake = Faker(['it_IT', 'en_US', 'ja_JP', 'pl_PL'])

# Generowanie danych (imie, nazwisko, email)
for _ in range(5):
    print("name: ", fake.name())
    print("email: ", fake.email())
    print("=====================================")

fake2 = Faker('pl_PL')

# Generowanie tekstu o podanej liczbie znaków
print(fake2.text(100))
