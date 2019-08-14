import random as rd


def rand_distinct(n, max):
    res = []
    for i in range(n):
        e = rd.randint(1, max)
        while e in res:
            e = rd.randint(1, max)
        res.append(e)
    return res


def rand_problem(n):
    leaps = list(range(1, n + 1))
    max = n * (n + 1) / 2
    points = rand_distinct(n - 1, max - 1)
    return leaps, points


def verify(leaps, points):
    current_leap = 0
    for i, leap in enumerate(leaps):
        current_leap += leap
        if current_leap in points:
            print('intersect in', current_leap)
            return False
    return True


def intersect(origin, leaps, point):
    for i, l in enumerate(leaps):
        if origin + l == point:
            return i
        origin = origin + l
    return -1


def pick_leap(origin, max_leap, leaps, points):
    not_in_points = [l for l in leaps if l + origin not in points]
    return max([l for l in not_in_points if l + max_leap + origin not in points])


def swap(l, i, j):
    if i != j:
        temp = l[i]
        l[i] = l[j]
        l[j] = temp


def solve(origin, leaps, points):
    if not points:
        return leaps
    else:
        max_leap = max(leaps)
        min_point = min(points)
        next_step = origin + max_leap
        leaps.remove(max_leap)
        remaining_points = [p for p in points if p > max(next_step, min_point)]
        if next_step > min_point and next_step in points:
            max_leap2 = pick_leap(origin, max_leap, leaps, points)
            leaps.remove(max_leap2)
            next_step += max_leap2
            return [max_leap2, max_leap] + solve(next_step, leaps, remaining_points)
        else:
            sol = [max_leap] + solve(next_step, leaps, remaining_points)
            i = intersect(origin, sol, min_point)
            swap(sol, 0, i + 1)
            return sol


def turbo_test():
    for k in range(1, 500):
        for _ in range(10):
            leaps, points = rand_problem(k)
            sol = solve(0, leaps, points)
            check = verify(sol, points)
            if not check:
                raise Exception("Incorrect solution")


if __name__ == "__main__":
    turbo_test()
