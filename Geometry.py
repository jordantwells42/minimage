from typing import List, Tuple
import random
import math

class Point:
	def __init__(self, x: float, y: float):
		if not (0 < x < 1):
			x = round(x, 0)
		if not (0 < y < 1):
			y = round(y, 0)

		self.x = x
		self.y = y

	def generate_variant(self, mutation_rate: float):
		x = self.x + random.uniform(-1, 1)*mutation_rate/10
		y = self.y + random.uniform(-1, 1)*mutation_rate/10
		
		return Point(x, y)

	@classmethod
	def generate_random(cls):
		x, y = (random.random(), random.random())
		return cls(x, y)


class Color:
	def __init__(self, r: float, g: float, b: float):
		self.r = r
		self.g = g
		self.b = b
		self.a = 0.3


	def __eq__(self, other):
		return math.isclose(self.r, other.r) and math.isclose(self.g, other.g) and math.isclose(self.b, other.b)

	@classmethod
	def generate_random(cls, image = None):
		if image is not None:
			image_size = (image.shape[0], image.shape[1])
			pixel = image[random.randrange(0, image_size[0]), random.randrange(0, image_size[1])]/255
			return cls(pixel[0], pixel[1], pixel[2])
		return cls(random.random(), random.random(), random.random())


class Polygon:
	def __init__(self, points: List[Point], color: Color):
		self.points = points[0:3]
		self.color = color

	def generate_variant(self, mutation_rate: float):
		points = []

		for point in self.points:
			new_point = point.generate_variant(mutation_rate)
			points.append(new_point)

		# Randomly remove a point
		if len(self.points) > 3:
			if random.random() < mutation_rate:
				points.remove(random.choice(points))


		# Randomly add a new point
		if random.random() < mutation_rate:
			points.append(Point.generate_random())


		# Randomly change color
		color = self.color
		if random.random() < mutation_rate:
			color = Color.generate_random()


		return Polygon(points, color)


	@classmethod
	def generate_random(cls, image = None):
		num_points = random.randrange(10) + 3

		points = []
		for _ in range(num_points):
			p = Point.generate_random()
			points.append(p)

		color = Color.generate_random(image)

		return cls(points, color)




