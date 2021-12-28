class ObjectStorage:
    def __init__(self, relative_path):
        self.relative_path = relative_path

    def get(self, obj_type):
        try:
            directory = 'responded_members' if 'respond' in obj_type else 'storage'
            with open(f'{self.relative_path}/{directory}/{obj_type}.txt', 'r') as f:
                data = []
                for elem in f:
                    data.append(elem.strip())
            return data
        except FileNotFoundError:
            return []

    def set(self, obj_type, value):
        directory = 'responded_members' if 'respond' in obj_type else 'storage'
        with open(f'{self.relative_path}/{directory}/{obj_type}.txt', 'a+') as f:
            print(value, file=f)
