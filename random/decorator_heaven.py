def d1(function):
    def innerd1():
        print(f"In d1: {function.__name__}")

        return function()

    return innerd1


def d2(function):
    def innerd2():
        print(f"In d2: {function.__name__}")

        return function()

    return innerd2


@d1
@d2
def a():
    return "bim bom bam bish bash bosh"


a()
