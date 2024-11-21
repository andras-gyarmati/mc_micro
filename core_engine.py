import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import time


class CoreEngine:
    def __init__(self, width=800, height=600, title="Simple Minecraft"):
        self.width = width
        self.height = height
        self.title = title
        self.window = None
        self.last_time = time.time()
        self.delta_time = 0

    def initialize(self):
        if not glfw.init():
            raise Exception("GLFW could not be initialized!")
        self.window = glfw.create_window(self.width, self.height, self.title, None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window could not be created!")

        glfw.make_context_current(self.window)
        glEnable(GL_DEPTH_TEST)

        # Set callbacks for input
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        # Setup projection matrix
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, self.width / self.height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def key_callback(self, window, key, scancode, action, mods):
        pass  # Will delegate to the Player module later

    def mouse_callback(self, window, xpos, ypos):
        pass  # Will delegate to the Player module later

    def run(self, update_func, render_func):
        while not glfw.window_should_close(self.window):
            # Calculate delta time
            current_time = time.time()
            self.delta_time = current_time - self.last_time
            self.last_time = current_time

            glfw.poll_events()

            # Update and render
            update_func(self.delta_time)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            render_func()
            glfw.swap_buffers(self.window)

        glfw.terminate()
