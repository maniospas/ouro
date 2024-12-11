def B(n):
    if n < 0:
        return
    from file_a import A

    A(n - 1)
    print("B", n)
