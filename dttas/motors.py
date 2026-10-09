# Считываем входные данные
line = input().split('; ')
n = int(line[0])
a, c, c0 = map(lambda x: list(map(int, x.split())), line[1:4])

# Число моторов на отрезке [x;y) будем считать префиксами
pref = [0 for _ in range(n + 1)]
for i in range(n):
    pref[i + 1] = pref[i] + a[i]
def n_motors(x: int, y: int) -> int:
    if x >= y:
        return 0
    return pref[y] - pref[x]

# Затраты на покрытие отрезка [x;y) моторами x
def f(x: int, y: int) -> int:
    if x >= y:
        return 0
    return c0[x] + c[x] * n_motors(x, y)

# Динамическое программирование
# Нумерация моторов с нуля
# dp[y][x] = минимальное число затрат на покрытие отрезка [x;n) за не более, чем y+1 моторов
dp = [[0 for _ in range(n)] for _ in range(n)]

# База (покрытие не более чем одним отрезком)
for x in range(0, n):
    dp[0][x] = f(x, n)

# Шаг (выбираем длину нового, если нужно, покрывающего отрезка)
for y in range(1, n):
    for x in range(n):
        # j - x - это длина нового отрезка. При j = x новый отрезок не требуется
        dp[y][x] = min([dp[y-1][j] + f(x, j) for j in range(x, n)])

# Ответ - минимальное число затрат на отрезке [0; n) за не более, чем n моторов (т.е. все возможные комбинации)
print(dp[n-1][0])
