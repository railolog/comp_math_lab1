import sys


def print_mes(mes, error=False):
    if sys.stdin == sys.__stdin__:
        print(mes)
    elif error:
        terminate(mes + f'\nФормат текстового файла:\nТОЧНОСТЬ\nРАЗМЕРНОСТЬ_МАТРИЦЫ\nЧИСЛОВЫЕ_КОЭФФИЦИЕНТЫ_ПОСТРОЧНО(кол-во чисел в каждой строке РАЗМЕРНОСТЬ_МАТРИЦЫ + 1')


def terminate(mes):
    print(f'Программа завершается с ошибкой: {mes}')
    exit(1)


def read_int():
    a = input().strip()

    try:
        res = int(a)
        return res
    except ValueError:
        if sys.stdin == sys.__stdin__:
            print('Пожалуйста, введите целое число')
            return read_int()
        else:
            print_mes('На вход было подано не целое число', True)
    except EOFError:
        print_mes('Конец ввода', True)


def read_matrix_size():
    print_mes('Введите размер матрицы (<= 20)')
    n = read_int()

    if 1 <= n <= 20:
        return n

    if sys.stdin == sys.__stdin__:
        print('На вход было подано число не из диапазона [1, 20]')
        return read_matrix_size()

    terminate('На вход было подано число не из диапазона [1, 20]')


def read_n_open_file():
    print('Введите имя фалйа, с которого хотите осуществить ввод данных либо нажмите Enter')
    filename = input()

    if filename.strip() == '':
        return sys.__stdin__

    try:
        return open(filename, 'r')
    except:
        print('Файл не найден либо недостаточно прав доступа')
        return read_n_open_file()


def read_row(n):
    try:
        res = [float(i.replace(',', '.')) for i in input().strip().split()]

        if len(res) != n:
            print_mes(f'Кол-во элементов в строке не соответствует ожидаемому: {len(res)} вместо {n}', True)
            print('Повторите ввод строки')
            return read_row(n)

        return res
    except ValueError:
        print_mes('На вход было подано не число', True)
        print('Повторите ввод строки')
        return read_row(n)
    except EOFError:
        print_mes('Конец ввода', True)


def read_matrix(n):
    print_mes('Введите построчно коэффициенты матрицы (включая свободные члены)')

    res1, res2 = [], []
    for i in range(n):
        res = read_row(n + 1)
        res1.append(res[:n])
        res2.append(res[n])

    return res1, res2


def read_precision():
    print_mes('Введите точность (максимальное значение абсолютного отклонения)')

    try:
        res = float(input().strip().replace(',', '.', -1))
        return res
    except ValueError:
        print_mes('Введено не число', True)
        return read_precision()
    except EOFError:
        print_mes('Было введено не число', True)


def make_diagonal(A, d):
    MP = [[] for i in range(len(A))]
    WP = [[len(A) - j - 1 for j in range(len(A))] for i in range(len(A))]

    for i in range(len(A)):
        for j in range(len(A)):
            if abs(A[i][j]) > sum(map(lambda x: abs(x), A[i])) - abs(A[i][j]):
                MP[j].insert(0, i)
            elif abs(A[i][j]) == sum(map(lambda x: abs(x), A[i])) - abs(A[i][j]):
                MP[j].append(i)

    if any(len(i) == 0 for i in MP):
        terminate('Невозможно достижение диагонального преобладания')

    m_is_free = [True for i in range(len(A))]
    w_is_free = [True for i in range(len(A))]

    m_pairs = [None for i in range(len(A))]
    w_pairs = [None for i in range(len(A))]

    while any(i for i in m_is_free):
        free_m_idx = m_is_free.index(True)
        w_idx = MP[free_m_idx][0]

        if w_is_free[w_idx]:
            m_pairs[free_m_idx] = w_idx
            w_pairs[w_idx] = free_m_idx

            m_is_free[free_m_idx] = False
            w_is_free[w_idx] = False
        elif WP[w_idx].index(free_m_idx) < WP[w_idx].index(w_pairs[w_idx]):
            m_is_free[w_pairs[w_idx]] = True
            MP[w_pairs[w_idx]].remove(w_idx)
            m_pairs[w_pairs[w_idx]] = None

            m_pairs[free_m_idx] = w_idx
            w_pairs[w_idx] = free_m_idx

            m_is_free[free_m_idx] = False
            w_is_free[w_idx] = False
        else:
            MP[free_m_idx].remove(w_idx)

    new_A = []
    new_d = []

    for i in range(len(A)):
        new_A.append(A[m_pairs[i]])
        new_d.append(d[m_pairs[i]])

    is_correct = False
    for i in range(len(A)):
        if abs((new_A[i][i])) > sum(map(lambda x: abs(x), new_A[i])) - abs((new_A[i][i])):
            is_correct = True
        elif abs((new_A[i][i])) > sum(map(lambda x: abs(x), new_A[i])) - abs((new_A[i][i])):
            terminate('Невозможно достижение диагонального преобладания')

    if is_correct:
        return new_A, new_d

    terminate('Невозможно достижение диагонального преобладания')


def get_C_n_b(A, b):
    C = [[] for i in range(len(A))]
    d = []

    for i in range(len(A)):
        for j in range(len(A)):
            if i == j:
                C[i].append(0)
            else:
                if A[i][i] == 0:
                    C[i].append(0)
                else:
                    C[i].append( -A[i][j] / A[i][i])

    for i in range(len(A)):
        if A[i][i] == 0:
            d.append(0)
        else:
            d.append(b[i]/A[i][i])

    return C, d


def evaluate(x, C, d):
    new_x = [0 for i in range(len(x))]
    delta = []

    for i in range(len(x)):
        for j in range(len(x)):
            new_x[i] += C[i][j] * x[j]
        new_x[i] += d[i]

        delta.append(abs(new_x[i] - x[i]))

    return new_x, delta


def disrap(x, A, d):
    disraps = []

    for i in range(len(x)):
        di = 0
        for j in range(len(x)):
            #print(x[j], A[i][j])
            di += x[j] * A[i][j]
        #print('di: ', di)
        #print(d)
        disraps.append(abs(di - d[i]))

    return disraps


def check_norma(C):
    norma = -1
    for i in range(len(C)):
        ni = 0

        for j in range(len(C)):
            ni += abs(C[i][j])
        norma = max(norma, ni)

    #print(norma)
    if norma > 1:
        terminate('Требование к норме матрицы не достигнуто')

    print(f'\nНорма матрицы по строкам: {norma} < 1\n')


def solve(C, d, e, A, old_d):
    #heck_norma(C)

    print('Начало поиска ответа...')

    print_mes('Введите вектор начального приближения')
    x_k = read_row(len(C))
    it = 0

    print('Итерация 0: x = [', *x_k, ']', '\n')
    delta = float('inf')
    disraps = disrap(x_k, A, old_d)

    while delta >= e and it < 10 ** 9:
        x_k, deltas = evaluate(x_k, C, d)
        disraps = disrap(x_k, A, old_d)
        it += 1
        print(f'Итерация {it}: x = [', *x_k, ']')
        print('Вектор погрешностей: [', *deltas, ']')
        print('Вектор невязок: [', *disraps, ']', '\n')
        delta = max(disraps)

    print(f'Выполнено итераций: {it}')
    print('Итоговый вектор неизвестных: [', *x_k, ']')
    print('Итоговый вектор погрешнойстей: [', *deltas, ']')
    print('Итоговый вектор невязок: [', *disraps, ']')


def run():
    print('Данная программа решает СЛАУ с помощью метода простых итераций')

    sys.stdin = read_n_open_file()
    e = read_precision()
    n = read_matrix_size()
    A, d = read_matrix(n)
    #A, d = make_diagonal(A, d)

    print('Матрица с диагональным преобладанием, полученная из исходной:')

    for i in range(len(A)):
        print('|', *A[i], '|', d[i], '|', sep='  ')

    C, new_d = get_C_n_b(A, d)

    solve(C, new_d, e, A, d)


if __name__ == '__main__':
    run()
