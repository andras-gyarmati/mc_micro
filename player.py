from math import sin, cos, radians


class Player:
    def __init__(self, bounding_box, start_position=(0.0, 1.0, 0.0)):
        self.position = list(start_position)  # Player's position in the world
        self.bounding_box = bounding_box  # Bounding box as [(min_x, max_x), (min_y, max_y), (min_z, max_z)]
        self.velocity = [0.0, 0.0, 0.0]  # Velocity vector for movement and gravity
        self.gravity = -9.8  # Gravity constant
        self.jump_speed = 15.0  # Initial upward velocity when jumping
        self.speed = 5.0  # Movement speed (units per second)
        self.yaw = -90.0  # Horizontal rotation (degrees)
        self.pitch = 0.0  # Vertical rotation (degrees)
        self.camera_front = [0.0, 0.0, -1.0]  # Camera direction
        self.camera_up = [0.0, 1.0, 0.0]  # Up vector
        self.grounded = True  # Is the player on the ground?

    def update(self, delta_time, keys):
        """Update player position and physics."""
        # Calculate movement direction based on key presses
        forward = [
            cos(radians(self.yaw)) * cos(radians(self.pitch)),
            sin(radians(self.pitch)),
            sin(radians(self.yaw)) * cos(radians(self.pitch)),
        ]
        right = [
            -forward[2],  # Corrected sign
            0,
            forward[0],
        ]
        self.normalize(right)
        self.normalize(forward)

        # Movement based on keys
        movement = [0.0, 0.0, 0.0]
        if keys.get("W", False):  # Move forward
            movement[0] += forward[0] * self.speed * delta_time
            movement[1] += forward[1] * self.speed * delta_time
            movement[2] += forward[2] * self.speed * delta_time
        if keys.get("S", False):  # Move backward
            movement[0] -= forward[0] * self.speed * delta_time
            movement[1] -= forward[1] * self.speed * delta_time
            movement[2] -= forward[2] * self.speed * delta_time
        if keys.get("A", False):  # Move left
            movement[0] -= right[0] * self.speed * delta_time
            movement[2] -= right[2] * self.speed * delta_time
        if keys.get("D", False):  # Move right
            movement[0] += right[0] * self.speed * delta_time
            movement[2] += right[2] * self.speed * delta_time

        # Apply movement
        self.position[0] += movement[0]
        self.position[1] += movement[1]
        self.position[2] += movement[2]

        # Apply gravity
        if not self.grounded:
            self.velocity[1] += self.gravity * delta_time
        else:
            self.velocity[1] = 0.0

        # Apply vertical movement (gravity or jump)
        self.position[1] += self.velocity[1] * delta_time

        # Enforce bounding box constraints
        self.position[0] = max(self.bounding_box[0][0], min(self.bounding_box[0][1], self.position[0]))
        self.position[1] = max(self.bounding_box[1][0], min(self.bounding_box[1][1], self.position[1]))
        self.position[2] = max(self.bounding_box[2][0], min(self.bounding_box[2][1], self.position[2]))

        # Check if grounded
        if self.position[1] <= self.bounding_box[1][0] + 0.001:
            self.grounded = True
            self.position[1] = self.bounding_box[1][0]
        else:
            self.grounded = False

        # Ensure the player remains above the floor:
        if self.position[1] < self.bounding_box[1][0] + 1.5:
            self.position[1] = self.bounding_box[1][0] + 1.5  # Ensure the player stays slightly above the floor
            self.grounded = True
        else:
            self.grounded = False

    def jump(self):
        """Make the player jump if grounded."""
        if self.grounded:
            self.velocity[1] = self.jump_speed
            self.grounded = False

    def handle_mouse(self, dx, dy, sensitivity=0.1):
        """Handle mouse movement to rotate the camera."""
        # Apply sensitivity
        dx *= sensitivity
        dy *= sensitivity

        # Debug the changes to yaw and pitch
        # print(f"Before update: yaw={self.yaw}, pitch={self.pitch}")

        # Update yaw and pitch
        self.yaw += dx
        self.pitch += dy

        # Clamp pitch to avoid flipping
        self.pitch = max(-89.0, min(89.0, self.pitch))

        # Debug the changes after update
        # print(f"After update: yaw={self.yaw}, pitch={self.pitch}")

        # Update the camera direction vector based on yaw and pitch
        self.camera_front[0] = cos(radians(self.yaw)) * cos(radians(self.pitch))
        self.camera_front[1] = sin(radians(self.pitch))
        self.camera_front[2] = sin(radians(self.yaw)) * cos(radians(self.pitch))
        self.normalize(self.camera_front)


    def normalize(self, vector):
        """Normalize a 3D vector."""
        length = (vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2) ** 0.5
        if length > 0.0:
            vector[0] /= length
            vector[1] /= length
            vector[2] /= length

    def get_position(self):
        """Get the player's current position."""
        return self.position

    def get_camera_direction(self):
        """Get the direction the camera is facing."""
        return self.camera_front
