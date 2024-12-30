# from classes.biome import Biome, BiomeData, BiomeMatrix
# from data_models.enums import BiomeType
import unittest

# Test Biome class
class TestBiome(unittest.TestCase):
    def test_biome_initialization(self):
        biome = Biome(
            id=1,
            name="Test Biome",
            type=BiomeType.BASIC,
            color="#FFFFFF",
            cost=10,
            habitability=50,
            max_temp=20,
            min_temp=-20,
            max_moisture=100,
            min_moisture=0,
            icons={"grass": 1},
            options=None
        )

        self.assertEqual(biome.id, 1)
        self.assertEqual(biome.name, "Test Biome")
        self.assertEqual(biome.type, BiomeType.BASIC)
        self.assertEqual(biome.color, "#FFFFFF")
        self.assertEqual(biome.cost, 10)
        self.assertEqual(biome.habitability, 50)
        self.assertEqual(biome.temp_range, (-20, 20))
        self.assertEqual(biome.moisture_range, (0, 100))
        self.assertEqual(biome.icons, {"grass": 1})
        self.assertEqual(biome.avg_temp, 0)
        self.assertEqual(biome.avg_moisture, 50)


# Test BiomeMatrix class
class TestBiomeMatrix(unittest.TestCase):
    def test_biome_matrix_initialization(self):
        matrix = BiomeMatrix(rows=10, columns=10)

        self.assertEqual(matrix.rows, 10)
        self.assertEqual(matrix.columns, 10)
        self.assertEqual(matrix.matrix, [[None] * 10 for _ in range(10)])
        self.assertEqual(matrix.temp_range, (float('inf'), float('-inf')))
        self.assertEqual(matrix.moisture_range, (float('inf'), float('-inf')))


    def test_biome_matrix_add_and_get(self):
        matrix = BiomeMatrix(rows=10, columns=10)
        matrix.add_biome("Test Biome", (-20, 20), (0, 100))
        biome_name = matrix.get_biome(0, 50)

        self.assertEqual(biome_name, "Test Biome")


# Test BiomeData class
class TestBiomeData(unittest.TestCase):
    def test_biome_data_initialization(self):
        biome_data = BiomeData()

        self.assertEqual(biome_data.temp_range, (0, 0))
        self.assertEqual(biome_data.moisture_range, (0, 0))
        self.assertIsInstance(biome_data.matrix, BiomeMatrix)


    def test_biome_data_add_and_access(self):
        biome_data = BiomeData()
        biome = Biome(
            id=1,
            name="Test Biome",
            type=BiomeType.BASIC,
            color="#FFFFFF",
            cost=10,
            habitability=50,
            max_temp=20,
            min_temp=-20,
            max_moisture=100,
            min_moisture=0,
            icons={"grass": 1},
            options=None
        )
        biome_data.add_biome(biome)

        self.assertEqual(biome_data["Test Biome"], biome)

if __name__ == "__main__":
    import sys, os
    sys.path.append(os.getcwd())
    
    from data_models.biome import Biome, BiomeData, BiomeMatrix
    from data_models.enums import BiomeType
    
    biome_data = BiomeData()
    biome_data.load_from_json("config_data/biome_data.json")
    
    # print(f"BiomeData: {biome_data}")
    # print(biome_data["Test Biome"])
    # print(biome_data.matrix)
    print(biome_data.display_matrix_indexes())
    print()
    print(biome_data.display_matrix())
    