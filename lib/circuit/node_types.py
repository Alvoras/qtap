EMPTY = -1
IDEN = 0
X = 1
Y = 2
Z = 3
S = 4
SDG = 5
T = 6
TDG = 7
H = 8
SWAP = 9
# B = 10
CTRL = 11  # "control" part of multi-qubit gate
TRACE = 12  # In the path between a gate part and a "control" or "swap" part
RX = 13

NOT_GATE = 14
CTRL_TOP_WIRE = 15
CTRL_BOTTOM_WIRE = 16

GATE_MAPPING = {
    H: "H",
    X: "X",
    Y: "Y",
    Z: "Z",
    S: "S",
    SDG: "SDG",
    T: "T",
    TDG: "TDG",
    SWAP: "SWP",
    IDEN: "#",
    NOT_GATE: "🜨",
    CTRL_TOP_WIRE: "⬤",
    CTRL_BOTTOM_WIRE: "⬤",
    TRACE: "│"
}
