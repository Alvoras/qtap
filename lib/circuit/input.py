import curses
from lib.constants import *
import numpy as np

from lib.exceptions import CursorMove

binds = Bindings.values()


def handle_input(circuit, key):
    circuit_grid = circuit.circuit_grid

    # Left Arrow
    if key == curses.KEY_LEFT:
        circuit_grid.move_to_adjacent_node(MOVE_LEFT)
        circuit.render()
        raise CursorMove

    # Right Arrow
    elif key == curses.KEY_RIGHT:
        circuit_grid.move_to_adjacent_node(MOVE_RIGHT)
        circuit.render()
        raise CursorMove

    # Up Arrow
    elif key == curses.KEY_UP:
        circuit_grid.move_to_adjacent_node(MOVE_UP)
        circuit.render()
        raise CursorMove

    # Down Arrow
    elif key == curses.KEY_DOWN:
        circuit_grid.move_to_adjacent_node(MOVE_DOWN)
        circuit.render()
        raise CursorMove

    # Gate Manipulation
    if key == ord(binds[BIND_X_GATE]):
        circuit_grid.handle_input_x()
        circuit.render()

    elif key == ord(binds[BIND_Y_GATE]):
        circuit_grid.handle_input_y()
        circuit.render()

    elif key == ord(binds[BIND_Z_GATE]):
        circuit_grid.handle_input_z()
        circuit.render()

    elif key == ord(binds[BIND_H_GATE]):
        circuit_grid.handle_input_h()
        circuit.render()

    elif key == ord(binds[BIND_S_GATE]):
        circuit_grid.handle_input_s()
        circuit.render()

    elif key == ord(binds[BIND_SDG_GATE]):
        circuit_grid.handle_input_sdg()
        circuit.render()

    elif key == ord(binds[BIND_T_GATE]):
        circuit_grid.handle_input_t()
        circuit.render()

    elif key == ord(binds[BIND_TDG_GATE]):
        circuit_grid.handle_input_tdg()
        circuit.render()

    # Space
    elif key == 32:
        circuit_grid.handle_input_delete()
        circuit.render()

    # Rotation
    elif key == ord(binds[BIND_ROTATE_RIGHT]):
        circuit_grid.handle_input_rotate(np.pi / ROTATION_INC)
        circuit.render()

    elif key == ord(binds[BIND_ROTATE_LEFT]):
        circuit_grid.handle_input_rotate(-np.pi / ROTATION_INC)
        circuit.render()

    # Control
    elif key == ord(binds[BIND_CONTROL_GATE]):
        # Add or remove a control
        circuit_grid.handle_input_ctrl()
        circuit.render()

    elif key == ord(binds[BIND_MOVE_CONTROL_DOWN]):
        # Move a control qubit up
        circuit_grid.handle_input_move_ctrl(MOVE_DOWN)
        circuit.render()

    elif key == ord(binds[BIND_MOVE_CONTROL_UP]):
        # Move a control qubit up
        circuit_grid.handle_input_move_ctrl(MOVE_UP)

    # Circuit management
    elif key == ord(binds[BIND_CLEAN_CIRCUIT]):
        # Move a control qubit up
        circuit_grid.handle_input_r()

    circuit.render()
