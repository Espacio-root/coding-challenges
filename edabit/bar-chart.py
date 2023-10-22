def bar_chart(results):
    results = [[r[0], r[1]] for r in results.items()]
    results = sorted(results, key=lambda x: x[1]-int(x[0][1]), reverse=True)
    res = ''
		
    for i, result in enumerate(results):
        space = 1 if result[1] != 0 else 0
        end = '' if i == len(results) - 1 else '\n'
        res += '{}|{}{}{}{}'.format(result[0], (result[1]//50) * "#", space * " ", result[1], end)
    return res

# better
def bar_chart(results):
    ordered = sorted(results.items(), key=lambda x: (-x[1], x[0]))
    chart = '\n'.join('{}|{} {}'.format(k, '#'*(v//50), v) for k, v in ordered).replace('| ', '|')
    return chart

print(bar_chart({'Q4': 0, 'Q3': 100, 'Q2': 0, 'Q1': 600}))
