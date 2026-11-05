import math
import random

PI = 3.14159265358979323846
TWO_PI = 2.0 * PI
HALF_PI = PI / 2.0

EPS = 1e-16 # threshold for stopping the series


def my_sin(x: float) -> float:

    # 1) reduce x to [-pi, pi] using periodicity 2*pi
    if x > PI or x < -PI:
        k = round(x / TWO_PI) # integer number of periods
        x = x - k * TWO_PI
    # 2) reduce to [-pi/2, pi/2] using sine symmetry
    if x > HALF_PI:
        x = PI - x
    elif x < -HALF_PI:
        x = -PI - x

    # 3) taylor series with a recurrent term
    term = x # t_0 = x
    s = x # sum
    x2 = x * x
    n = 0 # index: (2n+1)!
    while True:
        # t_{n+1} = -t_n * x^2 / ((2n+2)(2n+3))
        denom = (2 * n + 2) * (2 * n + 3) # integer numbers
        term = -term * x2 / denom
        s += term
        if abs(term) < EPS:
            break
        n += 1
    return s


def run_test():
    random.seed(42)
    N = 100
    # 100 points in [-10, 10]
    xs = [random.uniform(-10.0, 10.0) for _ in range(N)]

    max_abs_err = 0.0
    max_rel_err = 0.0
    worst_x = None

    print(f"{'x':>14} | {'my_sin':>18} | {'math.sin':>18} | {'abs_err':>12}")
    print("-" * 72)
    for x in xs:
        a = my_sin(x)
        b = math.sin(x)
        abs_err = abs(a - b)
        rel_err = abs_err / abs(b) if abs(b) > 1e-12 else abs_err
        if abs_err > max_abs_err:
            max_abs_err = abs_err
            worst_x = x
        max_rel_err = max(max_rel_err, rel_err)
        if xs.index(x) < 10:
            print(f"{x:14.8f} | {a:18.15f} | {b:18.15f} | {abs_err:12.3e}")

    print("-" * 72)
    print(f"Max absolute error : {max_abs_err:.3e}  (at x = {worst_x:.6f})")
    print(f"Max relative error : {max_rel_err:.3e}")
    print(f"Double machine epsilon : {2.220446049250313e-16:.3e}")


if __name__ == "__main__":
    run_test()