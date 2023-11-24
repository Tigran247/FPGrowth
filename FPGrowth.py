class node(object):
    def __init__(self, name2):
        self._name = name2
        self._node = []
        self._count = 0
        self._prev = None

    def prev(self):
        return self._prev

    def node_len(self):
        return len(self._node)

    def count_add(self):
        self._count += 1

    def node_id(self, id):
        return self._node[id]

    def node_char(self, char):
        for i in range(len(self._node)):
            if (self._node[i]._name == char):
                return i
        return -1

    def add(self, name):
        node1 = node(name)
        self._node.append(node1)
        node1._prev = self
        return node1

    def return_root(self):
        while (self._prev != None):
            self = self._prev

minSup = 2

tree = node("root")  # создаем корень дерева

dataset_sort = ['EDB', 'GDA', 'EGAF', 'EGC', 'GDA', 'DF', 'EBC', 'EGB', 'EDAC', 'ABF'] # отсортированные items

dict_Alp = {'A': 5, 'B': 4, 'C': 3, 'D': 5, 'E': 6, 'F': 3, 'G': 5}

ALPHABET = ['E', 'G', 'D', 'A', 'B', 'F', 'C']


def return_root_dict(tree): # получаем словарь путей от определенного узла до корня
    dict_pr = dict()
    while (tree._prev != None):
        dict_pr[tree._name] = tree._count
        tree = tree._prev
    return dict_pr

def tree_creat(tree, dataset_sort):  # создаем префиксное дерево
    for i in dataset_sort:
        prev_count = len(i)
        for j in i:
            id = tree.node_char(j)
            if (id != -1):
                tree = tree.node_id(id)
                tree.count_add()
            else:
                tree = tree.add(j)
                tree.count_add()
        for k in range(prev_count):
            tree = tree.prev()
    return tree

tree = tree_creat(tree, dataset_sort) # создаем дерево из наших данных

final_list = list()

def lpk(tree, charFind):  # обход дерева в зависимости от символа, получаем пути в виде списка словарей
    if (tree._node != [] or tree._name == charFind):
        if (tree._name == charFind):
            final_list.append(return_root_dict(tree))
        else:
            lenNode = tree.node_len()
            for i in range(lenNode):
                x = tree.node_id(i)
                lpk(x, charFind)

def remake_dict(dictL):  # перезаписываем количество повторений в путях в словарях
    for i in dictL:
        x = list(i.values())[0]
        for j in list(i.keys()):
            i[j] = x
    return dictL

def sum_dict(dict_old): #соединяем список словарей в один словарь
    c = dict()
    for i in dict_old:
        for j, jValue in zip(list(i.keys()), list(i.values())):
            c[j] = 0
    for i in dict_old:
        for j, jValue in zip(list(i.keys()), list(i.values())):
            c[j] += jValue
    return c

def del_dict(dict_old, sup): #удаляем в словаре ключи, которые не подходят под поддержку
    for j, jValue in zip(list(dict_old.keys()), list(dict_old.values())):
        if (jValue < sup):
            del dict_old[j]
    return dict_old

def create_t(tree_char): #создаем условное префиксное дерево
    tree_new = node("root")
    for i in tree_char:
        prev_count = len(i)
        for j, jValue in zip(list(reversed(list(i.keys()))), list(reversed(list(i.values())))):
            id = tree_new.node_char(j)
            if (id != -1):
                tree_new = tree_new.node_id(id)
                tree_new._count += jValue
            else:
                tree_new = tree_new.add(j)
                tree_new._count += jValue
        for k in range(prev_count):
            tree_new = tree_new.prev()
    return tree_new

final = dict()

def rec(tree, char, sup): #рекурсивная функция, куда подаем дерево, символ и поддержку
    lpk(tree, char)
    res = final_list.copy()
    final_list.clear()
    res = remake_dict(res)
    list_find = sum_dict(res)
    list_find = del_dict(list_find.copy(), sup)  # получаем элементы, которые подходят под поддержку
    if (len(list_find) == 2):
        Q = list_find[char]
        E = list(list_find.keys())
        P = list(list_find.values())
        Eword = E[1] + E[0]
        W = dict()
        W[Eword] = P[1]
        W[char] = list_find.get(char)
        return W
    elif (len(list_find) == 1):
        return list_find
    else:
        for i, iValue in zip(list(list_find.keys()), list(list_find.values())):
            if (i == char): # удаляем из списка символ, по которому строили условное дерево
                final[i] = iValue
                for m in res:
                    del m[char]
            else:
                final[i + char] = iValue
                tree_new = create_t(res)
                R = rec(tree_new, i, sup)
                H = list(R.keys())[0]
                final[H + char] = list(R.values())[0]
        return (final)

FINAL = dict()

for i in list(reversed(ALPHABET)):  # мы проверяем букву и отправляем в рекурсинвую функцию,если подходит по минимальной поддержке
    mS = dict_Alp.get(i)
    if (mS >= minSup):
        FINAL.update(rec(tree, i, minSup))

print(len(FINAL.items()))
print(sorted(FINAL.items()))
