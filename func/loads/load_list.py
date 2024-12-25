

def load_list(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]