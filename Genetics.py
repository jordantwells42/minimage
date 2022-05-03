import random
from typing import List, Tuple
from pathlib import Path

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
		for parent1 in seed_creatures:
			for parent2 in seed_creatures:
				offspring = parent1.generate_offspring_most(parent2, mutation_rate)
				offspring = offspring.generate_variant(mutation_rate, image)
				new_generation.append(offspring)

		for asexual in seed_creatures:
			offspring = asexual.generate_variant(mutation_rate, image)
			new_generation.append(offspring)


		return new_generation


	def calculate_fitness(self, image, LOD: int = 1):
		#print(self.creatures)
		for creature in tqdm(self.creatures):
			creature.calculate_fitness(image, LOD)


	def select(self, quota: int):
		self.get_best()
		return self.creatures[0:quota]
		return random.choices(self.creatures, weights = [e.fitness for e in self.creatures], k = quota)


	def print_best_worst(self):
		self.get_best()
		print(self.creatures[0].fitness, self.creatures[-1].fitness)

	def get_best(self):
		self.creatures = sorted(self.creatures, key = lambda x: x.fitness, reverse = True)

		return self.creatures[0]

	def display_best(self):
		self.get_best().draw((400,400))


	def save_best(self, name: str, size: Tuple[int], run_dir: Path):
		creature = self.get_best()
		c_img = creature.get_image(size)
		iio.imwrite(run_dir / (name + ".png"), c_img)




if __name__ == "__main__":
	quota = 50
	image = iio.imread('eddy.jpg')
	size = (image.shape[0], image.shape[1])
	LOD = 1
	mutation_rate = 0.4
	rounds = 1000
	run_dir = Path("./runs/1")
	run_dir.mkdir(0o774, parents=True, exist_ok=True)

	print("Generating first generation")
	g1 = Generation.generate_first_generation(quota, image)

	g = g1


	for i in range(rounds):
		print("Calculating Fitness of Generation")
		g.calculate_fitness(image, LOD)

		print("Displaying best fitness:", end = " ")
		g.print_best_worst()
		g.save_best(str(i), size, run_dir)
		print("Selecting creatures to survive")
		selected_creatures = g.select(quota)
		print(len(selected_creatures))
		print("Generating new generation")
		g = Generation(selected_creatures, mutation_rate, image)
		
	plt.show()

