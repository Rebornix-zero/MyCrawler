# 1.录入学生信息
# 2.从csv文件录入学生信息
# 3.查找学生信息
# 4.删除学生信息
# 5.显示所有学生信息
# 6.清空所有学生信息
# 7.退出系统(退出前数据保存在data/data.csv中，启动时从data/data.csv中加载数据)
from src.studentInfoManager.studentInfoManager import newStudentInfoManager

if __name__ == "__main__":
    student_info_manager = newStudentInfoManager()
    student_info_manager.run()
