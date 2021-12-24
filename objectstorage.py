class ObjectStorage:
    def __init__(self, relative_path):
        self.relative_path = relative_path

    def get(self, obj_type):
        if 'respond' in obj_type:
            with open(f'{self.relative_path}/responded_members/{obj_type}.txt', 'r') as f:
                data = []
                for elem in f:
                    data.append(elem.strip())
                return data
        else:
            with open(f'{self.relative_path}/storage/{obj_type}.txt', 'r') as f:
                data = []
                for elem in f:
                    data.append(elem.strip())
                return data

    def set(self, obj_type, value):
        if 'respond' in obj_type:
            with open(f'{self.relative_path}/responded_members/{obj_type}.txt', 'a+') as f:
                print(value, file=f)
        else:
            with open(f'{self.relative_path}/storage/{obj_type}.txt', 'a+') as f:
                print(value, file=f)
