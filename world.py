from OpenGL.GL import *
import math


class World:
    def __init__(self, size=(10, 10, 10)):
        self.size = size  # World grid size (x, y, z)
        self.blocks = {}  # Dictionary to store active blocks {(x, y, z): True/False}

    def add_block(self, x, y, z):
        """Add a block at the given grid position."""
        if self.is_within_bounds(x, y, z):
            self.blocks[(x, y, z)] = True

    def remove_block(self, x, y, z):
        """Remove a block at the given grid position."""
        if (x, y, z) in self.blocks:
            del self.blocks[(x, y, z)]

    def is_within_bounds(self, x, y, z):
        """Check if a block position is within the world bounds."""
        return (
            -self.size[0] // 2 <= x < self.size[0] // 2 and  # X bounds
            0 <= y < self.size[1] and                       # Y bounds
            -self.size[2] // 2 <= z < self.size[2] // 2     # Z bounds
        )

    def raycast(self, origin, direction, max_distance=10.0):
        """
        Perform a raycast from the origin in the given direction.
        Returns the first block hit and the position of the face where the ray intersects.
        """
        position = list(origin)
        step = [direction[i] * 0.1 for i in range(3)]  # Small steps for ray traversal

        for _ in range(int(max_distance / 0.1)):
            grid_pos = tuple(map(math.floor, position))
            if grid_pos in self.blocks:
                return grid_pos
            for i in range(3):
                position[i] += step[i]

        return None

    def render(self):
        """Render all blocks in the world."""
        for (x, y, z) in self.blocks.keys():
            self.render_block(x, y, z)

    def render_block(self, x, y, z):
        """Render a single block."""
        glPushMatrix()
        glTranslatef(x + 0.5, y + 0.5, z + 0.5)  # Center the block in the grid cell
        glColor3f(0.5, 0.5, 0.5)  # Gray block color
        self.draw_cube()
        glPopMatrix()

    def draw_cube(self):
        """Draw a unit cube."""
        glBegin(GL_QUADS)
        # Front face
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        # Back face
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        # Top face
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        # Bottom face
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        # Left face
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        # Right face
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glEnd()

    def render_highlight(self, position):
        """Render a wireframe around the block being pointed at."""
        if position:
            x, y, z = position
            glPushMatrix()
            glTranslatef(x + 0.5, y + 0.5, z + 0.5)  # Center the highlight
            glColor3f(0.0, 1.0, 0.0)  # Green wireframe
            glLineWidth(2.0)
            glBegin(GL_LINE_LOOP)
            # Draw wireframe
            for dx, dy, dz in [
                (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5),  # Back
                (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5),  # Front
            ]:
                glVertex3f(dx, dy, dz)
            glEnd()
            glPopMatrix()

    def render_floor(self):
        """Render the subdivided floor."""
        glColor3f(0.8, 0.8, 0.8)  # Light gray for the floor
        for x in range(-self.size[0] // 2, self.size[0] // 2):
            for z in range(-self.size[2] // 2, self.size[2] // 2):
                glBegin(GL_QUADS)
                glVertex3f(x, 0, z)
                glVertex3f(x + 1, 0, z)
                glVertex3f(x + 1, 0, z + 1)
                glVertex3f(x, 0, z + 1)
                glEnd()
                # Draw black grid lines
                glColor3f(0.0, 0.0, 0.0)
                glBegin(GL_LINE_LOOP)
                glVertex3f(x, 0, z)
                glVertex3f(x + 1, 0, z)
                glVertex3f(x + 1, 0, z + 1)
                glVertex3f(x, 0, z + 1)
                glEnd()
                glColor3f(0.8, 0.8, 0.8)  # Reset floor color

    def render_boundary(self):
        """Render a wireframe cube to represent the world boundary."""
        glColor3f(0.5, 0.5, 0.5)  # Gray for boundary wireframe
        glLineWidth(2.0)
        glBegin(GL_LINES)
        for x in (-self.size[0] // 2, self.size[0] // 2):
            for y in (0, self.size[1]):
                for z in (-self.size[2] // 2, self.size[2] // 2):
                    # Draw lines for all edges of the cube
                    glVertex3f(x, y, z)
                    glVertex3f(x, y, z + (self.size[2] if z == -self.size[2] // 2 else -self.size[2]))
                    glVertex3f(x, y, z)
                    glVertex3f(x + (self.size[0] if x == -self.size[0] // 2 else -self.size[0]), y, z)
                    glVertex3f(x, y, z)
                    glVertex3f(x, y + (self.size[1] if y == 0 else -self.size[1]), z)
        glEnd()

    def render_face_highlight(self, position, normal):
        """Highlight the face of a block with a wireframe."""
        if position:
            glPushMatrix()
            glTranslatef(position[0] + 0.5, position[1] + 0.5, position[2] + 0.5)
            glColor3f(1.0, 1.0, 0.0)  # Yellow for face highlight
            glLineWidth(2.0)

            # Determine the face to highlight based on the normal
            if normal == (0, 1, 0):  # Top face
                corners = [(-0.5, 0.5, -0.5), (0.5, 0.5, -0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5)]
            elif normal == (0, -1, 0):  # Bottom face
                corners = [(-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, -0.5, 0.5), (-0.5, -0.5, 0.5)]
            elif normal == (1, 0, 0):  # Right face
                corners = [(0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (0.5, 0.5, 0.5), (0.5, -0.5, 0.5)]
            elif normal == (-1, 0, 0):  # Left face
                corners = [(-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, 0.5, 0.5), (-0.5, -0.5, 0.5)]
            elif normal == (0, 0, 1):  # Front face
                corners = [(-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5)]
            elif normal == (0, 0, -1):  # Back face
                corners = [(-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5)]

            # Render the wireframe for the face
            glBegin(GL_LINE_LOOP)
            for corner in corners:
                glVertex3f(*corner)
            glEnd()
            glPopMatrix()

    def render_full_wireframe(self, position, color=(1.0, 1.0, 0.0)):
        """Render a full wireframe cube at the given position."""
        if position:
            glPushMatrix()
            glTranslatef(position[0] + 0.5, position[1] + 0.5, position[2] + 0.5)
            glColor3f(*color)  # Wireframe color
            glLineWidth(3.0)  # Increase line width for better visibility
            glBegin(GL_LINES)

            # List of cube edges (pairs of vertices)
            edges = [
                (-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5),
                (-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5),
                (-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5),
                (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5),

                (0.5, -0.5, -0.5), (0.5, -0.5, 0.5),
                (0.5, -0.5, 0.5), (0.5, 0.5, 0.5),
                (0.5, 0.5, 0.5), (0.5, 0.5, -0.5),
                (0.5, 0.5, -0.5), (0.5, -0.5, -0.5),

                (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5),
                (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5),
                (-0.5, 0.5, 0.5), (0.5, 0.5, 0.5),
                (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5),
            ]

            # Draw edges
            for edge in edges:
                glVertex3f(*edge)
            glEnd()
            glPopMatrix()

    def render_solid_block(self, position, color=(0.6, 0.6, 0.6)):
        """Render a solid block at the given position."""
        if position:
            glPushMatrix()
            glTranslatef(position[0] + 0.5, position[1] + 0.5, position[2] + 0.5)
            glColor3f(*color)  # Solid block color

            # Render the solid cube
            glBegin(GL_QUADS)
            # Front face
            glVertex3f(-0.5, -0.5, 0.5)
            glVertex3f(0.5, -0.5, 0.5)
            glVertex3f(0.5, 0.5, 0.5)
            glVertex3f(-0.5, 0.5, 0.5)
            # Back face
            glVertex3f(-0.5, -0.5, -0.5)
            glVertex3f(0.5, -0.5, -0.5)
            glVertex3f(0.5, 0.5, -0.5)
            glVertex3f(-0.5, 0.5, -0.5)
            # Left face
            glVertex3f(-0.5, -0.5, -0.5)
            glVertex3f(-0.5, -0.5, 0.5)
            glVertex3f(-0.5, 0.5, 0.5)
            glVertex3f(-0.5, 0.5, -0.5)
            # Right face
            glVertex3f(0.5, -0.5, -0.5)
            glVertex3f(0.5, -0.5, 0.5)
            glVertex3f(0.5, 0.5, 0.5)
            glVertex3f(0.5, 0.5, -0.5)
            # Top face
            glVertex3f(-0.5, 0.5, -0.5)
            glVertex3f(0.5, 0.5, -0.5)
            glVertex3f(0.5, 0.5, 0.5)
            glVertex3f(-0.5, 0.5, 0.5)
            # Bottom face
            glVertex3f(-0.5, -0.5, -0.5)
            glVertex3f(0.5, -0.5, -0.5)
            glVertex3f(0.5, -0.5, 0.5)
            glVertex3f(-0.5, -0.5, 0.5)
            glEnd()

            glPopMatrix()


    def render_blocks_with_wireframes(self):
        """Render all blocks with a solid cube and wireframe edges."""
        for block in self.blocks:
            # Render the solid cube
            self.render_solid_block(block, color=(0.6, 0.6, 0.6))  # Gray for solid blocks

            # Render the wireframe around the block
            self.render_full_wireframe(block, color=(0.0, 0.0, 0.0))  # Black for wireframe
