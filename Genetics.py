import random




from Creature import Creature



class Generation:
	def __init__(self, seed_creatures: List[Creature], mutation_rate: float = 0.05):
		self.creatures = self._generate_offspring(seed_creatures, mutation_rate)


	@classmethod
	def generate_first_generation(cls, quota:int):
		seed_creatures = []

		for _ in range(quota):
			seed_creatures.append(Creature.generate_random())

		return cls(seed_creatures)



	def _generate_offspring(self, seed_creatures: List[Creature], mutation_rate) -> List[Creature]:
		new_generation = []
		for parent1 in seed_creatures:
			for parent2 in seed_creatures:
				offspring = parent1.generate_offspring(parent2, mutation_rate)
				new_generation.append(offspring)

		for asexual in seed_creatures:
			offspring = asexual.generate_variant(mutation_rate)
			new_generation.append(offspring)


		return new_generation


	def compute_fitness(self, image, LOD: int = 1):
		for creature in self.seed_creatures:
			creature.compute_fitness(image, LOD)


	def select(self, quota: int):
		return random.choices(self.creatures, [e.fitness for e in self.creatures])


if __name__ == "__main__":
	quota = 80
	im = iio.imread('eddy.jpg')
	LOD = 1
	mutation_rate = 0.05



	g1 = Generation.generate_first_generation(quota)
	g1.compute_fitness(image, LOD)

