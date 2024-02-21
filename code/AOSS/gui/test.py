def outer_function(x):
    def inner_function(y):
        return x + y

    return inner_function

closure_function = outer_function(10)
result = closure_function(5)  # 