information = {}

def show_menu():
    print("=" * 30)
    print("      学生宿舍管理系统")
    print("  1. 按学号查找学生信息")
    print("  2. 录入新的学生信息")
    print("  3. 显示所有学生信息")
    print("  4. 退出系统")
    print("=" * 30)

def defi_phone(phone):
    if len(phone) == 11 and phone.isdigit():
        return True
    return False

def phone_chongfu(phone):
    for info in information.values():
        if info['phone'] == phone:
            return True
    return False

def search():
    student_id = input("请输入要查找的学生学号：").strip()
    if not student_id:
        print("学号不能为空 请重新操作！")
        return
    
    if student_id in information:
        info = information[student_id]
        print("\n查找结果如下：")
        print(f"学号：{student_id}")
        print(f"姓名：{info['name']}")
        print(f"性别：{info['gender']}")
        print(f"宿舍房间号：{info['dorm']}")
        print(f"联系电话：{info['phone']}\n")
    else:
        print(f"未找到学号为 {student_id} 的学生信息！\n")

def add_student():
    print("请录入新学生信息")
    
    student_id = input("学号：").strip()
    if not student_id:
        print("学号不能为空，录入失败！\n")
        return
    if student_id in information:
        print(f"错误：学号 {student_id} 已存在，请勿重复录入！\n")
        return
    
    name = input("姓名：").strip()
    if not name:
        print("姓名不能为空，录入失败！\n")
        return
    
    gender = input("性别（男/女）：").strip()
    if gender not in ["男", "女"]:
        print("性别必须为'男'或'女'，录入失败！\n")
        return
    
    dorm = input("宿舍房间号：").strip()
    if not dorm:
        print("宿舍房间号不能为空，录入失败！\n")
        return
    
    phone = input("联系电话（11位数字）：").strip()
    if not defi_phone(phone):
        print("联系电话必须是11位数字，录入失败！\n")
        return
    if phone_chongfu(phone):
        print(f"错误：电话号码 {phone} 已存在，请勿重复录入！\n")
        return
    
    information[student_id] ={
        "name": name,
        "gender": gender,
        "dorm": dorm,
        "phone": phone
    }
    print("学生信息录入成功！\n")

def show_all():
    if not information:
        print("当前暂无学生信息！\n")
        return
    
    print("=" * 60)
    print(f"{'学号':<12}{'姓名':<8}{'性别':<6}{'宿舍房间号':<12}{'联系电话':<15}")
    print("=" * 60)
    
    for sid, info in information.items():
        print(f"{sid:<12}{info['name']:<8}{info['gender']:<6}{info['dorm']:<12}{info['phone']:<15}")
    print("=" * 60 + "\n")

def main():
    while True:
        show_menu()
        try:
            choice = int(input("请输入功能序号（1-4）：").strip())
            if choice == 1:
                search()
            elif choice == 2:
                add_student()
            elif choice == 3:
                show_all()
            elif choice == 4:
                print("感谢使用学生宿舍管理系统，再见！")
                break
            else:
                print("请输入1-4之间的有效序号！\n")
        except ValueError:
            print("输入无效，请输入数字序号！\n")

if __name__ == "__main__":
    main()
