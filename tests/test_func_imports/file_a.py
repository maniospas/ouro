from file_b import B


def A(n):
    B(n - 1)
    print("A", n)


if __name__ == "__main__":
    A(2)
