'''
    ДЗТПР (ДЗ №2)
    Задача о Джоне и Бобе: https://stepik.org/lesson/1474692/step/1?unit=1494396
'''
def solve():
    # Проверяем входные данные на корректность
    try: # Считываем и обрабатываем входные данные
        line = input().split('; ') # T, N, (D), (B), d0, b0, d, b, (t)
        T, N, d0, b0, d, b = map(int, (line[e] for e in (0, 1, 4, 5, 6, 7)))
        D, B, t = map(lambda x: list(map(int, x.split())), (line[e] for e in (2, 3, 8)))
    except:
        return 'Error: Incorrect read input data'

    # Проверяем входные массивы на совпадение размерностей
    if len(D) != T or len(B) != T or len(t) != N:
        return 'Error: Incorrect vector size'

    # Часы нумеруются с нуля
    # task_hour[x] = число задач, которые нужно выполнить Бобу/Джону в час x
    task_hour = [len(list(filter(lambda x: i <= x / 60 < i + 1, t))) for i in range(T)]

    # pref[y] = task_hour[0] + task_hour[1] + ... + task_hour[y-1]
    pref = [0 for _ in range(T + 1)]
    for i in range(T):
        pref[i + 1] = pref[i] + task_hour[i]

    # n_tasks(x, y) = a[x] + ... + a[y-1] = число задач для выполнения в часы [x;y)
    def n_tasks(x: int, y: int) -> int:
        return pref[y] - pref[x]

    # Затраты на вызов нового сотрудника(Боба - если workBob==True, иначе - Джона) на время [x;y), причем x < y
    def cost(x: int, y: int, workBob=False) -> int:
        # if n_tasks(x, y) == 0:  # Важно для случая task_hour[x] == 0, но по условию такого не будет
        #     return 0
        k = n_tasks(x, y)
        if workBob:
            return B[x] + b0 * k + b * k * (k + 1) // 2
        return D[x] + d0 * k + d * k * (k + 1) // 2

    # sJohn[y] - мин. затраты на [y, T), если в час y работает Джон | sBob аналогично для Боба
    sJohn = [float('inf') for _ in range(T + 1)]
    sBob = [float('inf') for _ in range(T + 1)]

    # База
    sBob[T], sJohn[T] = 0, 0

    # Шаг
    for y in range(T - 1, -1, -1):
        # Вариант 1: одна смена тянется до самого конца T
        sJohn[y] = min(sJohn[y], cost(y, T, False))
        sBob[y] = min(sBob[y], cost(y, T, True))

        # Вариант 2: смена заканчивается на y+k
        for k in range(1, T - y):
            # Если сейчас работает Джон (False), то на y+k выходит Боб
            sJohn[y] = min(sJohn[y], cost(y, y + k, False) + sBob[y + k])
            # Если сейчас работает Боб (True), то на y+k выходит Джон
            sBob[y] = min(sBob[y], cost(y, y + k, True) + sJohn[y + k])

    # В начале (час 0) на дежурство может выйти как Джон, так и Боб
    return min(sJohn[0], sBob[0])


if __name__ == '__main__':
    print(solve())
