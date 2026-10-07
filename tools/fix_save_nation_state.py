"""Moves nation_state_advance in a debug (text) EU5 save from the Age of Revolutions advance tree to the Age of
Reformation tree, under fine_cloth_workshop_advance, as LudiMPbalance's file change would on a new game.
The node's own children stay where they were, under its old parent."""
import re
import sys

SRC, DST = sys.argv[1], sys.argv[2]
MOVE, NEW_PARENT = "3190", "2065"

data = open(SRC, "rb").read()
start = data.index(b"\tage_1_traditions={", data.index(b"\nadvance_manager={"))
end = data.index(b"\nevent_manager={", start)
section = data[start:end].decode("utf-8")

tokens = re.findall(r"\{|\}|[A-Za-z0-9_]+=|[A-Za-z0-9_]+", section)
pos = 0


def node():
    """{ ref=N children={ node node ... } } -> [ref, [children]]"""
    global pos
    assert tokens[pos] == "{"; pos += 1
    assert tokens[pos] == "ref="; ref = tokens[pos + 1]; pos += 2
    kids = []
    if tokens[pos] == "children=":
        pos += 1
        assert tokens[pos] == "{"; pos += 1
        while tokens[pos] == "{":
            kids.append(node())
        assert tokens[pos] == "}"; pos += 1
    assert tokens[pos] == "}"; pos += 1
    return [ref, kids]


ages = []
while pos < len(tokens):
    if tokens[pos] == "}":          # the closing brace of advance_manager
        pos += 1
        continue
    name = tokens[pos]; assert name.endswith("="), (pos, name)
    pos += 1
    tokens.insert(pos, "{") if False else None
    # an age block is { ref=N children={...} }: the same shape as a node
    ages.append((name[:-1], node()))
assert pos == len(tokens)


def find(n, ref, parent=None):
    if n[0] == ref:
        return n, parent
    for k in n[1]:
        r = find(k, ref, n)
        if r:
            return r
    return None


moved = None
for name, root in ages:
    r = find(root, MOVE)
    if r:
        node_, parent = r
        i = parent[1].index(node_)
        parent[1][i:i + 1] = node_[1]          # its children take its place
        moved = [MOVE, []]
        print("removed", MOVE, "from", name, "parent", parent[0], "children kept:", [k[0] for k in node_[1]])
        break
assert moved
for name, root in ages:
    r = find(root, NEW_PARENT)
    if r:
        r[0][1].append(moved)
        print("added", MOVE, "to", name, "under", NEW_PARENT)
        break


def ser(n, ind):
    t = "\t" * ind
    s = f"{t}{{\n{t}\tref={n[0]}\n"
    if n[1]:
        s += f"{t}\tchildren={{\n" + "".join(ser(k, ind + 2) for k in n[1]) + f"{t}\t}}\n"
    return s + f"{t}}}\n"


out = ""
for name, root in ages:
    body = ser(root, 1)
    out += f"\t{name}=" + body.lstrip("\t")
out += "}"
open(DST, "wb").write(data[:start] + out.encode("utf-8") + data[end:])
print("written", DST)
