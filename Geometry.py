from typing import List, Tuple
import random
import math

def clamp(x):
	return max(min(1, x), 0)

class Point:
	def __init__(self, x: float, y: float):
		self.x = clamp(x)
		self.y = clamp(y)

	def generate_variant(self, mutation_rate: float):
		x = self.x + random.uniform(-1, 1)*mutation_rate*10
		y = self.y + random.uniform(-1, 1)*mutation_rate*10
		
		return Point(x, y)

	@classmethod
	def generate_random(cls):
		x, y = (random.random(), random.random())
		return cls(x, y)


class Color:
	def __init__(self, r: float, g: float, b: float, a: float):
		self.r = clamp(r)
		self.g = clamp(g)
		self.b = clamp(b)
		self.a = clamp(a)

		#print(r, g, b, a)


	def __eq__(self, other):
		return math.isclose(self.r, other.r) and math.isclose(self.g, other.g) and math.isclose(self.b, other.b)


	def generate_variant(self, mutation_rate: float):
		r = self.r + random.uniform(-1, 1)*mutation_rate*10
		g = self.g + random.uniform(-1, 1)*mutation_rate*10
		b = self.b + random.uniform(-1, 1)*mutation_rate*10
		a = self.a + random.uniform(-1, 1)*mutation_rate*10

		return Color(r, g, b, a)

	@classmethod
	def generate_random(cls, image = None):
		if image is not None:
			image_size = (image.shape[0], image.shape[1])
			pixel = image[random.randrange(0, image_size[0]), random.randrange(0, image_size[1])]/255
			return cls(pixel[0], pixel[1], pixel[2], random.random())
		return cls(random.random(), random.random(), random.random(), random.random())


class Polygon:
	def __init__(self, points: List[Point], color: Color):
		self.points = points[:5]
		self.color = color

	def generate_variant(self, mutation_rate: float):
		

		points = []
		for point in self.points:
			if random.random() < mutation_rate:
				new_point = point.generate_variant(mutation_rate)
				points.append(new_point)
			else:
				points.append(point)
	
		points = self.points.copy()
		# Randomly remove a point
		if len(self.points) > 3:
			if random.random() < mutation_rate:
				points.remove(random.choice(points))


		# Randomly add a new point
		if random.random() < mutation_rate*2:
			points.insert(random.randrange(len(points)), (Point.generate_random()))


		# Randomly change color
		
		color = self.color
		if random.random() < mutation_rate:
			color = Color.generate_random()
		
		color = color.generate_variant(mutation_rate)
		return Polygon(points, color)


	@classmethod
	def generate_random(cls, image = None):
		num_points = random.randrange(2) + 3

		points = []
		for _ in range(num_points):
			p = Point.generate_random()
			points.append(p)

		color = Color.generate_random(image)

		return cls(points, color)




