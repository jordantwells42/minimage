import random
from typing import List, Tuple
from pathlib import Path
import pickle

import itertools

import imageio.v3 as iio
from tqdm import tqdm

from Creature import Creature



class Generation:
	def __init__(self, seed_creatures: List[Creature], mutation_rate: float = 0.05, image = None):
		self.creatures = self._generate_offspring(seed_creatures, mutation_rate, image)


	@classmethod
	def generate_first_generation(cls, quota : int, image = None):
		seed_creatures = []

		for _ in range(quota):
			seed_creatures.append(Creature.generate_random(image))

		return cls(seed_creatures)



	def _generate_offspring(self, seed_creatures: List[Creature], mutation_rate, image = None) -> List[Creature]:
		new_generation = []
		
		for parent1, parent2 in itertools.combinations(seed_creatures, r = 2):
			offspring = parent1.generate_offspring_half(parent2, mutation_rate)
			offspring = offspring.generate_variant(mutation_rate, image)
			new_generation.append(offspring)

		

		for asexual in seed_creatures:
			offspring = asexual.generate_variant(mutation_rate, image)
			new_generation.append(offspring)


		new_generation.append(seed_creatures[0])

		return new_generation


	def calculate_fitness(self, image, LOD: int = 1):
		#print(self.creatures)
		for creature in tqdm(self.creatures):
			creature.calculate_fitness(image, LOD)
		self.creatures = sorted(self.creatures, key = lambda x: x.fitness, reverse = True)



	def select(self, quota: int):
		return self.creatures[:quota]
		return random.choices(self.creatures, weights = [e.fitness for e in self.creatures], k = quota)


	def print_best_worst(self):
		print(self.creatures[0].fitness, self.creatures[-1].fitness)

	def get_best(self):
		return self.creatures[0]

	def display_best(self):
		self.get_best().draw((400,400))


	def save_best(self, name: str, size: Tuple[int], run_dir: Path):
		creature = self.get_best()
		c_img = creature.get_image(size)
		iio.imwrite(run_dir / (name + ".png"), c_img)


if __name__ == "__main__":
	quota = 3
	image = iio.imread('poland-small.jpg')
	size = (image.shape[0], image.shape[1])
	LOD = 50
	mutation_rate = 0.01
	rounds = 10000000
	run_dir = Path("./runs/poland")
	run_dir.mkdir(0o774, parents=True, exist_ok=True)

	print("Generating first generation")
	name = "poland"

	if False:
		g1 = Generation.generate_first_generation(quota)

		g = g1

		
		for i in range(rounds):
			print("Calculating Fitness of Generation")
			g.calculate_fitness(image, LOD)

			print("Displaying best fitness:", end = " ")
			g.print_best_worst()

			if i % 100 == 0:
				g.save_best(str(i), size, run_dir)
				c = g.get_best()
				pickle.dump(c, open(f"{name}.p", "wb" ) )

			print("Selecting creatures to survive")
			selected_creatures = g.select(quota)
			print(len(selected_creatures))
			print(f"Generating new generation: {i}")
			g = Generation(selected_creatures, mutation_rate)
			
		plt.show()
		
	else:

		c1 = Creature.generate_random()
		c1.calculate_fitness(image, LOD)
		f1 = c1.fitness


		for i in range(rounds):

			c2 = c1.generate_variant(mutation_rate, image)
			c2.calculate_fitness(image, LOD)

			f2 = c2.fitness


			if f2 > f1:
				c1 = c2
				f1 = f2
				print(f2)


			if i % 100 == 0:
				c_img = c1.get_image(size)
				iio.imwrite(run_dir / (str(i) + ".png"), c_img)
				pickle.dump(c1, open(f"{name}.p", "wb" ) )



