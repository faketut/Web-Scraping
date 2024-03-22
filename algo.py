# 第二题 算法题目
# 每输入一个字符串，检查括号是否匹配。如果只有左括号没有右括号，我们就在它下面标一个
# x，如果只有右括号，我们就在它下面标一个问号。每行为单独测试用例。
# 样例输入：
# bge)))))))))
# ((IIII))))))
# ()()()()(uuu
# ))))UUUU((()
# 样例输出：
# bge)))))))))
#    ?????????
# ((IIII))))))
#         ????
# ()()()()(uuu
#         x
# ))))UUUU((()
# ????    xx
class BracketInfo:
    def __init__(self, index, char):
        self.index = index
        self.char = char

def check_brackets(string):
    stack = []
    res = [' '] * len(string)
    # Balance brackets and record bracket information
    for index, char in enumerate(string):
        if char == '(':
            stack.append(BracketInfo(index, char))
        elif char == ')':
            if stack:
                stack.pop()
            else:
                res[index] = '?'
    # record the extra left bracket
    for b in stack:
        if b.char == '(':
            i = b.index
            res[i] = 'x'
 
    # substring res
    res = ''.join(res)
    res = res[:len(string)]
    # print 
    print(string)
    print(''.join(res))

if __name__ == "__main__":
    test_cases = [
        "bge)))))))))",
        "((IIII))))))",
        "()()()()(uuu",
        "))))UUUU((()"
    ]

    for test_case in test_cases:
        check_brackets(test_case)
        
