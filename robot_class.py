import random

import matplotlib.pyplot as plt


class Robot:
    """
    This Robot lives in 2D, x-y space, and its motion is
    pointed in a random direction, initially.
    It moves in a straight line until it comes close to a wall
    at which point it stops.
    For measurements, it  senses the x- and y-distance
    to landmarks. This is different from range and bearing as
    commonly studied in the literature, but this makes it much
    easier to implement the essentials of SLAM without
    cluttered math.
    """

    def __init__(
        self,
        world_size=100.0,
        measurement_range=30.0,
        motion_noise=1.0,
        measurement_noise=1.0,
    ):
        """
        creates a Robot with the specified parameters and initializes
        the location (self.x, self.y) to the center of the world
        :param world_size:
        :param measurement_range:
        :param motion_noise:
        :param measurement_noise:
        """
        self.measurement_noise = 0.0
        self.world_size = world_size
        self.measurement_range = measurement_range
        self.x = world_size / 2.0
        self.y = world_size / 2.0
        self.motion_noise = motion_noise
        self.measurement_noise = measurement_noise
        self.landmarks = []
        self.num_landmarks = 0

    # returns a positive, random float
    @staticmethod
    def rand():
        return random.random() * 2.0 - 1.0

    def move(self, dx, dy):
        """
        attempts to move Robot by dx, dy. If outside world
        boundary, then the move does nothing and instead returns failure
        :param dx:
        :param dy:
        :return:
        """
        x = self.x + dx + self.rand() * self.motion_noise
        y = self.y + dy + self.rand() * self.motion_noise

        if x < 0.0 or x > self.world_size or y < 0.0 or y > self.world_size:
            return False
        else:
            self.x = x
            self.y = y
            return True

    def sense(self):
        """This function does not take in any parameters, instead it references internal variables
        (such as self.landamrks) to measure the distance between the Robot and any landmarks
        that the Robot can see (that are within its measurement range).
        This function returns a list of landmark indices, and the measured distances (dx, dy)
        between the Robot's position and said landmarks.
        This function should account for measurement_noise and measurement_range.
        One item in the returned list should be in the form: [landmark_index, dx, dy].

        returns x- and y- distances to landmarks within visibility range
        because not all landmarks may be in this range, the list of measurements
        is of variable length. Set measurement_range to -1 if you want all
        landmarks to be visible at all times
        """

        measurements = []

        # iterate through all of the landmarks in a world
        # For each landmark
        # 1. compute dx and dy, the distances between the Robot and the landmark
        # 2. account for measurement noise by *adding* a noise component to dx and dy
        #    - The noise component should be a random value between [-1.0, 1.0)*measurement_noise
        #    - Feel free to use the function self.rand() to help calculate this noise component
        # 3. If either of the distances, dx or dy, fall outside of the internal var, measurement_range
        #    then we cannot record them; if they do fall in the range, then add them to the measurements list
        #    as list.append([index, dx, dy]), this format is important for data creation done later
        for landmark_id, landmark in enumerate(self.landmarks):
            dx = abs(self.x - landmark[0] + self.rand() * self.measurement_noise)
            dy = abs(self.y - landmark[1] + self.rand() * self.measurement_noise)

            if dx <= self.measurement_range and dy <= self.measurement_range:
                measurements.append([landmark_id, dx, dy])

        return measurements

    def make_landmarks(self, num_landmarks):
        """
        make random landmarks located in the world
        :param num_landmarks:
        :return:
        """
        self.landmarks = []
        for i in range(num_landmarks):
            self.landmarks.append(
                [
                    round(random.random() * self.world_size),
                    round(random.random() * self.world_size),
                ]
            )
        self.num_landmarks = num_landmarks

    # called when print(Robot) is called; prints the Robot's location
    def __repr__(self):
        return "Robot: [x=%.5f y=%.5f]" % (self.x, self.y)


if __name__ == "__main__":
    world_size = 10.0  # size of world (square)
    measurement_range = 5.0  # range at which we can sense landmarks
    motion_noise = 0.2  # noise in robot motion
    measurement_noise = 0.2  # noise in the measurements

    # instantiate a robot, r
    r = Robot(world_size, measurement_range, motion_noise, measurement_noise)

    # print out the location of r
    print(r)

    # import helper function
    from helpers import display_world

    # define figure size
    plt.rcParams["figure.figsize"] = (5, 5)

    # call display_world and display the robot in it's grid world
    print(r)
    display_world(int(world_size), [r.x, r.y])

    # Movement

    # choose values of dx and dy (negative works, too)
    dx = 1
    dy = 2
    r.move(dx, dy)

    # print out the exact location
    print(r)

    # display the world after movement, not that this is the same call as before
    # the robot tracks its own movement
    display_world(int(world_size), [r.x, r.y])

    # create any number of landmarks
    num_landmarks = 3
    r.make_landmarks(num_landmarks)

    # print out our robot's exact location
    print(r)

    # display the world including these landmarks
    display_world(int(world_size), [r.x, r.y], r.landmarks)

    # print the locations of the landmarks
    print("Landmark locations [x,y]: ", r.landmarks)

    # Sense
    # try to sense any surrounding landmarks
    measurements = r.sense()

    # this will print out an empty list if `sense` has not been implemented
    print(measurements)

    print(r.landmarks)
