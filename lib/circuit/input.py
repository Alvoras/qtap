from lib.constants import MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT


def handle_input(circuit, key):
    circuit_grid = circuit.circuit_grid

    # Left Arrow
    if key == 75:
        circuit_grid.move_to_adjacent_node(MOVE_LEFT)
        circuit.render()
    # Right Arrow
    elif key == 77:
        circuit_grid.move_to_adjacent_node(MOVE_RIGHT)
        circuit.render()
    # Up Arrow
    elif key == 72:
        circuit_grid.move_to_adjacent_node(MOVE_UP)
        circuit.render()
    # Down Arrow
    elif key == 80:
        circuit_grid.move_to_adjacent_node(MOVE_DOWN)
        circuit.render()

    # Gate Manipulation
    if key == ord("x"):
        circuit_grid.handle_input_x()
        circuit.render()
        
    elif key == ord("y"):
        circuit_grid.handle_input_y()
        circuit.render()
        
    elif key == ord("w"):
        circuit_grid.handle_input_z()
        circuit.render()
        
    elif key == ord("h"):
        circuit_grid.handle_input_h()
        circuit.render()
        
    # Space
    elif key == 32:
        circuit_grid.handle_input_delete()
        circuit.render()
        
    elif key == ord("c"):
        # Add or remove a control
        circuit_grid.handle_input_ctrl()
        circuit.render()
        
    elif key == ord("q"):
        # Move a control qubit up
        circuit_grid.handle_input_move_ctrl(MOVE_UP)
        circuit.render()