class ObjectStorage:
    def __init__(self, relative_path):
        self.relative_path = relative_path

    def get(self, obj_type, key):
        with open(f'{self.relative_path}/{obj_type}', key) as f:
            data = []
            for elem in f:
                data.append(elem.strip())
            return data

    def set(self, obj_type, key, value):
        with open(f'{self.relative_path}/{obj_type}', key) as f:
            print(value, file=f)
