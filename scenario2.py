
import csv
from pathlib import Path

from models import School, Director, Teacher, SecurityGuard

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

school = School("Моя школа")

# Створюємо працівників
school.add_employee(Director("Петренко", "Іван", 20, 10))

school.add_employee(Teacher("Шевченко", "Олена", "Математика", 15))
school.add_employee(Teacher("Коваленко", "Андрій", "Фізика", 10))
school.add_employee(Teacher("Бондаренко", "Марія", "Інформатика", 25))

school.add_employee(SecurityGuard("Мельник", "Микола", 12))
school.add_employee(SecurityGuard("Ткаченко", "Олег", 5))

# Записуємо дані у CSV
file_path = OUTPUT_DIR / "salaries.csv"

with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(["Посада", "Прізвище", "Ім'я", "Зарплата"])

    for employee in school.employees:
        writer.writerow([
            type(employee).__name__,
            employee.surname,
            employee.first_name,
            employee.calculate_salary()
        ])

# Виводимо зарплати
print("Зарплати працівників школи:")
print("-" * 45)

for employee in school.employees:
    print(
        f"{type(employee).__name__}: "
        f"{employee.surname} {employee.first_name} — "
        f"{employee.calculate_salary():.2f} грн"
    )

print("\nФайл salaries.csv успішно створено!")
print(file_path)
