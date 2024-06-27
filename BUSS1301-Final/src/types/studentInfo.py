from enum import Enum


class Gender(Enum):
    UNKNOWN = 0
    MALE = 1
    FEMALE = 2


class StudentInfo:
    def __init__(
        self,
        id: str = "",
        name: str = "",
        gender: Gender = Gender.UNKNOWN,
        chinese_grade: int = 0,
        math_grade: int = 0,
        english_grade: int = 0,
    ) -> None:
        self.id = id
        self.name = name
        self.gender = gender
        self.chinese_grade = chinese_grade
        self.math_grade = math_grade
        self.english_grade = english_grade
