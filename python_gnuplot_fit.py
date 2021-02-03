from subprocess import run, PIPE


def prepare_data(x_data, y_data, y_error):
    result = ""
    for data in zip([str(i) for i in x_data], [str(i) for i in y_data], [str(i) for i in y_error]):
        result += "\t".join(data) + "\n"
    return result[:-1]


def prepare_script(function, varriables):
    return f'''
    set print "-" append;
    set fit quiet;
    set fit errorvariables;
    f(x) = {function};
    fit f(x) '-' u 1:2:3 yerrors via {",".join(varriables)};
    print {",".join(varriables)},{",".join([i+"_err/FIT_STDFIT" for i in varriables])};
    '''


def fit(x_data,  y_data, y_error, function, varriables):
    p = run(['gnuplot', '-e', prepare_script(function, varriables)], stdout=PIPE,
            input=prepare_data(x_data, y_data, y_error), encoding='ascii')

    A = [float(i) for i in p.stdout[:-1].split(" ")]
    errors = A[len(A)//2:]
    values = A[:len(A)//2]
    return list(zip(values, errors))


if __name__ == "__main__":
    print(fit([1, 2, 3, 4], [9, 21, 31, 39],
              [1, 2, 3, 4], "a*x+b", ["a", "b"]))
