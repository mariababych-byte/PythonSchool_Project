class Student:
    """Клас для представлення учня."""

    def __init__(
        self,
        last_name: str,
        first_name: str,
        middle_name: str,
        birth_year: int,
        gender: str,
        average_grade: float
    ):
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.birth_year = birth_year
        self.gender = gender
        self.average_grade = average_grade

    def get_full_name(self) -> str:
        return f"{self.last_name} {self.first_name} {self.middle_name}"

class SchoolClass:
    """Клас для представлення шкільного класу."""
    def get_name(self) -> str:
        return f"{self.parallel}{self.vertical}"
    def __init__(self, parallel: int, vertical: str):
        self.parallel = parallel
        self.vertical = vertical
        self.students: list[Student] = []

    @property
    def name(self) -> str:
        return f"{self.parallel}{self.vertical}"

    def add_student(self, student: Student) -> None:
        self.students.append(student)

    def get_average_grade(self) -> float:
        if not self.students:
            return 0.0

        return sum(s.average_grade for s in self.students) / len(self.students)

    def advance_year(self) -> None:
        self.parallel += 1


class Employee:
    """Базовий клас для працівників школи."""

    def __init__(self, surname: str, first_name: str, base_salary: float):
        self.surname = surname
        self.first_name = first_name
        self.base_salary = base_salary

    def calculate_salary(self) -> float:
        return self.base_salary


class Director(Employee):
    """Клас директора."""

    def __init__(self, surname: str, first_name: str,
                 pedagogical_experience: int, management_experience: int):
        super().__init__(surname, first_name, 15000)
        self.pedagogical_experience = pedagogical_experience
        self.management_experience = management_experience

    def calculate_salary(self) -> float:
        return (
            self.base_salary * self.pedagogical_experience / 50
            + self.management_experience * 500
        )


class Teacher(Employee):
    """Клас вчителя."""

    def __init__(self, surname: str, first_name: str,
                 subject: str, pedagogical_experience: int):
        super().__init__(surname, first_name, 12000)
        self.subject = subject
        self.pedagogical_experience = pedagogical_experience

    def calculate_salary(self) -> float:
        return self.base_salary * self.pedagogical_experience / 30


class SecurityGuard(Employee):
    """Клас охоронця."""

    def __init__(self, surname: str, first_name: str, work_experience: int):
        super().__init__(surname, first_name, 11000)
        self.work_experience = work_experience

    def calculate_salary(self) -> float:
        return self.base_salary + self.work_experience * 250



class School:
    """Головний клас для керування школою."""

    def __init__(self, name: str):
        self.name = name
        self.classes: list[SchoolClass] = []
        self.employees: list[Employee] = []

    def add_class(self, school_class: SchoolClass) -> None:
        self.classes.append(school_class)

    def get_all_students(self) -> list[Student]:
        students = []
        for school_class in self.classes:
            students.extend(school_class.students)
        return students

    def add_employee(self, employee: Employee) -> None:
        self.employees.append(employee)

    def promote_classes(self) -> None:
        new_classes = []

        for school_class in self.classes:
            if school_class.parallel < 11:
                school_class.parallel += 1
                new_classes.append(school_class)

        self.classes = new_classes



