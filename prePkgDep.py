import subprocess
import sys
import json
import os

# add your ignore folder list
ignoreList = set(['.git', '.idea', '.vscode', 'build', 'vendor',
                  'node_modules', 'tests', 'test', 'testdata'])
filterStd = True


def walkHelper(d):
    isGoPkg = False

    for tf in os.listdir(d):
        _, ext = os.path.splitext(tf)
        if ext == ".go":
            isGoPkg = True

        f = os.path.join(d, tf)
        if os.path.isdir(f) and tf not in ignoreList:
            walkHelper(f)

    if isGoPkg:
        print("processing go pkg: ", d)
        process(golist(d))


def index(srcDir):
    walkHelper(srcDir)
    with open('pkgri.json', 'w') as outfile:
        json.dump(reverseIndex, outfile, cls=SetEncoder)


class SetEncoder(json.JSONEncoder):
    # to encode set data structure
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


# global data
reverseIndex = {}


def process(data):
    if data is None:
        return

    pkg, pkgDeps = data
    for dep in pkgDeps:
        # TODO: fiter std lib

        if dep in reverseIndex:
            reverseIndex[dep].add(pkg)
        else:
            reverseIndex[dep] = set([pkg])


def golist(dir):
    res = subprocess.run(['go', 'list',
                          '-json'], stdout=subprocess.PIPE, cwd=dir)
    if res.returncode != 0:
        print("go list -json " + dir + " failed, continue")
        return None
    data = json.loads(res.stdout)
    # NOTE: for now, ignore TestImports
    return (data["ImportPath"], data["Imports"] if "Imports" in data else [])


# test
# print(golist("./ethdb/leveldb"))
# print(golist("./swarm/network/simulations/discovery"))
# process(golist("./ethdb/leveldb"))
# print(reverseIndex)

# example srcDir is either relative path or absolute path
# python prePkgDep.py .
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python prePkgDep.py srcDir")
        sys.exit(2)

    srcDir = sys.argv[1]
    index(srcDir)
