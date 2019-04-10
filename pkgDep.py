import json
import sys


def trimPrefix(text):
    return "\"" + text + "\""


maxLevel = 3


def walkHelper(pkg, index, level):
    if level >= maxLevel:
        return

    if pkg in index:
        for dep in index[pkg]:
            print(trimPrefix(dep), "->", trimPrefix(pkg))
            walkHelper(dep, index, level+1)


def diagramGen(pkg, index):
    print("@startuml")
    print("digraph foo {")
    walkHelper(pkg, index, 1)
    print("}")
    print("@enduml")


    # example
    # python pkgDep.py github.com/ethereum/go-ethereum/ethdb
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python pkgDep.py pkgName")
        sys.exit(2)

    pkg = sys.argv[1]

    # load index from disk
    with open('pkgri.json', 'r') as f:
        index = json.load(f)
    # TODO: notify user index first if no pkgri.json file or outdated

    # print list
    if pkg in index:
        for dep in index[pkg]:
            print(dep)

    # print package dependencies DAG
    # print plantuml
    # diagramGen(pkg, index)
