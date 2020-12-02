from lib.circuit.circuit_grid import CircuitGrid
from lib.circuit.circuit_grid_model import CircuitGridModel
from lib.constants import MAX_COLUMNS


class Circuit:
    def __init__(self, qbit_qty):
        self.qbit_qty = qbit_qty
        self.circuit_grid_model = CircuitGridModel(self.qbit_qty, MAX_COLUMNS)
        self.circuit_grid = CircuitGrid(self.qbit_qty, MAX_COLUMNS, self.circuit_grid_model)

    def render(self):
        return ""
