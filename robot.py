"""A robot simulation script.

Robot controls:
  Right arrow: Steers robot to the `right` direction.
  Left: arrow: Steers robot to the `left` direction.
  Space bar: Moves robot forward.

Author: Daryl Ronquillo
"""

import Tkinter


# Robot properties.
_ROBOT_POSITION = 50, 0, 100, 100
_ROBOT_ACCELERATION = 5  # Acceleration in pixels.
_ROBOT_WIDTH = 50
_ROBOT_HEIGHT = 100

# Canvas properties.
_CANVAS_WIDTH = 500
_CANVAS_HEIGHT = 500


def _GetNextDirection(direction, previous_direction):
  """Computes next direction.

  Args:
    direction: String, user intended direction, right or left.
    previous_direction: String, user's last previous direction.

  Returns:
    String, next direction.
      Up, down, right, left, also equivalent to north, south, west east.
  """
  next_direction = None
  if previous_direction == 'Up':
    if direction == 'Right':
      next_direction = 'Right'
    if direction == 'Left':
      next_direction = 'Left'

  elif previous_direction == 'Down':
    if direction == 'Right':
      next_direction = 'Left'
    if direction == 'Left':
      next_direction = 'Right'

  elif previous_direction == 'Left':
    if direction == 'Right':
      next_direction = 'Up'
    if direction == 'Left':
      next_direction = 'Down'

  elif previous_direction == 'Right':
    if direction == 'Right':
      next_direction = 'Down'
    if direction == 'Left':
      next_direction = 'Up'

  return next_direction


class Robot(object):
  """A robot simulation.

  Attributes:
    canvas: Tkinter canvas object.
    robot: Tkinter Rectangle object.
    current_direction: String, current direction of the robot,
        based from user keypress event.
    previous_direction: String, previous direction of the robot or previous user
        keypress event.
    acceleration: Integer, number of pixels per robot movement.
    initial_coordinates: Tuple, robot shape and/or location coordinates.
  """

  def __init__(self, robot_canvas, initial_coordinates, acceleration=5):
    self.canvas = robot_canvas
    self.robot = self.canvas.create_rectangle(
        *initial_coordinates,
        fill='Grey',
        outline='Grey',
        tags='robot'
    )
    self.current_direction = 'Up'
    self.previous_direction = None
    self.acceleration = acceleration

    # Move.
    root.bind('<space>', self.Move)

    # Steering.
    root.bind('<Right>', self.Steer)
    root.bind('<Left>', self.Steer)

  def Move(self, unused_moved):
    """Allows robot to move forward."""
    x, y = 0, 0
    if self.current_direction in ('Up', 'Down'):
      y = (-self.acceleration
           if self.current_direction == 'Up' else self.acceleration)
    elif self.current_direction in ('Right', 'Left'):
      x = (self.acceleration
           if self.current_direction == 'Right' else -self.acceleration)

    # Prevent the robot from falling down the sreen!
    new_coords = self.canvas.coords(self.robot)
    x1, y1, x2, y2 = new_coords
    if (
        x2 > _CANVAS_WIDTH or
        x1 < 1 or
        y2 > _CANVAS_HEIGHT or
        y1 < 1
    ):
      return

    # Move the robot within the canvas only.
    self.canvas.move(self.robot, x, y)

  def Steer(self, event):
    """Changes robot direction.

    Args:
      event: Object, keypress event.
    """

    # Get intended direction.
    next_direction = _GetNextDirection(
        direction=event.keysym, previous_direction=self.current_direction)
    self.previous_direction = self.current_direction

    # Current robot coordinates.
    new_coords = self.canvas.coords(self.robot)
    x1, y1, x2, y2 = new_coords

    # Direct robot.
    if next_direction == 'Right':
      if self.previous_direction == 'Up':
        new_coords = (x1, y2-_ROBOT_WIDTH, x1+_ROBOT_HEIGHT, y2)
      elif self.previous_direction == 'Down':
        new_coords = (x1, y1, x1+_ROBOT_HEIGHT, y1+_ROBOT_WIDTH)

    elif next_direction == 'Left':
      if self.previous_direction == 'Up':
        new_coords = (x2-_ROBOT_HEIGHT, y2-_ROBOT_WIDTH, x2, y2)
      elif self.previous_direction == 'Down':
        new_coords = [x2-_ROBOT_HEIGHT, y2-_ROBOT_WIDTH, x2, y1]

    elif next_direction == 'Up':
      if self.previous_direction == 'Left':
        new_coords = (x2-_ROBOT_WIDTH, y2-_ROBOT_HEIGHT, x2, y2)
      if self.previous_direction == 'Right':
        new_coords = (x1, y2-_ROBOT_HEIGHT, x1+_ROBOT_WIDTH, y2)

    elif next_direction == 'Down':
      if self.previous_direction == 'Right':
        new_coords = (x1, y1, x1+_ROBOT_WIDTH, y1+_ROBOT_HEIGHT)
      elif self.previous_direction == 'Left':
        new_coords = (x2-_ROBOT_WIDTH, y1, x2, y1+_ROBOT_HEIGHT)

    # Set current direction to intended direction.
    self.current_direction = next_direction
    self.canvas.coords(self.robot, *new_coords)


if __name__ == '__main__':
  root = Tkinter.Tk()
  canvas = Tkinter.Canvas(root, width=_CANVAS_WIDTH, height=_CANVAS_HEIGHT)
  canvas.pack()
  Robot(canvas, _ROBOT_POSITION, _ROBOT_ACCELERATION)
  root.mainloop()

