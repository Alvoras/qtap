#!/usr/bin/env python
#
# Copyright 2019 the original author or authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import numpy as np

from lib.circuit import circuit_node_types as node_types
from lib.circuit.circuit_grid_model import CircuitGridNode
from lib.constants import MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT


class CircuitGrid:
    """Enables interaction with circuit"""

    def __init__(self, xpos, ypos, circuit_grid_model):
        self.xpos = xpos
        self.ypos = ypos
        self.circuit_grid_model = circuit_grid_model
        self.selected_wire = 0
        self.selected_column = 0

    def move_to_adjacent_node(self, direction):
        if direction == MOVE_LEFT and self.selected_column > 0:
            self.selected_column -= 1
        elif direction == MOVE_RIGHT and self.selected_column < self.circuit_grid_model.max_columns - 1:
            self.selected_column += 1
        elif direction == MOVE_UP and self.selected_wire > 0:
            self.selected_wire -= 1
        elif direction == MOVE_DOWN and self.selected_wire < self.circuit_grid_model.max_wires - 1:
            self.selected_wire += 1

    def get_selected_node_gate_part(self):
        return self.circuit_grid_model.get_node_gate_part(self.selected_wire, self.selected_column)

    def handle_input_x(self):
        # Add X gate regardless of whether there is an existing gate
        # circuit_grid_node = CircuitGridNode(node_types.X)
        # self.circuit_grid_model.set_node(self.selected_wire, self.selected_column, circuit_grid_node)

        # Allow deleting using the same key only
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part == node_types.EMPTY:
            circuit_grid_node = CircuitGridNode(node_types.X)
            self.circuit_grid_model.set_node(self.selected_wire, self.selected_column, circuit_grid_node)
        elif selected_node_gate_part == node_types.X:
            self.handle_input_delete()
        self.update()

    def handle_input_y(self):
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part == node_types.EMPTY:
            circuit_grid_node = CircuitGridNode(node_types.Y)
            self.circuit_grid_model.set_node(self.selected_wire, self.selected_column, circuit_grid_node)
        elif selected_node_gate_part == node_types.Y:
            self.handle_input_delete()
        self.update()

    def handle_input_z(self):
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part == node_types.EMPTY:
            circuit_grid_node = CircuitGridNode(node_types.Z)
            self.circuit_grid_model.set_node(self.selected_wire, self.selected_column, circuit_grid_node)
        elif selected_node_gate_part == node_types.Z:
            self.handle_input_delete()
        self.update()

    def handle_input_h(self):
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part == node_types.EMPTY:
            circuit_grid_node = CircuitGridNode(node_types.H)
            self.circuit_grid_model.set_node(self.selected_wire, self.selected_column, circuit_grid_node)
        elif selected_node_gate_part == node_types.H:
            self.handle_input_delete()
        self.update()

    def handle_input_delete(self):
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part == node_types.X or \
                selected_node_gate_part == node_types.Y or \
                selected_node_gate_part == node_types.Z or \
                selected_node_gate_part == node_types.H:
            self.delete_controls_for_gate(self.selected_wire, self.selected_column)

        if selected_node_gate_part == node_types.CTRL:
            gate_wire_num = \
                self.circuit_grid_model.get_gate_wire_for_control_node(self.selected_wire,
                                                                       self.selected_column)
            if gate_wire_num >= 0:
                self.delete_controls_for_gate(gate_wire_num,
                                              self.selected_column)
        elif selected_node_gate_part != node_types.SWAP and \
                selected_node_gate_part != node_types.CTRL and \
                selected_node_gate_part != node_types.TRACE:
            circuit_grid_node = CircuitGridNode(node_types.EMPTY)
            self.circuit_grid_model.set_node(self.selected_wire, self.selected_column, circuit_grid_node)

        self.update()

    def handle_input_ctrl(self):
        # TODO: Handle Toffoli gates. For now, control qubit is assumed to be in ctrl_a variable
        #       with ctrl_b variable reserved for Toffoli gates
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part == node_types.X or \
                selected_node_gate_part == node_types.Y or \
                selected_node_gate_part == node_types.Z or \
                selected_node_gate_part == node_types.H:
            circuit_grid_node = self.circuit_grid_model.get_node(self.selected_wire, self.selected_column)
            if circuit_grid_node.ctrl_a >= 0:
                # Gate already has a control qubit so remove it
                orig_ctrl_a = circuit_grid_node.ctrl_a
                circuit_grid_node.ctrl_a = -1
                self.circuit_grid_model.set_node(self.selected_wire, self.selected_column, circuit_grid_node)

                # Remove TRACE nodes
                for wire_num in range(min(self.selected_wire, orig_ctrl_a) + 1,
                                      max(self.selected_wire, orig_ctrl_a)):
                    if self.circuit_grid_model.get_node_gate_part(wire_num,
                                                                  self.selected_column) == node_types.TRACE:
                        self.circuit_grid_model.set_node(wire_num, self.selected_column,
                                                         CircuitGridNode(node_types.EMPTY))
                self.update()
            else:
                # Attempt to place a control qubit beginning with the wire above
                if self.selected_wire >= 0:
                    if self.place_ctrl_qubit(self.selected_wire, self.selected_wire - 1) == -1:
                        if self.selected_wire < self.circuit_grid_model.max_wires:
                            if self.place_ctrl_qubit(self.selected_wire, self.selected_wire + 1) == -1:
                                print("Can't place control qubit")
                                self.display_exceptional_condition()

    def handle_input_move_ctrl(self, direction):
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part == node_types.X or \
                selected_node_gate_part == node_types.Y or \
                selected_node_gate_part == node_types.Z or \
                selected_node_gate_part == node_types.H:
            circuit_grid_node = self.circuit_grid_model.get_node(self.selected_wire, self.selected_column)
            if 0 <= circuit_grid_node.ctrl_a < self.circuit_grid_model.max_wires:
                # Gate already has a control qubit so try to move it
                if direction == MOVE_UP:
                    candidate_wire_num = circuit_grid_node.ctrl_a - 1
                    if candidate_wire_num == self.selected_wire:
                        candidate_wire_num -= 1
                else:
                    candidate_wire_num = circuit_grid_node.ctrl_a + 1
                    if candidate_wire_num == self.selected_wire:
                        candidate_wire_num += 1
                if 0 <= candidate_wire_num < self.circuit_grid_model.max_wires:
                    if self.place_ctrl_qubit(self.selected_wire, candidate_wire_num) == candidate_wire_num:
                        print("control qubit successfully placed on wire ", candidate_wire_num)
                        if direction == MOVE_UP and candidate_wire_num < self.selected_wire:
                            if self.circuit_grid_model.get_node_gate_part(candidate_wire_num + 1,
                                                                          self.selected_column) == node_types.EMPTY:
                                self.circuit_grid_model.set_node(candidate_wire_num + 1, self.selected_column,
                                                                 CircuitGridNode(node_types.TRACE))
                        elif direction == MOVE_DOWN and candidate_wire_num > self.selected_wire:
                            if self.circuit_grid_model.get_node_gate_part(candidate_wire_num - 1,
                                                                          self.selected_column) == node_types.EMPTY:
                                self.circuit_grid_model.set_node(candidate_wire_num - 1, self.selected_column,
                                                                 CircuitGridNode(node_types.TRACE))
                        self.update()
                    else:
                        print("control qubit could not be placed on wire ", candidate_wire_num)

    def handle_input_rotate(self, radians):
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part == node_types.X or \
                selected_node_gate_part == node_types.Y or \
                selected_node_gate_part == node_types.Z:
            circuit_grid_node = self.circuit_grid_model.get_node(self.selected_wire, self.selected_column)
            circuit_grid_node.radians = (circuit_grid_node.radians + radians) % (2 * np.pi)
            self.circuit_grid_model.set_node(self.selected_wire, self.selected_column, circuit_grid_node)

        self.update()

    def place_ctrl_qubit(self, gate_wire_num, candidate_ctrl_wire_num):
        """Attempt to place a control qubit on a wire.
        If successful, return the wire number. If not, return -1
        """
        if candidate_ctrl_wire_num < 0 or candidate_ctrl_wire_num >= self.circuit_grid_model.max_wires:
            return -1
        candidate_wire_gate_part = \
            self.circuit_grid_model.get_node_gate_part(candidate_ctrl_wire_num,
                                                       self.selected_column)
        if candidate_wire_gate_part == node_types.EMPTY or \
                candidate_wire_gate_part == node_types.TRACE:
            circuit_grid_node = self.circuit_grid_model.get_node(gate_wire_num, self.selected_column)
            circuit_grid_node.ctrl_a = candidate_ctrl_wire_num
            self.circuit_grid_model.set_node(gate_wire_num, self.selected_column, circuit_grid_node)
            self.circuit_grid_model.set_node(candidate_ctrl_wire_num, self.selected_column,
                                             CircuitGridNode(node_types.EMPTY))
            self.update()
            return candidate_ctrl_wire_num
        else:
            print("Can't place control qubit on wire: ", candidate_ctrl_wire_num)
            return -1

    def delete_controls_for_gate(self, gate_wire_num, column_num):
        control_a_wire_num = self.circuit_grid_model.get_node(gate_wire_num, column_num).ctrl_a
        control_b_wire_num = self.circuit_grid_model.get_node(gate_wire_num, column_num).ctrl_b

        # Choose the control wire (if any exist) furthest away from the gate wire
        control_a_wire_distance = 0
        control_b_wire_distance = 0
        if control_a_wire_num >= 0:
            control_a_wire_distance = abs(control_a_wire_num - gate_wire_num)
        if control_b_wire_num >= 0:
            control_b_wire_distance = abs(control_b_wire_num - gate_wire_num)

        control_wire_num = -1
        if control_a_wire_distance > control_b_wire_distance:
            control_wire_num = control_a_wire_num
        elif control_a_wire_distance < control_b_wire_distance:
            control_wire_num = control_b_wire_num

        if control_wire_num >= 0:
            # TODO: If this is a controlled gate, remove the connecting TRACE parts between the gate and the control
            # ALSO: Refactor with similar code in this method
            for wire_idx in range(min(gate_wire_num, control_wire_num),
                                  max(gate_wire_num, control_wire_num) + 1):
                print("Replacing wire ", wire_idx, " in column ", column_num)
                circuit_grid_node = CircuitGridNode(node_types.EMPTY)
                self.circuit_grid_model.set_node(wire_idx, column_num, circuit_grid_node)