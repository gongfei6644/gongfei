# 练习：定义函数，将列表中0元素，移动到末尾。
# [2,0,2,0]   -->  [2,2,0,0]
# [0,4,2,4]   -->  [4,2,4,0]

# 适合零基础同学
# def zero_to_end(list_target):
#     # 选出非零元素 形成新列表
#     # [2, 0, 2, 0] -->  [2, 2]
#     new_list = []
#     for item in list_target:
#         if item != 0:
#             new_list.append(item)
#             # 追加零元素 [2, 2] --> [2,2,0,0]
#     # 判断原列表零元素数量： list_target.count(0)
#     for i in range(list_target.count(0)):
#         new_list.append(0)
#         # 返回新列表
#     return new_list


# def zero_to_end(list_target):
#     # 选出非零元素 形成新列表
#     # [2, 0, 2, 0] -->  [2, 2]
#     new_list = [item for item in list_target if item != 0]
#     # 重复生成零元素 [0] * list_target.count(0)
#     new_list += [0] * list_target.count(0)
#     # 返回新列表
#     return new_list

def zero_to_end(list_target):
    # 删除零元素  在后面追加
    for item in list_target:
        if item == 0:
            list_target.remove(item)
            list_target.append(item)
    # 返回新列表
    return list_target

print(zero_to_end([1, 0, 0, 2]))
print(zero_to_end([0, 4, 2, 4]))

