def draw_sierpinski_triangle(n):
    def triangle(height):
        if height == 0:
            return ['*']
        else:
            previous_triangle = triangle(height - 1)
            spaces = ' ' * (2 ** (height - 1))
            upper_triangle = list(map(lambda line: spaces + line + spaces, previous_triangle))
            lower_triangle = list(map(lambda line: line + ' ' + line, previous_triangle))
            return upper_triangle + lower_triangle

    triangle = triangle(n)
    for line in triangle:
        print(line.center(2 ** n - 1))

draw_sierpinski_triangle(4)
