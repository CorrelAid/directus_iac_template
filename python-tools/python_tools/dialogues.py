def select_instance(apply_on):
    valid_answers = ["prod", "dev"]
    msg = f"Do you want to {apply_on} the  prod or dev server? (prod/dev) "
    answer = input(msg)

    while answer not in valid_answers:
        print("Invalid input. Please enter 'prod' or 'dev'.")
        answer = input(msg)

    instance = 1 if answer == "prod" else 0

    return instance