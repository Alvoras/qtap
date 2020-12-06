import curses
from lib.constants import MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT
import numpy as np


def handle_input(circuit, key):
    circuit_grid = circuit.circuit_grid

    # Left Arrow
    if key == curses.KEY_LEFT:
        circuit_grid.move_to_adjacent_node(MOVE_LEFT)
        circuit.render()
    # Right Arrow
    elif key == curses.KEY_RIGHT:
        circuit_grid.move_to_adjacent_node(MOVE_RIGHT)
        circuit.render()
    # Up Arrow
    elif key == curses.KEY_UP:
        circuit_grid.move_to_adjacent_node(MOVE_UP)
        circuit.render()
    # Down Arrow
    elif key == curses.KEY_DOWN:
        circuit_grid.move_to_adjacent_node(MOVE_DOWN)
        circuit.render()

    # Gate Manipulation
    if key == ord("x"):
        circuit_grid.handle_input_x()
        circuit.render()

    elif key == ord("y"):
        circuit_grid.handle_input_y()
        circuit.render()

    elif key == ord("z"):
        circuit_grid.handle_input_z()
        circuit.render()

    elif key == ord("h"):
        circuit_grid.handle_input_h()
        circuit.render()

    elif key == ord("s"):
        circuit_grid.handle_input_s()
        circuit.render()

    elif key == ord("S"):
        circuit_grid.handle_input_sdg()
        circuit.render()

    elif key == ord("t"):
        circuit_grid.handle_input_t()
        circuit.render()

    elif key == ord("T"):
        circuit_grid.handle_input_tdg()
        circuit.render()

    # Space
    elif key == 32:
        circuit_grid.handle_input_delete()
        circuit.render()

    elif key == ord("e"):
        circuit_grid.handle_input_rotate(np.pi / 2)  # +45°
        circuit.render()

    elif key == ord("a"):
        circuit_grid.handle_input_rotate(-np.pi / 2)  # -45°
        circuit.render()

    elif key == ord("c"):
        # Add or remove a control
        circuit_grid.handle_input_ctrl()
        circuit.render()

    elif key == ord("w"):
        # Move a control qubit up
        circuit_grid.handle_input_move_ctrl(MOVE_DOWN)
        circuit.render()

    elif key == ord("W"):
        # Move a control qubit up
        circuit_grid.handle_input_move_ctrl(MOVE_UP)

    circuit.render()
