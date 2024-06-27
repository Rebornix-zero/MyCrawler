from ..types.studentInfo import *
import re
from typing import Dict


def Str2StudentInfo(info_str: str) -> StudentInfo:
    # 分割字符串
    info_list = info_str.split(",")
    # print(info_list)
    c_grade = 0
    m_grade = 0
    e_grade = 0
    # 检查分割后的格式和长度
    if len(info_list) != 6:
        # info数量不等于6,肯定不符合格式
        raise RuntimeError("[ERROR]Missing or Redundant Student Information!")
    # 去掉前后空格
    for i in range(6):
        info_list[i] = info_list[i].strip()
    # 检查学号
    if not IsIdInvaild(info_list[0]):
        raise RuntimeError("[ERROR]Invaild Id format!")
    # 检查姓名
    if info_list[1] == "":
        raise RuntimeError("[ERROR]Null name is invaild!")
    # 检查性别
    if info_list[2] != Gender.FEMALE.name and info_list[2] != Gender.MALE.name:
        raise RuntimeError(
            '[ERROR]Invaild gender format, can only be "{}" or "{}"!'.format(
                Gender.FEMALE.name, Gender.MALE.name
            )
        )
    # 检查语文成绩
    try:
        c_grade = int(info_list[3])
    except ValueError:
        raise RuntimeError(
            "[Error]Invaild chinese grade format, Please input a number!\n"
        )
    if c_grade < 0 or c_grade > 100:
        raise RuntimeError(
            "[Error]Invaild chinese grade, the grade range should be 0-100!\n"
        )
    # 检查数学成绩
    try:
        m_grade = int(info_list[4])
    except ValueError:
        raise RuntimeError("[Error]Invaild math grade format, Please input a number!\n")
    if m_grade < 0 or m_grade > 100:
        raise RuntimeError(
            "[Error]Invaild math grade, the grade range should be 0-100!\n"
        )
    # 检查英语成绩
    try:
        e_grade = int(info_list[5])
    except ValueError:
        raise RuntimeError(
            "[Error]Invaild english grade format, Please input a number!\n"
        )
    if e_grade < 0 or e_grade > 100:
        raise RuntimeError(
            "[Error]Invaild english grade, the grade range should be 0-100!\n"
        )
    # 全部合法，可以返回一个StudentInfo
    return StudentInfo(
        info_list[0], info_list[1], str2Gender(info_list[2]), c_grade, m_grade, e_grade
    )


def StudentInfo2Str(sinfo: StudentInfo) -> str:
    result = ""
    result += sinfo.id + ","
    result += sinfo.name + ","
    result += sinfo.gender.name + ","
    result += str(sinfo.chinese_grade) + ","
    result += str(sinfo.math_grade) + ","
    result += str(sinfo.english_grade)
    return result


def StudentInfo2ShowStr(sinfo: StudentInfo) -> str:
    result = ""
    result += sinfo.id + "\t"
    result += sinfo.gender.name + "\t"
    result += str(sinfo.chinese_grade) + "\t\t"
    result += str(sinfo.math_grade) + "\t\t"
    result += str(sinfo.english_grade) + "\t\t"
    result += sinfo.name
    return result


def IsIdInvaild(id: str) -> bool:
    # print("id",id)
    pattern = r"^\d{5}$"
    if re.match(pattern, id):
        return id[0] != "0"
    else:
        return False


def str2Gender(id: str) -> Gender:
    if id == Gender.MALE.name:
        return Gender.MALE
    if id == Gender.FEMALE.name:
        return Gender.FEMALE
    return Gender.UNKNOWN


ID = "ID"
GENDER = "Gender"
CHINESE_GRADE = "Chinese_Grade"
MATH_GRADE = "Math_Grade"
ENGLISH_GRADE = "English_Grade"
NAME = "Name"

# 所有的筛选规则按照如下顺序列出，顺序越靠前，代表越先检测
# NOTE: 字段有ID, Gender, Chinese_Grade, Math_Grade, English_Grade, Name字段,参考展示的效果即可
# 比较算法
#   ==, !=:
#       所有field均可使用此符号
#   >=, <=:
#       只有学号，三类分数可使用此符号
#   <, >:
#       只有学号，三类分数可使用此符号
# 成员算法
#   in, not in:
#       所有field均可使用此符号


def FieldTypeAndPosition(left: str, right: str) -> tuple[bool, str]:
    if left == ID:
        return True, ID
    if left == GENDER:
        return True, GENDER
    if left == CHINESE_GRADE:
        return True, CHINESE_GRADE
    if left == MATH_GRADE:
        return True, MATH_GRADE
    if left == ENGLISH_GRADE:
        return True, ENGLISH_GRADE
    if left == NAME:
        return True, NAME
    if right == ID:
        return False, ID
    if right == GENDER:
        return False, GENDER
    if right == CHINESE_GRADE:
        return False, CHINESE_GRADE
    if right == MATH_GRADE:
        return False, MATH_GRADE
    if right == ENGLISH_GRADE:
        return False, ENGLISH_GRADE
    if right == NAME:
        return False, NAME
    raise Exception("[ERROR in FieldTypeAndPosition]Where is the placeholder?")


def FilterByCondition(
    condition: str, student_info_list: dict[str, StudentInfo]
) -> list[str]:
    try:
        r = re.compile("(==|!=|>=|<=| in | not in )")
        split_list = r.split(condition)
        if len(split_list) == 3:
            for i in range(3):
                split_list[i] = split_list[i].strip()
            isleft, type = FieldTypeAndPosition(split_list[0], split_list[2])
            if split_list[1] == "==":
                # 匹配==
                return MatchEqual(isleft, type, split_list, student_info_list)
            elif split_list[1] == "!=":
                # 匹配!=
                return MatchNotEqual(isleft, type, split_list, student_info_list)
            elif split_list[1] == ">=":
                # 匹配>=
                return MatchGreaterEqual(isleft, type, split_list, student_info_list)
            elif split_list[1] == "<=":
                # 匹配<=
                return MatchLessEqual(isleft, type, split_list, student_info_list)
            elif split_list[1] == "in":
                # 匹配in
                return MatchIn(isleft, type, split_list, student_info_list)
            elif split_list[1] == "not in":
                # 匹配not in
                return MatchNotIn(isleft, type, split_list, student_info_list)

        r = re.compile("(>|<)")
        split_list = r.split(condition)
        if len(split_list) == 3:
            for i in range(3):
                split_list[i] = split_list[i].strip()
            isleft, type = FieldTypeAndPosition(split_list[0], split_list[2])
            if split_list[1] == ">":
                # 匹配>
                return MatchGreater(isleft, type, split_list, student_info_list)
            elif split_list[1] == "<":
                # 匹配<
                return MatchLess(isleft, type, split_list, student_info_list)

        # 上述任一匹配成功，就会返回，否则，匹配失败
        print("Invaild filter syntax!")
    except Exception as e:
        print("An error occurred:", e)
    return []

def MatchEqual(
    isleft: bool,
    type: str,
    split_list: list[str],
    student_info_list: dict[str, StudentInfo],
) -> list[str]:
    result = []
    values = ["", ""]
    st_va_pos = 0
    # isleft代表了要从学生信息中取出占位符的位置
    if isleft:
        st_va_pos = 0
        values[1] = split_list[2]
    else:
        st_va_pos = 1
        values[0] = split_list[0]

    for k, s_item in student_info_list.items():
        if type == ID:
            values[st_va_pos] = s_item.id
        elif type == NAME:
            values[st_va_pos] = s_item.name
        elif type == GENDER:
            values[st_va_pos] = s_item.gender.name
        elif type == CHINESE_GRADE:
            values[st_va_pos] = str(s_item.chinese_grade)
        elif type == MATH_GRADE:
            values[st_va_pos] = str(s_item.math_grade)
        elif type == ENGLISH_GRADE:
            values[st_va_pos] = str(s_item.english_grade)
        if values[0] == values[1]:
            result.append(k)
    return result


def MatchNotEqual(
    isleft: bool,
    type: str,
    split_list: list[str],
    student_info_list: dict[str, StudentInfo],
) -> list[str]:
    result = []
    values = ["", ""]
    st_va_pos = 0
    # isleft代表了要从学生信息中取出占位符的位置
    if isleft:
        st_va_pos = 0
        values[1] = split_list[2]
    else:
        st_va_pos = 1
        values[0] = split_list[0]

    for k, s_item in student_info_list.items():
        if type == ID:
            values[st_va_pos] = s_item.id
        elif type == NAME:
            values[st_va_pos] = s_item.name
        elif type == GENDER:
            values[st_va_pos] = s_item.gender.name
        elif type == CHINESE_GRADE:
            values[st_va_pos] = str(s_item.chinese_grade)
        elif type == MATH_GRADE:
            values[st_va_pos] = str(s_item.math_grade)
        elif type == ENGLISH_GRADE:
            values[st_va_pos] = str(s_item.english_grade)
        if values[0] != values[1]:
            result.append(k)
    return result


def MatchGreaterEqual(
    isleft: bool,
    type: str,
    split_list: list[str],
    student_info_list: dict[str, StudentInfo],
) -> list[str]:
    try:
        result = []
        values = [0, 0]
        st_va_pos = 0
        # isleft代表了要从学生信息中取出占位符的位置
        if isleft:
            st_va_pos = 0
            values[1] = int(split_list[2])
        else:
            st_va_pos = 1
            values[0] = int(split_list[0])

        for k, s_item in student_info_list.items():
            if type == ID:
                values[st_va_pos] = int(s_item.id)
            elif type == NAME:
                raise Exception("[Error]can't filter Name in >=")
            elif type == GENDER:
                raise Exception("[Error]can't filter Gender in >=")
            elif type == CHINESE_GRADE:
                values[st_va_pos] = s_item.chinese_grade
            elif type == MATH_GRADE:
                values[st_va_pos] = s_item.math_grade
            elif type == ENGLISH_GRADE:
                values[st_va_pos] = s_item.english_grade
            if values[0] >= values[1]:
                result.append(k)
        return result
    except Exception as e:
        print("An error occurred:", e)
    return []


def MatchLessEqual(
    isleft: bool,
    type: str,
    split_list: list[str],
    student_info_list: dict[str, StudentInfo],
) -> list[str]:
    try:
        result = []
        values = [0, 0]
        st_va_pos = 0
        # isleft代表了要从学生信息中取出占位符的位置
        if isleft:
            st_va_pos = 0
            values[1] = int(split_list[2])
        else:
            st_va_pos = 1
            values[0] = int(split_list[0])

        for k, s_item in student_info_list.items():
            if type == ID:
                values[st_va_pos] = int(s_item.id)
            elif type == NAME:
                raise Exception("[Error]can't filter Name in <=")
            elif type == GENDER:
                raise Exception("[Error]can't filter Gender in <=")
            elif type == CHINESE_GRADE:
                values[st_va_pos] = s_item.chinese_grade
            elif type == MATH_GRADE:
                values[st_va_pos] = s_item.math_grade
            elif type == ENGLISH_GRADE:
                values[st_va_pos] = s_item.english_grade
            if values[0] <= values[1]:
                result.append(k)
        return result
    except Exception as e:
        print("An error occurred:", e)
    return []


def MatchGreater(
    isleft: bool,
    type: str,
    split_list: list[str],
    student_info_list: dict[str, StudentInfo],
) -> list[str]:
    try:
        result = []
        values = [0, 0]
        st_va_pos = 0
        # isleft代表了要从学生信息中取出占位符的位置
        if isleft:
            st_va_pos = 0
            values[1] = int(split_list[2])
        else:
            st_va_pos = 1
            values[0] = int(split_list[0])

        for k, s_item in student_info_list.items():
            if type == ID:
                values[st_va_pos] = int(s_item.id)
            elif type == NAME:
                raise Exception("[Error]can't filter Name in >")
            elif type == GENDER:
                raise Exception("[Error]can't filter Gender in >")
            elif type == CHINESE_GRADE:
                values[st_va_pos] = s_item.chinese_grade
            elif type == MATH_GRADE:
                values[st_va_pos] = s_item.math_grade
            elif type == ENGLISH_GRADE:
                values[st_va_pos] = s_item.english_grade
            if values[0] > values[1]:
                result.append(k)
        return result
    except Exception as e:
        print("An error occurred:", e)
    return []


def MatchLess(
    isleft: bool,
    type: str,
    split_list: list[str],
    student_info_list: dict[str, StudentInfo],
) -> list[str]:
    try:
        result = []
        values = [0, 0]
        st_va_pos = 0
        # isleft代表了要从学生信息中取出占位符的位置
        if isleft:
            st_va_pos = 0
            values[1] = int(split_list[2])
        else:
            st_va_pos = 1
            values[0] = int(split_list[0])

        for k, s_item in student_info_list.items():
            if type == ID:
                values[st_va_pos] = int(s_item.id)
            elif type == NAME:
                raise Exception("[Error]can't filter Name in <")
            elif type == GENDER:
                raise Exception("[Error]can't filter Gender in <")
            elif type == CHINESE_GRADE:
                values[st_va_pos] = s_item.chinese_grade
            elif type == MATH_GRADE:
                values[st_va_pos] = s_item.math_grade
            elif type == ENGLISH_GRADE:
                values[st_va_pos] = s_item.english_grade
            if values[0] < values[1]:
                result.append(k)
        return result
    except Exception as e:
        print("An error occurred:", e)
    return []


def MatchIn(
    isleft: bool,
    type: str,
    split_list: list[str],
    student_info_list: dict[str, StudentInfo],
) -> list[str]:
    result = []
    values = ["", ""]
    st_va_pos = 0
    # isleft代表了要从学生信息中取出占位符的位置
    if isleft:
        st_va_pos = 0
        values[1] = split_list[2]
    else:
        st_va_pos = 1
        values[0] = split_list[0]

    for k, s_item in student_info_list.items():
        if type == ID:
            values[st_va_pos] = s_item.id
        elif type == NAME:
            values[st_va_pos] = s_item.name
        elif type == GENDER:
            values[st_va_pos] = s_item.gender.name
        elif type == CHINESE_GRADE:
            values[st_va_pos] = str(s_item.chinese_grade)
        elif type == MATH_GRADE:
            values[st_va_pos] = str(s_item.math_grade)
        elif type == ENGLISH_GRADE:
            values[st_va_pos] = str(s_item.english_grade)
        if values[0] in values[1]:
            result.append(k)
    return result


def MatchNotIn(
    isleft: bool,
    type: str,
    split_list: list[str],
    student_info_list: dict[str, StudentInfo],
) -> list[str]:
    result = []
    values = ["", ""]
    st_va_pos = 0
    # isleft代表了要从学生信息中取出占位符的位置
    if isleft:
        st_va_pos = 0
        values[1] = split_list[2]
    else:
        st_va_pos = 1
        values[0] = split_list[0]

    for k, s_item in student_info_list.items():
        if type == ID:
            values[st_va_pos] = s_item.id
        elif type == NAME:
            values[st_va_pos] = s_item.name
        elif type == GENDER:
            values[st_va_pos] = s_item.gender.name
        elif type == CHINESE_GRADE:
            values[st_va_pos] = str(s_item.chinese_grade)
        elif type == MATH_GRADE:
            values[st_va_pos] = str(s_item.math_grade)
        elif type == ENGLISH_GRADE:
            values[st_va_pos] = str(s_item.english_grade)
        if values[0] not in values[1]:
            result.append(k)
    return result
