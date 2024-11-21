from core_engine import CoreEngine
from player import Player
from world import World
from utils import raycast_to_grid
from OpenGL.GL import *
from OpenGL.GLU import *
import glfw

# Constants
BOUNDING_BOX = [(-10, 10), (0, 10), (-10, 10)]
GRID_SIZE = (1, 1, 1)

# Initialize components
engine = CoreEngine(width=800, height=600, title="Simple Minecraft")
player = Player(bounding_box=BOUNDING_BOX, start_position=(0.0, 2.0, 0.0))
world = World(size=(20, 10, 20))


def key_callback(window, key, scancode, action, mods):
    """Handle keyboard input for adding/removing blocks."""
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_SPACE:
            player.jump()


def update(delta_time):
    """Update game state."""
    keys = {
        "W": glfw.get_key(engine.window, glfw.KEY_W) == glfw.PRESS,
        "A": glfw.get_key(engine.window, glfw.KEY_A) == glfw.PRESS,
        "S": glfw.get_key(engine.window, glfw.KEY_S) == glfw.PRESS,
        "D": glfw.get_key(engine.window, glfw.KEY_D) == glfw.PRESS,
    }

    # Update player position and gravity
    player.update(delta_time, keys)

    # Handle block placement/removal
    if glfw.get_mouse_button(engine.window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS:
        add_block()
    if glfw.get_mouse_button(engine.window, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS:
        remove_block()


def render():
    glLineWidth(2.0)  # Set uniform line thickness

    """Render game world."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Set the background color to light blue
    glClearColor(0.5, 0.7, 1.0, 1.0)

    # Set up the camera
    camera_target = [
        player.position[0] + player.camera_front[0],
        player.position[1] + player.camera_front[1],
        player.position[2] + player.camera_front[2],
    ]
    gluLookAt(
        player.position[0], player.position[1], player.position[2],
        camera_target[0], camera_target[1], camera_target[2],
        player.camera_up[0], player.camera_up[1], player.camera_up[2],
    )

    # Render the floor and boundary
    world.render_floor()
    world.render_boundary()

    # Render solid blocks with wireframes
    world.render_blocks_with_wireframes()

    # Highlight the current block or floor cell
    highlight_block()

    # Draw the camera direction
    draw_camera_direction()


# Track mouse press state
mouse_pressed = False


def add_block():
    """Add a block where the player is pointing."""
    global mouse_pressed

    # Check if the left mouse button is pressed
    if glfw.get_mouse_button(engine.window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS:
        if not mouse_pressed:  # Place a block only once per click
            position = player.get_position()
            direction = player.get_camera_direction()

            for grid_pos in raycast_to_grid(position, direction, max_distance=10.0, grid_size=GRID_SIZE):
                if grid_pos in world.blocks:
                    # Add a block on the highlighted face
                    face_normal = get_face_normal(position, direction, grid_pos)
                    new_block_pos = (
                        grid_pos[0] + face_normal[0],
                        grid_pos[1] + face_normal[1],
                        grid_pos[2] + face_normal[2],
                    )
                    if world.is_within_bounds(*new_block_pos):
                        world.add_block(*new_block_pos)
                    break
                elif grid_pos[1] == 0 and world.is_within_bounds(*grid_pos):
                    # Add a block on the floor cell
                    world.add_block(*grid_pos)
                    break

            mouse_pressed = True  # Set mouse pressed state
    else:
        mouse_pressed = False  # Reset mouse pressed state when released


def remove_block():
    """Remove the block the player is pointing at."""
    position = player.get_position()
    direction = player.get_camera_direction()
    for grid_pos in raycast_to_grid(position, direction, max_distance=10.0, grid_size=GRID_SIZE):
        if grid_pos in world.blocks:
            world.remove_block(*grid_pos)
            break


def highlight_block():
    """Highlight the floor cell or block face the player is pointing at."""
    position = player.get_position()
    direction = player.get_camera_direction()

    for grid_pos in raycast_to_grid(position, direction, max_distance=10.0, grid_size=GRID_SIZE):
        if grid_pos in world.blocks:
            # Highlight the face
            face_normal = get_face_normal(position, direction, grid_pos)
            world.render_face_highlight(grid_pos, face_normal)
            break
        elif grid_pos[1] == 0:
            # Highlight the floor cell
            world.render_full_wireframe(grid_pos, color=(0.0, 1.0, 0.0))  # Green for floor highlight
            break


def get_face_normal(player_position, direction, block_position):
    """
    Determine the face normal of the block the player is looking at.
    Returns a tuple (x, y, z) representing the face normal.
    """
    offset = [
        player_position[0] - block_position[0],
        player_position[1] - block_position[1],
        player_position[2] - block_position[2],
    ]
    axis = max(range(3), key=lambda i: abs(offset[i]))  # Find the dominant axis
    face_normal = [0, 0, 0]
    face_normal[axis] = 1 if direction[axis] > 0 else -1
    return tuple(face_normal)


def draw_camera_direction():
    """Draw the player's camera direction as a red line."""
    position = player.get_position()
    direction = player.get_camera_direction()
    glColor3f(1.0, 0.0, 0.0)  # Red line
    glBegin(GL_LINES)
    glVertex3f(*position)
    glVertex3f(
        position[0] + direction[0] * 5,
        position[1] + direction[1] * 5,
        position[2] + direction[2] * 5,
    )
    glEnd()


def mouse_callback(window, xpos, ypos):
    """Handle mouse movement to control camera direction."""
    global last_mouse_pos

    # Debug the raw mouse position
    # print(f"Mouse position: ({xpos}, {ypos})")

    # Initialize last_mouse_pos on the first call
    if 'last_mouse_pos' not in globals() or last_mouse_pos is None:
        last_mouse_pos = (xpos, ypos)
        return  # Skip updating on the first call

    # Calculate mouse movement deltas
    dx = xpos - last_mouse_pos[0]
    dy = last_mouse_pos[1] - ypos  # Invert Y-axis

    # Debug the deltas
    # print(f"Mouse deltas: dx={dx}, dy={dy}")

    # Update last mouse position
    last_mouse_pos = (xpos, ypos)

    # Pass the deltas to the player
    player.handle_mouse(dx, dy)


if __name__ == "__main__":
    engine.initialize()

    # Set callbacks after the window is initialized
    glfw.set_key_callback(engine.window, key_callback)
    glfw.set_cursor_pos_callback(engine.window, mouse_callback)

    engine.run(update, render)
