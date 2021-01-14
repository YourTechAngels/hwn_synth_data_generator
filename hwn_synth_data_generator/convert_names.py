source_dir = 'source/'

def names_to_lower(target_file, source_file=source_dir + 'draft.txt'):
    def to_lower(name):
        return name[0].upper() + name[1:].lower()

    with open(source_file) as f:
        names = f.read().splitlines()

    names = [to_lower(name) for name in names]

    with open(target_file, 'w') as f:
        f.write('\n'.join(names))

names_to_lower(source_dir + "cleared_data.txt")
