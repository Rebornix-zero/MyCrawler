# # 示例框架
# def menu():
#     print("""
#         —————————————————————学生信息管理系统———————————————————————--
#         |                                                          |
#         |         1 录入学生信息                                     |
#         |         2 从文件录入学生信息                                |
#         |         3 查找学生信息                                     |
#         |         4 删除学生信息                                     |
#         |         <todo: 这里根据题目自行补充>                         |
#         |         0 退出系统                                         |
#         |                                                          |
#         ------------------------------------------------------------
#         """)

# def insert():
#     while(True):
#         Str = input('请输入学生信息，格式如"学号，姓名，性别，语文成绩，数学成绩，英语成绩"：')
#         # 处理 Str，比如存储
#         if_continue = input('继续输入（Y/n）?')
#         if if_continue.lower() == 'n':
#             break

# def search():
#     print('还没实现呢')

# def delete():
#     print('还没实现呢')

# def main():
#     print("*****欢迎登陆学生信息管理系统*****")
#     flag_on = True
#     while flag_on:
#         menu()  # 显示页面菜单
#         option = int(input("请选择："))  # 选择菜单项 todo:这里需要更多判断，比如只允许输入整数等

#         if option == 0:  # 退出选择界面
#             print("您已经退出学生信息管理系统！")
#             flag_on = False
#         elif option == 1:  # 录入学生成绩信息
#             insert()
#         elif option == 2:  # 查询学生成绩信息
#             search()
#         elif option == 3:  # 删除学生成绩信息
#             delete()
#         else:
#             print('还没实现呢')
from .printMessage import *
from ..utils.utils import *
from ..config import config


class StudentInfoManager:
    def __init__(self) -> None:
        self.can_exit = False
        # 维护加载至内存中的student info list
        # 一个字典，映射关系是id -> strudent info
        self.student_info_list = {}

    def manual(self) -> None:
        print(MANUAL_MESSAGE)
        input("Print [Enter] to back")

    def add(self) -> None:
        student_str = input(ADD_MESSAGE)
        try:
            student_info = Str2StudentInfo(student_str)
            self.student_info_list[student_info.id] = student_info
            print(ADD_SUCCESS)
        except RuntimeError as e:
            print(e)

    def load(self) -> None:
        file_path = input(LOAD_MESSAGE)
        try:
            self.load_from_csv(file_path)
            print(LOAD_SUCCEED)
        except Exception as e:
            print("An error occurred:", e)

    def filter(self) -> None:
        filter_str = input(FILTER_MESSAGE)
        id_list = FilterByCondition(filter_str, self.student_info_list)
        print(FILTER_OUTPUT)
        print(OUTPUT_LIST_HEADER)
        for id_item in id_list:
            print(StudentInfo2ShowStr(self.student_info_list[id_item]))

    def delete(self) -> None:
        filter_str = input(DELETE_MESSAGE)
        id_list = FilterByCondition(filter_str,self.student_info_list)
        print(FILTER_OUTPUT)
        print(OUTPUT_LIST_HEADER)
        for id_item in id_list:
            print(StudentInfo2ShowStr(self.student_info_list[id_item]))
        can_exit = (len(id_list)==0)
        while not can_exit:
            ack_str = input(DELETE_ACK)
            if ack_str == "y":
                can_exit = True
                print(DELETE_IN)
                for id_item in id_list:
                    del self.student_info_list[id_item]
                print(DELETE_MESSAGE_SUCCESS)
            elif ack_str == "n":
                can_exit = True
                print(DELETE_NOT)
            else:
                print(DELETE_UNKNOWN)

    def show_all(self) -> None:
        print(SHOWALL_MESSAGE)
        print(OUTPUT_LIST_HEADER)
        for value in self.student_info_list.values():
            print(StudentInfo2ShowStr(value))

    def clear_all(self) -> None:
        can_exit = False
        while not can_exit:
            ack_str = input(CLEARALL_ACK)
            if ack_str == "y":
                can_exit = True
                print(CLEARALL_MESSAGE)
                self.student_info_list = {}
                print(CLEARALL_MESSAGE_SUCCESS)
            elif ack_str == "n":
                can_exit = True
                print(CLEARALL_NOT)
            else:
                print(CLEARALL_UNKNOWN)

    def exit(self) -> None:
        print(EXIT_MESSAGE)
        self.can_exit = True
        try:
            with open(config.DEFAULT_SAVE_PATH, "w") as file:
                for value in self.student_info_list.values():
                    file.write(StudentInfo2Str(value) + "\n")
        except Exception as e:
            print("An error occurred:", e)

    def load_from_csv(self, file_path: str) -> None:
        with open(file_path, "r") as file:
            for line in file:
                try:
                    student_info = Str2StudentInfo(line)
                    if student_info.id in self.student_info_list:
                        print("Override student {} info by csv data".format(student_info.id))
                    self.student_info_list[student_info.id] = student_info
                except RuntimeError as e:
                    print(e)

    def run(self) -> None:
        print(WELCOME_MESSAGE)
        print("Load save data...")
        self.load_from_csv(config.DEFAULT_SAVE_PATH)
        print("Load finish")
        self.can_exit = False
        while not self.can_exit:
            print("")
            print(SELECT_MESSAGE)
            try:
                num_str = input()
                if(num_str==""):
                    continue
                num = int(num_str)
                if num == 0:
                    self.manual()

                elif num == 1:
                    is_continue = True
                    while is_continue:
                        self.add()
                        ack_str = input("Continue adding?[y/n]")
                        if ack_str == "y":
                            is_continue = True
                        elif ack_str == "n":
                            is_continue = False
                        else:
                            print("Unknown input, try again.")

                elif num == 2:
                    self.load()

                elif num == 3:
                    is_continue = True
                    while is_continue:
                        self.filter()
                        ack_str = input("Continue filtering?[y/n]")
                        if ack_str == "y":
                            is_continue = True
                        elif ack_str == "n":
                            is_continue = False
                        else:
                            print("Unknown input, try again.")

                elif num == 4:
                    is_continue = True
                    while is_continue:
                        self.delete()
                        ack_str = input("Continue deleting?[y/n]")
                        if ack_str == "y":
                            is_continue = True
                        elif ack_str == "n":
                            is_continue = False
                        else:
                            print("Unknown input, try again.")

                elif num == 5:
                    self.show_all()

                elif num == 6:
                    self.clear_all()

                elif num == 7:
                    self.exit()

                else:
                    print("[Error]Unknown function number!")

            except ValueError:
                print("[Error]Invaild input format, Please input a number!\n")


def newStudentInfoManager() -> StudentInfoManager:
    return StudentInfoManager()
