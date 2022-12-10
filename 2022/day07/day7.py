class Dir:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = {}
        self.files = {}
        self.size = None

    def __repr__(self):
        return "{} (dir)".format(self.name)

    def get_size(self):
        if not self.size:
            self.size = 0
            for f in self.files.values():
                self.size += f.size
            for c in self.children.values():
                self.size += c.get_size()
        return self.size


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __repr__(self):
        return "{} (file, size={})".format(self.name, self.size)


def run_command(cmd, pwd):
    if cmd[0].startswith("cd"):
        pwd = run_cd(cmd[0], pwd)
    elif cmd[0] == "ls":
        run_ls(cmd[1:], pwd)
    else:
        raise Exception("Invalid input")
    return pwd


def run_cd(cmd, pwd):
    dest = cmd.removeprefix("cd ")
    if dest == "/":
        return root
    if dest == "..":
        return pwd.parent
    pwd.children[dest] = pwd.children.get(dest, Dir(dest, parent=pwd))
    return pwd.children[dest]


def run_ls(result, pwd):
    for inode in result:
        item = inode.split(" ")
        name = item[1]
        if item[0] == "dir":
            pwd.children[name] = pwd.children.get(name, Dir(name, parent=pwd))
        else:
            size = int(item[0])
            pwd.files[name] = pwd.files.get(name, File(name, size))


def dfs(pwd, all_sizes = []):
    all_sizes.append(pwd.get_size())
    for c in pwd.children.values():
        dfs(c, all_sizes)


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        cmds = f.read().strip().split("$ ")[1:]
        cmds = [c.strip().split("\n") for c in cmds]

    root = Dir("/")
    pwd = root
    for cmd in cmds:
        pwd = run_command(cmd, pwd=pwd)
    
    sizes = []
    dfs(root, sizes)
    print("Part 1:", sum([s for s in sizes if s <= 100000]))
    
    total = root.get_size()
    missing = total - 40000000 # How much the total exceeds
    print("Part 2:", min([s for s in sizes if s >= missing]))

