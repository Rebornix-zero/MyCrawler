# 1.录入学生信息
# 2.从csv文件录入学生信息
# 3.查找学生信息
# 4.删除学生信息
# 5.显示所有学生信息
# 6.清空所有学生信息
# 7.退出系统(退出前数据保存在data/data.csv中，启动时从data/data.csv中加载数据)

WELCOME_MESSAGE = """
****** Welcome to Student Information Management System *****"""

SELECT_MESSAGE = "Please select your action number(input 0 to see the manual):"

MANUAL_MESSAGE = """****** Manual of Student Information Management System *****
    1. Add a piece of student info from shell
    2. Load student info list from csv
    3. Filter student info
    4. Delete student info
    5. Show all records
    6. Clear all records 
    7. exit 

****** Select synatx ******
所有的筛选规则按照如下顺序列出，顺序越靠前，代表越先检测
NOTE: 字段有ID, Gender, Chinese_Grade, Math_Grade, English_Grade, Name字段,参考展示的效果即可
比较算法
    ==, !=:
        所有field均可使用此符号
    >=, <=:
        只有学号，三类分数可使用此符号
    <, >:
        只有学号，三类分数可使用此符号
成员算法
    in, not in:
        所有field均可使用此符号"""

OUTPUT_LIST_HEADER = "ID\tGender\tChinese_Grade\tMath_Grade\tEnglish_Grade\tName"

ADD_MESSAGE = "Please input student info:\n"
ADD_SUCCESS = "Add student succeed!"


LOAD_MESSAGE = "Please give the path of .csv file:\n"
LOAD_SUCCEED = "Load data succeed"

FILTER_MESSAGE = "Please input the filter condition:\n"
FILTER_OUTPUT = "Filtered records:"

DELETE_MESSAGE = "Please inuput the delete condition:\n"
DELETE_ACK = "Confirm deletion ?[y/n]:"
DELETE_NOT = "Deletion cancel, back"
DELETE_UNKNOWN = "Invaild input, try again"
DELETE_IN = "Delete records..."
DELETE_MESSAGE_SUCCESS = "Delete records succeed"


SHOWALL_MESSAGE = "Show all records:"

CLEARALL_ACK = "Confirm clear?[y/n]:"
CLEARALL_NOT = "Cancel clear, back"
CLEARALL_UNKNOWN = "Invaild input, try again"
CLEARALL_MESSAGE = "Clear all records..."
CLEARALL_MESSAGE_SUCCESS = "Clear all records succeed"

EXIT_MESSAGE = "Exit system"
