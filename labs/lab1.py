import struct

def float_to_bits(x):
    # return the 64-bit representation of a float as a string of 0s and 1s
    packed = struct.pack('>d', x)
    return ''.join(f'{b:08b}' for b in packed)

def parse_float(x):
    # split a float into sign, exponent, mantissa (IEEE 754 double)
    bits = float_to_bits(x)
    sign = int(bits[0], 2)
    exponent = int(bits[1:12], 2)
    mantissa = int(bits[12:], 2)
    return bits, sign, exponent, mantissa

def reconstruct(sign, exponent, mantissa):
    # rebuild the number from IEEE 754 fields
    if exponent == 0:
        # subnormal number
        if mantissa == 0:
            return -0.0 if sign else 0.0
        value = mantissa * 2.0 ** (-1022 - 52)
    elif exponent == 0x7FF:
        # Inf / NaN
        return float('inf') if mantissa == 0 else float('nan')
    else:
        value = (1 + mantissa / 2.0**52) * 2.0 ** (exponent - 1023)
    return -value if sign else value

def print_row(label, n_or_k, x):
    bits, sign, exponent, mantissa = parse_float(x)
    rebuilt = reconstruct(sign, exponent, mantissa)
    print(f"{label}={n_or_k:>4} | x = {x!r:>24} | bits = {bits}")
    print(f"           sign={sign}, exp={exponent} ({exponent-1023:+d}), mant=0x{mantissa:013x}")
    print(f"           reconstructed = {rebuilt!r}  (equal: {rebuilt == x})\n")

print("=" * 100)
print("Sequence 1:  1 + 1/(10^n)")
print("=" * 100)
n = 0
while True:
    x = 1 + 1 / (10 ** n)
    print_row("n", n, x)
    if x == 1.0:
        print(f">>> Stop: at n = {n} the result equals 1.0\n")
        break
    n += 1

print("=" * 100)
print("Sequence 2:  1 + 1/(2^k)")
print("=" * 100)
k = 0
while True:
    x = 1 + 1 / (2 ** k)
    print_row("k", k, x)
    if x == 1.0:
        print(f">>> Stop: at k = {k} the result equals 1.0\n")
        break
    k += 1