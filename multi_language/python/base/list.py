if __name__ == '__main__':
    learn_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print("list: ", learn_list)
    print("list size: ", len(learn_list))
    print('list[0]', learn_list[0])
    print('list[-1]', learn_list[-1])
    learn_list.append(11)
    print("list size: ", len(learn_list))
    print('list[-1]', learn_list[-1])
    learn_list.insert(1, -1)
    print('list[1]', learn_list[1])
    print('remove last')
    learn_list.pop()
    print('list[-1]', learn_list[-1])
    print('replace index 1 to 0')
    learn_list[0] = 0
    print('list[0]', learn_list[0])

    ## tuple是不可变list

    ## 切片
    print("list: ", learn_list)
    print("list[0] ~ list[3]: ", learn_list[0:3])
    print("list[0] ~ list[3]: ", learn_list[:3])
    print("list[-3] ~ list[-1]: ", learn_list[-3:-1])
    print("list[-1] ~ list[1]: ", learn_list[-1:1])
    print("list[1],list[3]...", learn_list[::2])

    ## 字符串也可以看作是list