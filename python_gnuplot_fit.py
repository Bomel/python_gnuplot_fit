from subprocess import run, PIPE


def prepare_data(x_data, y_data, y_error):
    result = ""
    for data in zip([str(i) for i in x_data], [str(i) for i in y_data], [str(i) for i in y_error]):
        result += "\t".join(data) + "\n"
    return result[:-1]


def prepare_fit_script(function, varriables):
    return f'''
    set print "-" append;
    set fit quiet;
    set fit logfile '/dev/null';
    set fit errorvariables;
    f(x) = {function};
    fit f(x) '-' u 1:2:3 yerrors via {",".join(varriables)};
    print {",".join(varriables)},{",".join([i+"_err/FIT_STDFIT" for i in varriables])};
    '''


def prepare_plot_script(function, varriables, filename, data):
    return f'''
    set terminal pdfcairo  transparent enhanced font "arial,10";
    set output "{filename}";
    {";".join(["=".join(i) for i in zip(varriables, [str(i) for i in data])]) + ";"}
    f(x) = {function};
    set ylabel "V_{{eff}}(r,t)";
    set xlabel "t";
    set key at graph 0.9, graph 0.95 spacing 1.25;
    plot '-' u 1:2:3 w e notitle, f(x) lc 3 notitle;
    '''


def fit(x_data,  y_data, y_error, function, varriables, filename=None):
    script = prepare_fit_script(function, varriables)
    p = run(['gnuplot', '-e', script], stdout=PIPE,
            input=prepare_data(x_data, y_data, y_error), encoding='ascii')

    A = [float(i) for i in p.stdout[:-1].split(" ")]
    errors = A[len(A)//2:]
    values = A[:len(A)//2]

    if filename != None:
        script = prepare_plot_script(function, varriables, filename, values)
        p = run(['gnuplot', '-e', script], stdout=PIPE,
                input=prepare_data(x_data, y_data, y_error), encoding='ascii')

    return list(zip(values, errors))


if __name__ == "__main__":
    print(fit([1, 2, 3, 4], [9, 21, 31, 39],
              [1, 2, 3, 4], "a*x+b", ["a", "b"], filename="test.pdf"))
