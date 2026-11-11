
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from models import School, SchoolClass, Student


# Шлях до папки з CSV-файлами
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


# Завантаження даних зі школи
def load_school() -> School:
    school = School("Моя школа")

    # Завантажуємо інформацію про класи
    classes_df = pd.read_csv(DATA_DIR / "classes.csv")

    # Створюємо об'єкти класів
    for _, row in classes_df.iterrows():
        school_class = SchoolClass(
            int(row["parallel"]),
            str(row["vertical"])
        )
        school.add_class(school_class)

    # Створюємо словник для пошуку класів
    class_dict = {
        school_class.get_name(): school_class
        for school_class in school.classes
    }

    # Завантажуємо інформацію про учнів
    students_df = pd.read_csv(DATA_DIR / "students.csv")

    for _, row in students_df.iterrows():
        student = Student(
            last_name=str(row["last_name"]),
            first_name=str(row["first_name"]),
            middle_name=str(row["middle_name"]),
            birth_year=int(row["birth_year"]),
            gender=str(row["gender"]),
            average_grade=float(row["average_grade"])
        )

        class_name = (
            f"{int(row['class_parallel'])}"
            f"{row['class_vertical']}"
        )

        if class_name in class_dict:
            class_dict[class_name].add_student(student)

    return school


# Отримання статистики школи
def show_statistics(school: School, prefix: str) -> None:

    students = school.get_all_students()
    total_students = len(students)

    boys = sum(1 for s in students if s.gender == "Ч")
    girls = sum(1 for s in students if s.gender == "Ж")

    boys_percent = boys / total_students * 100 if total_students else 0
    girls_percent = girls / total_students * 100 if total_students else 0

    class_counts = [
        len(school_class.students)
        for school_class in school.classes
    ]

    average_count = (
        sum(class_counts) / len(class_counts)
        if class_counts else 0
    )

    # Пошук найбільшого та найменшого класу
    if school.classes:
        max_class = max(
            school.classes,
            key=lambda c: len(c.students)
        )
        min_class = min(
            school.classes,
            key=lambda c: len(c.students)
        )
    else:
        max_class = None
        min_class = None

    # Виведення статистики
    st.subheader("Загальна статистика")

    col1, col2, col3 = st.columns(3)

    col1.metric("Усього учнів", total_students)
    col2.metric("Хлопці", f"{boys_percent:.1f}%")
    col3.metric("Дівчата", f"{girls_percent:.1f}%")

    st.write(f"**Кількість хлопців:** {boys}")
    st.write(f"**Кількість дівчат:** {girls}")
    st.write(f"**Середня кількість учнів у класах:** {average_count:.2f}")

    if max_class and min_class:
        st.write(
            f"**Найбільший клас:** {max_class.get_name()} "
            f"({len(max_class.students)} учнів)"
        )
        st.write(
            f"**Найменший клас:** {min_class.get_name()} "
            f"({len(min_class.students)} учнів)"
        )

    # Підготовка даних для графіків
    class_data = []

    for school_class in school.classes:
        for student in school_class.students:
            class_data.append({
                "Клас": school_class.get_name(),
                "Паралель": school_class.parallel,
                "Вертикаль": school_class.vertical,
                "Рік народження": student.birth_year,
                "Середня оцінка": student.average_grade
            })

    df = pd.DataFrame(class_data)

    st.subheader("Графіки")

    if not df.empty:

        # Графік 1: кількість учнів за паралелями
        parallel_data = (
            df.groupby("Паралель")
            .size()
            .reset_index(name="Кількість учнів")
        )

        fig1 = px.bar(
            parallel_data,
            x="Паралель",
            y="Кількість учнів",
            title="Кількість учнів за паралелями"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True,
            key=f"{prefix}_chart_1"
        )

        # Графік 2: середня кількість учнів за вертикалями
        vertical_data = (
            pd.DataFrame([
                {
                    "Вертикаль": c.vertical,
                    "Кількість учнів": len(c.students)
                }
                for c in school.classes
            ])
            .groupby("Вертикаль")["Кількість учнів"]
            .mean()
            .reset_index()
        )

        fig2 = px.bar(
            vertical_data,
            x="Вертикаль",
            y="Кількість учнів",
            title="Середня кількість учнів за вертикалями"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True,
            key=f"{prefix}_chart_2"
        )

        # Графік 3: кількість учнів за роками народження
        birth_data = (
            df.groupby("Рік народження")
            .size()
            .reset_index(name="Кількість учнів")
            .sort_values("Рік народження")
        )

        fig3 = px.line(
            birth_data,
            x="Рік народження",
            y="Кількість учнів",
            markers=True,
            title="Кількість учнів за роками народження"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True,
            key=f"{prefix}_chart_3"
        )

        # Графік 4: залежність оцінки від класу
        fig4 = px.scatter(
            df,
            x="Клас",
            y="Середня оцінка",
            title="Середня оцінка учнів залежно від класу",
            hover_data=["Рік народження"]
        )

        st.plotly_chart(
            fig4,
            use_container_width=True,
            key=f"{prefix}_chart_4"
        )


# Основна частина програми
st.set_page_config(
    page_title="Система управління школою",
    page_icon="🏫",
    layout="wide"
)

st.title("🏫 Система управління школою")
st.write("Статистика та інформація про учнів")

# Завантажуємо школу
school = load_school()

# Початкова статистика
st.header("Початкові дані школи")
show_statistics(school, "before")

# Переведення класів на наступний рік
st.header("Переведення класів")

if st.button("Перевести всі класи на наступний рік"):

    school.promote_classes()

    st.success("Переведення класів успішно виконано!")

    st.write("Оновлений список класів:")
    st.write([c.get_name() for c in school.classes])

    st.header("Статистика після переведення")
    show_statistics(school, "after")

