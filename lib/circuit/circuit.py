from lib.circuit.circuit_grid import CircuitGrid
from lib.circuit.circuit_grid_model import CircuitGridModel
from lib.constants import MAX_COLUMNS, NUM_SHOTS
import lib.circuit.circuit_node_types as NODE_TYPES

from math import ceil

from qiskit import BasicAer, execute, ClassicalRegister

from copy import deepcopy


class Circuit:
    def __init__(self, qbit_qty, height=20, width=20):
        self.height = height
        self.width = width
        self.qbit_qty = qbit_qty

        self.circuit_grid_model = CircuitGridModel(self.qbit_qty, MAX_COLUMNS)
        self.circuit_grid = CircuitGrid(self.qbit_qty, MAX_COLUMNS, self.circuit_grid_model)

        self.grid_delta = 3
        self.y_padding = (self.height - (self.grid_delta * self.qbit_qty)) // 2

    def render(self):
        lines = []

        for i in range(self.y_padding):
            lines.append(" " * self.width)

        lines += self.make_circuit()
        return lines

    def make_circuit(self):
        line_idx = ceil(self.grid_delta / 2)
        lines = []

        for wire in range(self.qbit_qty):
            # 0 - 2
            for _ in range(self.grid_delta):
                # 0 - 6
                lines.append(" " * self.width)

            offset = (wire * self.grid_delta) + line_idx
        #     2
            lines[offset] = "─" * self.width

            for col in range(MAX_COLUMNS):
                c = self.render_gate(wire, col)
                # if col == self.circuit_grid.selected_column and wire == self.circuit_grid.selected_wire:
                #     c = "x"
                # else:
                #     c = "▆"

                left_padding = (col*((self.width)//MAX_COLUMNS)) + (self.width//MAX_COLUMNS)//2
                lines[offset] = lines[offset][:left_padding - 1] + c + lines[offset][left_padding+2:]

        lines.append(" " * self.width)

        lines = self.draw_cursor(lines)

        return lines

    def draw_cursor(self, lines):
        line_idx = ceil(self.grid_delta / 2)
        offset = (self.circuit_grid.selected_wire * self.grid_delta) + line_idx
        left_padding = (self.circuit_grid.selected_column*((self.width)//MAX_COLUMNS)) + (self.width//MAX_COLUMNS)//2

        gate = self.render_gate(self.circuit_grid.selected_wire, self.circuit_grid.selected_column)
        cursor = [
            "╰─ ─╯",
            f"  {gate}  ",
            "╭─ ─╮"
        ]

        # lines[offset] = lines[offset][:left_padding - 2] + cursor[1] + lines[offset][left_padding+3:]

        for idx, line in enumerate(cursor):
            cursor_line_size = len(cursor[idx]) // 2
            cursor_height_size = len(cursor) // 2
            cursor_offset_y = offset - (idx - cursor_height_size)

            lines[cursor_offset_y] = lines[cursor_offset_y][:left_padding - cursor_line_size] + \
                cursor[idx] + lines[cursor_offset_y][left_padding + cursor_line_size + 1:]
            # offset = y - (idx-1)
            # self.replacer(lines[offset-(idx-1)], line, left_padding - (idx-2))
            # lines[offset] = lines[offset][:y-idx-2] + gate + lines[offset][y+idx-2:]

        return lines

    def replacer(self, s, newstring, index, nofail=False):
        # raise an error if index is outside of the string
        if not nofail and index not in range(len(s)):
            raise ValueError("index outside given string")

        # if not erroring, but the index is still not in the correct range..
        if index < 0:  # add it to the beginning
            return newstring + s
        if index > len(s):  # add it to the end
            return s + newstring

        # insert the new string between "slices" of the original
        return s[:index] + newstring + s[index + 1:]

    def render_gate(self, x, y):
        # need 3 character for rendering gate
        c = " ▆ "
        gate = self.circuit_grid_model.get_node_gate_part(x, y)
        if gate == NODE_TYPES.EMPTY:
            pass
        elif gate == NODE_TYPES.H:
            c = " H "

        return c

    def predict(self):
        print("Want to predict")
        circuit = self.circuit_grid_model.compute_circuit()

        backend_sv_sim = BasicAer.get_backend('statevector_simulator')
        job_sim = execute(circuit, backend_sv_sim, shots=NUM_SHOTS)
        result_sim = job_sim.result()
        quantum_state = result_sim.get_statevector(circuit, decimals=3)

        for y in range(len(quantum_state)):
            print("Value predicted for " + str(y) + " : " + str(quantum_state[y]))

    def measure(self):
        circuit = self.circuit_grid_model.compute_circuit()

        backend_sv_sim = BasicAer.get_backend('qasm_simulator')
        cr = ClassicalRegister(self.qbit_qty)
        measure_circuit = deepcopy(circuit)  # make a copy of circuit
        measure_circuit.add_register(cr)  # add classical registers for measurement readout
        measure_circuit.measure(measure_circuit.qregs[0], measure_circuit.cregs[0])
        job_sim = execute(measure_circuit, backend_sv_sim, shots=NUM_SHOTS)
        result_sim = job_sim.result()
        counts = result_sim.get_counts(circuit)

        # TODO : Clean array

        return list(counts.keys())[0]
