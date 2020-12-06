from lib.circuit.circuit_grid import CircuitGrid
from lib.circuit.circuit_grid_model import CircuitGridModel
from lib.constants import MAX_COLUMNS, NUM_SHOTS
from lib.circuit.circuit_node_types import GATE_MAPPING
import lib.circuit.circuit_node_types as NODE_TYPES

from math import ceil, degrees
import numpy as np
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
            for _ in range(self.grid_delta):
                lines.append(" " * self.width)

            offset = (wire * self.grid_delta) + line_idx
            lines[offset] = "─" * self.width

            for col in range(MAX_COLUMNS):
                c = self.render_gate(wire, col).center(5)

                left_padding = (col * (self.width // MAX_COLUMNS)) + (self.width // MAX_COLUMNS) // 2
                lines[offset] = lines[offset][:left_padding - 2] + c + lines[offset][left_padding+3:]

        lines.append(" " * self.width)

        lines = self.draw_cursor(lines)

        return lines

    def draw_cursor(self, lines):
        line_idx = ceil(self.grid_delta / 2)
        offset = (self.circuit_grid.selected_wire * self.grid_delta) + line_idx
        left_padding = (self.circuit_grid.selected_column * (self.width // MAX_COLUMNS)) + (self.width // MAX_COLUMNS) // 2

        gate = self.render_gate(self.circuit_grid.selected_wire, self.circuit_grid.selected_column)
        cursor = [
            "╭─ ─╮",
            f"{gate.center(5)}",
            "╰─ ─╯"
        ]
        cursor.reverse()

        for idx, line in enumerate(cursor):
            cursor_line_size = len(cursor[idx]) // 2
            cursor_height_size = len(cursor) // 2
            cursor_offset_y = offset - (idx - cursor_height_size)

            lines[cursor_offset_y] = lines[cursor_offset_y][:left_padding - cursor_line_size] + \
                cursor[idx] + lines[cursor_offset_y][left_padding + cursor_line_size + 1:]

        return lines

    def render_rotated_gate(self, node):
        c = GATE_MAPPING[node.node_type]
        c += " "
        deg = int(degrees(node.radians % (2 * np.pi)))
        if deg < 90:
            c += "◯"
        elif 90 <= deg < 180:
            c += "◔"
        elif 180 <= deg < 270:
            c += "◑"
        elif 270 <= deg < 360:
            c += "◕"

        return c

    def render_gate(self, wire, col):
        c = "#"
        node = self.circuit_grid_model.get_node(wire, col)
        computed_type = self.circuit_grid_model.get_node_gate_part(wire, col)

        if not node:
            return c
        if computed_type == NODE_TYPES.H:
            c = GATE_MAPPING[node.node_type]
        elif computed_type == NODE_TYPES.X:
            if node.ctrl_a >= 0 or node.ctrl_b >= 0:
                # This is a control-X gate or Toffoli gate
                # TODO: Handle Toffoli gates more completely
                if wire > max(node.ctrl_a, node.ctrl_b):
                    c = GATE_MAPPING["NOT_GATE"]
                else:
                    c = GATE_MAPPING["NOT_GATE"]
            elif node.radians != 0:
                c = self.render_rotated_gate(node)
            else:
                c = GATE_MAPPING[NODE_TYPES.X]
        elif computed_type == NODE_TYPES.Y:
            if node.radians != 0:
                c = self.render_rotated_gate(node)
            else:
                c = GATE_MAPPING[node.node_type]
        elif computed_type == NODE_TYPES.Z:
            if node.radians != 0:
                c = self.render_rotated_gate(node)
            else:
                c = GATE_MAPPING[node.node_type]
        elif computed_type == NODE_TYPES.CTRL:
            if wire > \
                    self.circuit_grid_model.get_gate_wire_for_control_node(wire, col):
                c = GATE_MAPPING["CTRL_BOTTOM_WIRE"]
            else:
                c = GATE_MAPPING["CTRL_TOP_WIRE"]
        else:
            try:
                c = GATE_MAPPING[node.node_type]
            except KeyError:
                pass

        return c

    def predict(self):
        # print("Want to predict")
        circuit = self.circuit_grid_model.compute_circuit()

        backend_sv_sim = BasicAer.get_backend('statevector_simulator')
        job_sim = execute(circuit, backend_sv_sim, shots=NUM_SHOTS)
        result_sim = job_sim.result()
        quantum_state = result_sim.get_statevector(circuit, decimals=3)

        return quantum_state

        # for y in range(len(quantum_state)):
        #     print("Value predicted for " + str(y) + " : " + str(quantum_state[y]))

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
        self.circuit_grid_model.reset_circuit()

        return list(counts.keys())[0]
