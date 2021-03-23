def generate_random_code(n_digits=6):
    digits = [i for i in range(0, 10)]

    random_str = ""
    for i in range(n_digits):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])

    return random_str