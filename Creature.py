from typing import List, Tuple
import random
from pathlib import	 Path
import math

import numpy as np
import matplotlib.pyplot as plt
import imageio.v3 as iio
import matplotlib
matplotlib.use("Agg")


from Geometry import Point, Polygon, Color


class Creature:

	def __init__(self, polygons: List[Polygon]):
		self.polygons = polygons
		self.fitness = 0


	def calculate_complexity(self, LOD: int = 1) -> None:
		return 1
		num_polygons = len(self.polygons)
		"""
		num_colors = 0
		num_points = 0
		colors = []

		for polygon in self.polygons:
			num_points += len(polygon.points)

			if polygon.color not in colors:
				num_colors += 1
				colors.append(polygon.color)
		"""

		complexity = (num_polygons)
		return math.log(complexity)

	def calculate_error(self, img):
		err = 0

		c_img = self.get_image(size = (img.shape[0], img.shape[1]))
		c_img = c_img/255
		img = img/255

		diff = (c_img - img)**2
		err = np.sum(diff)/(img.shape[0] * img.shape[1])

		return err

	def calculate_fitness(self, image, LOD: int = 1):
		self.fitness = math.exp(1 + 1/(self.calculate_error(image) *self.calculate_complexity(LOD)))
		return self.fitness


	def generate_variant(self, mutation_rate, image = None):
		polygons = []

		
		for polygon in self.polygons:
			if random.random() < mutation_rate:
				new_polygon = polygon.generate_variant(mutation_rate)
				polygons.append(new_polygon)
			else:
				polygons.append(polygon)



		# Randomly remove a polygon
		if len(polygons) > 2:
			if random.random() < mutation_rate:
				polygons.remove(random.choice(polygons))

		# Randomly add a new polygon
		if random.random() < mutation_rate * 2:
			random_polygon = Polygon.generate_random(image)
			polygons.insert(random.randrange(len(polygons)), random_polygon)

		return Creature(polygons)

	def generate_offspring_half(self, other, mutation_rate: float):
		polygons = []

		self_polygons = self.polygons.copy()
		for _ in range(len(self.polygons)//2):
			self_polygons.remove(random.choice(self_polygons))

		other_polygons = other.polygons.copy()
		for _ in range(len(other.polygons)//2):
			other_polygons.remove(random.choice(other_polygons))


			


		polygons += self_polygons + other_polygons

		if len(polygons) > 2:
			polygons.remove(random.choice(polygons))
		if len(polygons) > 2:
			polygons.remove(random.choice(polygons))

		random.shuffle(polygons)

		offspring = Creature(polygons)
		return offspring


	def generate_offspring_most(self, other, mutation_rate: float):
		polygons =  self.polygons.copy()


		if len(polygons) > 2:
			polygons.remove(random.choice(polygons))
		if len(polygons) > 2:
			polygons.remove(random.choice(polygons))

		polygons.append(random.choice(other.polygons))
		polygons.append(random.choice(other.polygons))
		
		random.shuffle(polygons)

		offspring = Creature(polygons)
		return offspring


	def draw(self, size: Tuple[int]):
		fig, ax = plt.subplots()
		ax.axis('off')
		grayness = 0
		fig.tight_layout(pad=0)
		fig.set_size_inches(size[1]/20,  size[0]/20, forward=True)
		fig.set_dpi(300)
		plt.fill([0, 0, 1, 1], [0, 1, 1, 0], facecolor=(grayness/255, grayness/255, grayness/255, 1))
		# To remove the huge white borders
		ax.margins(0)
		for polygon in self.polygons:
			xs = []
			ys = []

			for point in polygon.points:
				xs.append(point.x)
				ys.append(point.y)

			color = (polygon.color.r, polygon.color.g, polygon.color.b, polygon.color.a)

			plt.fill(xs, ys, facecolor=color)
		

		fig.canvas.draw()
		plt.show(block=False)
		plt.close('all')


	def get_image(self, size):
		fig, ax = plt.subplots()
		grayness = 0
		ax.axis('off')
		fig.tight_layout(pad=0)
		fig.set_size_inches(size[1]/100,  size[0]/100, forward=True)
		fig.set_dpi(100)
		plt.fill([0, 0, 1, 1], [0, 1, 1, 0], facecolor=(grayness/255, grayness/255, grayness/255, 1))
		# To remove the huge white borders
		ax.margins(0)
		for polygon in self.polygons:
			xs = []
			ys = []

			for point in polygon.points:
				xs.append(point.x)
				ys.append(point.y)

			color = (polygon.color.r, polygon.color.g, polygon.color.b, polygon.color.a)

			plt.fill(xs, ys, facecolor=color)


		fig.canvas.draw()
		image_from_plot = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
		image_from_plot = image_from_plot.reshape(fig.canvas.get_width_height()[::-1] + (3,))
		plt.close('all')
		del fig
		return image_from_plot

	@classmethod
	def generate_random(cls, image = None):
		num_polygons = random.randrange(5) + 1

		polygons = []

		for _ in range(num_polygons):
			polygon = Polygon.generate_random(image)
			polygons.append(polygon)


		return cls(polygons)


if __name__ == "__main__":
	"""
	p1 = Point(0.1, 0.1)
	p2 = Point(0.8, 0.2)
	p3 = Point(0.5, 0.9)

	red_triangle = Polygon(points = [p1, p2, p3], color = (1, 0, 0))

	creature = Creature([red_triangle])
	creature.draw()
	"""


	im = iio.imread('eddy.jpg')


	creature = Creature.generate_random()
	#creature.draw(size = (im.shape[0], im.shape[1]))
	creature.calculate_fitness(im, 1)

	print(creature.fitness)
