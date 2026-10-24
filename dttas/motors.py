'''
    ДЗТПР (ДЗ №1)
    Задача о моторах
'''
def solve():
    # Проверяем входные данные на корректность
    try:
        # Считываем и парсим входные данные
        line = input().split(';')
        n = int(line[0])
        a, c, c0 = map(lambda x: list(map(int, x.split())), line[1:4])
    except:
        return 'Error: Incorrect read input data'
    else:
        # Проверяем входные массивы на совпадение размерностей с n
        if len(a) != n or len(c) != n or len(c0) != n:
            return 'Error: Incorrect vector size'

        # Наконец, приступаем к алгоритму решения
        # Типы моторов нумеруем с нуля

        # pref[y] = a[0] + a[1] + ... + a[y-1] = необходимое число моторов типов [0;y)
        pref = [0 for _ in range(n + 1)]
        for i in range(n):
            pref[i + 1] = pref[i] + a[i]

        # n_motors(x, y) = a[x] + ... + a[y-1] = необходимое число моторов типов [x;y)
        def n_motors(x: int, y: int) -> int:
            return pref[y] - pref[x]

        # Затраты на покрытие отрезка [x;y) моторами типа x, причем x < y
        def cost(x: int, y: int) -> int:
            if n_motors(x, y) == 0: # Важно для случая a[x] == 0 (м.б. дополнительно a[x+1]==0 и т.д.)
                return 0
            return c0[x] + c[x] * n_motors(x, y)

        # Минимальная стоимость покрытия моторов типов [y; n)
        s = [cost(y, n) for y in range(n)]
        for y in range(n - 2, -1, -1):
            for k in range(1, n - y):
                s[y] = min(s[y], cost(y, y + k) + s[y + k])

        return s[0]


if __name__ == '__main__':
    print(solve())
