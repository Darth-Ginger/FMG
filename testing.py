import numpy as np
import matplotlib.pyplot as plt

from Core.noise_ops import *

def map_noise_to_elevation(noise_map: np.ndarray, min_elevation: float, max_elevation: float) -> np.ndarray:
    """
    Maps Perlin noise values to a specified elevation range.

    Args:
        noise_map: 2D numpy array of noise values in the range [-1, 1].
        min_elevation: Minimum elevation value.
        max_elevation: Maximum elevation value.

    Returns:
        2D numpy array with values mapped to the elevation range.
    """
    return min_elevation + ((noise_map + 1) / 2) * (max_elevation - min_elevation)

def display_colored_heightmap(heightmap: np.ndarray, filename: str = "heightmap.png", cmap: str = "terrain"):
    """
    Displays a 2D heightmap with a colormap.

    Args:
        heightmap: 2D numpy array representing elevation values.
        cmap: Colormap to use for the visualization. Default is 'terrain'.
    """
    plt.figure(figsize=(8, 6))
    plt.imshow(heightmap, cmap=cmap)
    plt.colorbar(label="Elevation")  # Add a colorbar to show the elevation scale
    plt.title("Colored Heightmap")
    plt.axis("off")  # Remove axis ticks for better visualization
    # plt.show()
    plt.savefig(filename, bbox_inches="tight")
    plt.close()  # Close the plot to free memory

if __name__ == "__main__":

    # Initialize the noise generator
    generator = NoiseGenerator()

    # Register Perlin noise operation
    generator.register_noise("perlin", Perlin_Noise)

    # Create a sample heightmap
    heightmap = np.random.randint(0, 255, size=(500, 500))

    # Define operations with settings
    operations = [
        {
            "name": "perlin", 
            "settings": 
                {
                    # The scale of the noise. A higher scale will result in larger features in the noise.
                    "scale": 100.0, 
                    # The amplitude of the noise. 
                    # A higher amplitude will result in a greater range of values in the noise.
                    "amplitude": 1.0, 
                    # The number of octaves of the noise. 
                    # A higher number of octaves will result in more detailed noise.
                    "octaves": 8, 
                    # Persistence controls the amplitude of each successive octave. 
                    # When persistence is 1, each octave has the same amplitude. 
                    # When persistence is 0, each octave has an amplitude of 0. 
                    # When persistence is in between, each octave has an amplitude that 
                    #   is proportional to the previous amplitude. 
                    # For example, 
                    #       if persistence is 0.5, 
                    #           the amplitude of the second octave is half of the amplitude 
                    #           of the first octave.
                    "persistence": 0.6 
                }
        },
    ]

    # Execute the transformations
    final_map = generator.execute(heightmap, operations)

    # Access transformation history
    history = generator.get_history()

    print("Transformation History:")
    for i, step in enumerate(history):
        print(f"Step {i}:")
        print(step)
        print()
    # View the final map
    print("Final Map:")
    print(final_map)

    print()
    print()
    print("Mapping to Elevation Range:")
    print(map_noise_to_elevation(final_map, 0, 100))
    

    display_colored_heightmap(map_noise_to_elevation(final_map, 0, 100), cmap="terrain")