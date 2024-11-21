import math


def normalize(vector):
    """Normalize a 3D vector."""
    length = math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
    if length > 0:
        return [vector[0] / length, vector[1] / length, vector[2] / length]
    return [0.0, 0.0, 0.0]


def dot_product(v1, v2):
    """Calculate the dot product of two 3D vectors."""
    return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]


def cross_product(v1, v2):
    """Calculate the cross product of two 3D vectors."""
    return [
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0],
    ]


def raycast_to_grid(origin, direction, max_distance, grid_size=(1, 1, 1)):
    """
    Perform a raycast to a 3D grid and yield grid positions.
    - origin: Starting point of the ray.
    - direction: Normalized direction of the ray.
    - max_distance: Maximum distance for the raycast.
    - grid_size: Size of each grid cell.

    Yields:
    - (grid_x, grid_y, grid_z): Grid cell coordinates.
    """
    position = list(origin)
    direction = normalize(direction)

    step = [direction[i] * 0.1 for i in range(3)]  # Small step size for ray traversal
    for _ in range(int(max_distance / 0.1)):
        # Calculate the grid position
        grid_pos = (
            int(math.floor(position[0] / grid_size[0])),
            int(math.floor(position[1] / grid_size[1])),
            int(math.floor(position[2] / grid_size[2])),
        )

        # Check if within bounds
        yield grid_pos

        # Step along the ray
        for i in range(3):
            position[i] += step[i]


def clamp(value, min_value, max_value):
    """Clamp a value between a minimum and maximum."""
    return max(min_value, min(max_value, value))


def within_bounding_box(position, bounding_box):
    """
    Check if a position is within a given bounding box.
    - position: (x, y, z)
    - bounding_box: [(min_x, max_x), (min_y, max_y), (min_z, max_z)]
    """
    return all(
        bounding_box[i][0] <= position[i] <= bounding_box[i][1] for i in range(3)
    )
