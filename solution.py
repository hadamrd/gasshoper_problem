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


def inter(A, B):
    inter = []
    for leap in cumsum(leaps):
        if leap in points:
            inter.append(leap)
    return inter


def intersect(offset, leaps, point):
    s = offset
    for i, l in enumerate(leaps):
        if s + l == point:
            return i
        s = s + l
    return None


def cumsum(l, offset=0):
    if not l:
        return []
    else:
        offset += l[0]
        return [offset] + cumsum(l[1:], offset)


def pick_leap(offset, max_leap, leaps, points):
    not_in_points = [l for l in leaps if l + offset not in points]
    return max([l for l in not_in_points if l + max_leap + offset not in points])


def solve(offset, leaps, points):
    if not points:
        return leaps
    else:
        max_leap = max(leaps)
        min_point = min(points)
        next_step = offset + max_leap
        leaps.remove(max_leap)
        if next_step >= min_point:
            surpassed = [p for p in points if p <= next_step]
            reminding_points = [p for p in points if p not in surpassed]
            if next_step not in points:
                return [max_leap] + solve(next_step, leaps, reminding_points)
            elif next_step == min_point:
                leaps = solve(next_step, leaps, reminding_points)
                return [leaps[0], max_leap] + leaps[1:]
            else:
                max_leap2 = pick_leap(offset, max_leap, leaps, points)
                leaps.remove(max_leap2)
                next_step += max_leap2
                return [max_leap2, max_leap] + solve(next_step, leaps, reminding_points)
        else:
            points.remove(min_point)
            leaps = solve(next_step, leaps, points)
            i = intersect(next_step, leaps, min_point)
            return [max_leap] + leaps if i is None else \
                [leaps[i + 1]] + leaps[:i + 1] + [max_leap] + leaps[i + 2:]


def turbo_test():
    for k in range(1, 500):
        for _ in range(10):
            leaps, points = rand_problem(k)
            sol = solve(0, leaps.copy(), points.copy())
            check = verify(sol, points)
            print(check)
            if not check:
                raise Exception("Incorrect solution")


if __name__ == "__main__":
    turbo_test()
