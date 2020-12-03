from lib.circuit.circuit_grid import CircuitGrid
from lib.circuit.circuit_grid_model import CircuitGridModel
from lib.constants import MAX_COLUMNS, NUM_SHOTS

from qiskit import BasicAer, execute, ClassicalRegister

from copy import deepcopy


class Circuit:
    def __init__(self, qbit_qty):
        self.qbit_qty = qbit_qty
        self.circuit_grid_model = CircuitGridModel(self.qbit_qty, MAX_COLUMNS)
        self.circuit_grid = CircuitGrid(self.qbit_qty, MAX_COLUMNS, self.circuit_grid_model)

    def render(self):
        return ""

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

        print(counts)

        return int(list(counts.keys())[0], 2)
