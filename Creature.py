from typing import List, Tuple
import random
from pathlib import	 Path

import numpy as np
import matplotlib.pyplot as plt
import imageio.v3 as iio


from Geometry import Point, Polygon


class Creature:

	def __init__(self, polygons: List[Polygon]):
		self.polygons = polygons
		self.fitness = 0


	def calculate_complexity(self, LOD: int = 1) -> None:
		num_polygons = len(self.polygons)
		num_colors = 0
		num_points = 0
		colors = []

		for polygon in self.polygons:
			num_points += len(polygon.points)

			if polygon.color not in colors:
				num_colors += 1
				colors.append(polygon.color)


		complexity = (num_polygons*num_colors*num_points)
		print(complexity)
		return complexity**(1/LOD)

	def calculate_error(self, img):
		err = 0

		c_img = self.get_image(size = (img.shape[0], img.shape[1]))

		for i, j in zip(c_img, img):
			for c_pixel, i_pixel in zip(i, j):
				red_err = (c_pixel[0]/255 - i_pixel[0]/255)**2
				green_err = (c_pixel[1]/255 - i_pixel[1]/255)**2
				blue_err = (c_pixel[2]/255 - i_pixel[2]/255)**2

				print(c_pixel, i_pixel)
				print(red_err, green_err, blue_err)

				err += red_err + green_err + blue_err

		return err


	def calculate_fitness(self, image, LOD: int = 1):
		self.fitness = 1/(self.calculate_error(image)*self.calculate_complexity(LOD))
		return self.fitness


	def generate_variant(self, mutation_rate):
		polygons = []
		colors = []


		for polygon in self.polygons:
			new_polygon = polygon.generate_variant(mutation_rate)
			polygons.append(new_polygon)
			colors.append(polygon.color)


		# Randomly remove a polygon
		if len(self.polygons) > 2:
			if random.random() < mutation_rate:
				polygons.remove(random.choice(polygons))

		# Randomly add a new polygon
		if random.random() < mutation_rate:

			random_polygon = Polygon.generate_random()

			# Choose either from existing colors or new color
			if random.random() < 0.5:
				color = random.choice(colors)
			else:
				color = Color.generate_random()

			random_polygon.color = color

			polygons.append(random_polygon)



		return Creature(polygons)

	def generate_offspring(self, other: Creature, mutation_rate):
		polygons = []

		self_polygons = self.polygons.copy()
		for _ in range(len(self.polygons)//2):
			self_polygons.remove(random.choice(self_polygons))

		other_polygons = other.polygons.copy()
		for _ in range(len(other.polygons)//2):
			other_polygons.remove(random.choice(other_polygons))

		polygons += self_polygons + other_polygons
		random.shuffle(polygons)

		offspring = Creature(polygons).generate_variant(mutation_rate)


	def draw(self, size: Tuple[int]):
		self.get_image(size)
		plt.show()


	def get_image(self, size):
		fig, ax = plt.subplots()
		ax.axis('off')
		fig.tight_layout(pad=0)
		fig.set_size_inches(size[1]/100,  size[0]/100, forward=True)
		fig.set_dpi(100)

		# To remove the huge white borders
		ax.margins(0)
		for polygon in self.polygons:
			xs = []
			ys = []

			for point in polygon.points:
				xs.append(point.x)
				ys.append(point.y)

			color = (polygon.color.r, polygon.color.g, polygon.color.b)

			plt.fill(xs, ys, facecolor=color, edgecolor=color)

		fig.canvas.draw()
		image_from_plot = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
		image_from_plot = image_from_plot.reshape(fig.canvas.get_width_height()[::-1] + (3,))
		return image_from_plot

	@classmethod
	def generate_random(cls):
		num_polygons = random.randrange(3) + 1

		polygons = []
		for _ in range(num_polygons):
			polygon = Polygon.generate_random()
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
