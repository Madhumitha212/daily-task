from faker import Faker
import random

fake = Faker()
with open("sample_text.txt","w") as file:
    for _ in range(0,1440):
        file.write(str(random.randint(0,200)))
        file.write("\n")