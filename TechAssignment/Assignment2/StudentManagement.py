import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().with_name("students.json")


class StudentManagementSystem:
    def __init__(self):
        self.students = self.load_data()

    def load_data(self):
        if not DATA_FILE.exists():
            return {}

        try:
            with DATA_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError("Invalid student data.")

            for roll, student in data.items():
                if (
                    not isinstance(student, dict)
                    or not isinstance(student.get("name"), str)
                    or not isinstance(student.get("marks"), dict)
                    or not student["marks"]
                ):
                    raise ValueError(f"Invalid record: {roll}")

                for mark in student["marks"].values():
                    if (
                        type(mark) is not int
                        or not 0 <= mark <= 100
                    ):
                        raise ValueError(f"Invalid marks: {roll}")

            return data

        except (OSError, ValueError) as error:
            raise SystemExit(
                f"Cannot load students.json: {error}\n"
                "Check the file before restarting."
            )

    def save_data(self):
        temporary_file = DATA_FILE.with_suffix(".tmp")

        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(self.students, file, indent=4)

        temporary_file.replace(DATA_FILE)

    @staticmethod
    def read_text(prompt):
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("This field cannot be empty.")

    @staticmethod
    def read_integer(prompt, minimum, maximum):
        while True:
            try:
                value = int(input(prompt))
                if minimum <= value <= maximum:
                    return value
            except ValueError:
                pass

            print(f"Enter an integer from {minimum} to {maximum}.")

    def read_marks(self):
        count = self.read_integer("Number of subjects (1–20): ", 1, 20)
        marks = {}

        for index in range(count):
            while True:
                subject = self.read_text(
                    f"Subject {index + 1} name: "
                ).title()

                if subject not in marks:
                    break

                print("Subject already entered.")

            marks[subject] = self.read_integer(
                f"Marks in {subject} (out of 100): ", 0, 100
            )

        return marks

    @staticmethod
    def calculate_result(marks):
        total = sum(marks.values())
        percentage = total / len(marks)

        # Assignment grading rule:
        # A student must score at least 33 in every subject.
        if any(mark < 33 for mark in marks.values()):
            grade = "F"
            result = "Fail"
        else:
            result = "Pass"

            if percentage >= 90:
                grade = "A+"
            elif percentage >= 80:
                grade = "A"
            elif percentage >= 70:
                grade = "B"
            elif percentage >= 60:
                grade = "C"
            elif percentage >= 50:
                grade = "D"
            else:
                grade = "E"

        return total, percentage, grade, result

    def display_student(self, roll):
        student = self.students[roll]
        total, percentage, grade, result = self.calculate_result(
            student["marks"]
        )

        print(f"\nRoll number: {roll}")
        print(f"Name: {student['name']}")

        for subject, mark in student["marks"].items():
            print(f"  {subject}: {mark}/100")

        maximum = len(student["marks"]) * 100
        print(f"Total: {total}/{maximum}")
        print(f"Percentage: {percentage:.2f}%")
        print(f"Grade: {grade}")
        print(f"Result: {result}")

    def add_student(self):
        roll = self.read_text("Roll number: ")

        if roll in self.students:
            print("This roll number already exists.")
            return

        name = self.read_text("Student name: ")
        marks = self.read_marks()

        self.students[roll] = {"name": name, "marks": marks}
        self.save_data()
        print("Student added successfully.")

    def view_students(self):
        if not self.students:
            print("No students found.")
            return

        for roll in sorted(self.students):
            self.display_student(roll)

    def search_student(self):
        query = self.read_text("Enter roll number or name: ")

        if query in self.students:
            self.display_student(query)
            return

        matches = [
            roll
            for roll, student in self.students.items()
            if query.casefold() in student["name"].casefold()
        ]

        if not matches:
            print("No matching students found.")
            return

        for roll in matches:
            self.display_student(roll)

    def update_student(self):
        roll = self.read_text("Roll number to update: ")

        if roll not in self.students:
            print("Student not found.")
            return

        student = self.students[roll]
        name = input(
            f"New name (Enter to keep '{student['name']}'): "
        ).strip()

        if name:
            student["name"] = name

        change_marks = input(
            "Replace subject marks? (y/n): "
        ).strip().lower()

        if change_marks == "y":
            student["marks"] = self.read_marks()

        self.save_data()
        print("Student updated successfully.")

    def delete_student(self):
        roll = self.read_text("Roll number to delete: ")

        if roll not in self.students:
            print("Student not found.")
            return

        confirmation = input(
            f"Delete {self.students[roll]['name']}? (y/n): "
        ).strip().lower()

        if confirmation == "y":
            del self.students[roll]
            self.save_data()
            print("Student deleted.")
        else:
            print("Deletion cancelled.")

    def run(self):
        actions = {
            "1": self.add_student,
            "2": self.view_students,
            "3": self.search_student,
            "4": self.update_student,
            "5": self.delete_student,
        }

        while True:
            print("\nSTUDENT MANAGEMENT SYSTEM")
            print("1. Add student")
            print("2. View all students")
            print("3. Search student")
            print("4. Update student")
            print("5. Delete student")
            print("6. Exit")

            choice = input("Choose an option: ").strip()

            if choice == "6":
                print("Program closed.")
                break

            action = actions.get(choice)

            if action:
                action()
            else:
                print("Invalid choice. Select 1–6.")


if __name__ == "__main__":
    try:
        StudentManagementSystem().run()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram closed.")
    except OSError as error:
        print(f"\nCould not save data: {error}")
        print("The latest change may not have been saved.")