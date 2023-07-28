import sys

import modal

stub = modal.Stub("example-hello-world")

@stub.function()
def f(i):
    if i % 2 == 0:
        print("hello", i)
    else:
        print("world", i, file=sys.stderr)

    return i * i


@stub.local_entrypoint()
def main():
    # Call the function locally.
    print(f(1000))

    # Call the function remotely.
    print(f.call(1000))

    # Parallel map.
    total = 0
    for ret in f.map(range(20)):
        total += ret

    print(total)


