import math, sys, random
from abc import ABC, abstractmethod
from copy import deepcopy
import inspect


class Figure(ABC):
    @abstractmethod
    def get_perimeter(self):
        pass

    def __str__(self):
        pass

class Prototype(ABC):
    @abstractmethod
    def clone(self):
        pass

class AbstractFigureFactory:
    @staticmethod
    def get_factory(input_type):
        if input_type == "file":
            file_path = input("Enter the file path: ").strip()
            try:
                file_stream = open(file_path, "r")
                return StreamFigureFactory(file_stream, input_mode="file")
            except FileNotFoundError:
                print("File not found!")
                return None
        elif input_type == "stdin":
            print("Enter the figure descriptions line by line (example: circle 5). Type 'exit' to quit.")
            return StreamFigureFactory(sys.stdin, input_mode="stdin")
        elif input_type == "random":
            return RandomFigureFactory()
        else:
            raise ValueError(f"Invalid input type: {input_type}")

class FigureFactory:
    @staticmethod
    def create_figure(figure_str):
        parts = figure_str.split()
        if len(parts) < 2:
            raise ValueError('Invalid input format!')

        figure_type = parts[0].capitalize()
        dimensions = list(map(float, parts[1:]))

        figure_class = globals().get(figure_type)

        if not figure_class or not issubclass(figure_class, Figure):
            raise ValueError(f'Unknown or invalid figure type: {figure_type}')

        try:
            return figure_class(*dimensions)
        except TypeError as e:
            raise ValueError(f'Incorrect parameters for {figure_type}: {dimensions}') from e

class RandomFigureFactory:
    def create_random_figures(self, num_figures):
        if num_figures <= 0:
            raise ValueError('The number of figures must be positive!')
        if num_figures > 1000:
            raise OverflowError('The number of figures cannot be greater than 1000!')

        figure_classes = [
            cls for cls in globals().values()
            if inspect.isclass(cls) and issubclass(cls, Figure) and cls != Figure
        ]

        figures = []
        for _ in range(num_figures):
            figure_class = random.choice(figure_classes)

            if figure_class.__name__.lower() == "triangle":
                figures.append(self._create_random_triangle())
                continue

            constructor = inspect.signature(figure_class.__init__)
            param_count = len([
                param for param in constructor.parameters.values() if param.name != "self"
            ])

            random_params = [round(random.uniform(1, 2000), 2) for _ in range(param_count)]
            try:
                figures.append(figure_class(*random_params))
            except TypeError as e:
                raise ValueError(f"Could not create figure: {figure_class.__name__} with parameters {random_params}") from e

        return figures

    @staticmethod
    def _create_random_triangle():
        while True:
            a = round(random.uniform(1, 100), 2)
            b = round(random.uniform(1, 100), 2)
            c = round(random.uniform(1, 100), 2)
            if a + b > c and a + c > b and b + c > a:
                return Triangle(a, b, c)

class StreamFigureFactory:
    def __init__(self, stream, input_mode):
        self.stream = stream
        self.figure_factory = FigureFactory()
        self.input_mode = input_mode
        self.figure_count = 0
        self.max_figures = 1000 if input_mode == "stdin" else 10000
        self.first_line_processed = False

    def create_figure(self):
        if self.figure_count >= self.max_figures:
            raise OverflowError(f'The number of figures exceeded the maximum of {self.max_figures}')

        line = self.stream.readline().strip()

        if not self.first_line_processed:
            self.first_line_processed = True
            if not line:
                if self.input_mode == "file":
                    raise ValueError("No input provided in file!")
                elif self.input_mode == "stdin":
                    raise ValueError("No input provided in STDIN!")

        if not line:
            return None

        if line.lower() == 'exit':
            if self.input_mode == "file":
                raise ValueError("Invalid input in file: there should not be 'exit' in file!")
            elif self.input_mode == "stdin":
                print("Exiting program.")
                return None

        self.figure_count += 1

        return self.figure_factory.create_figure(line)


def main():
    print("Choose the input method you prefer:")
    print("1. Read from a file")
    print("2. Read from STDIN")
    print("3. Generate random figures")

    choice = input("Enter choice (1/2/3): ").strip()

    input_type = None
    if choice == "1":
        input_type = "file"
    elif choice == "2":
        input_type = "stdin"
    elif choice == "3":
        input_type = "random"
    else:
        print("Invalid choice!")
        return

    try:
        factory = AbstractFigureFactory.get_factory(input_type)
        if factory is None:
            return

        if input_type == "random":
            num_figures = int(input("Enter the number of random figures to create (max: 1000): ").strip())
            figures = factory.create_random_figures(num_figures)
            for figure in figures:
                print(f"Created random figure: {figure}")
        else:
            results = []
            while True:
                try:
                    figure = factory.create_figure()
                    if figure is None:
                        break
                    results.append(str(figure))
                except OverflowError as e:
                    print(f"Error: {e}")
                    break
                except ValueError as e:
                    print(f"Error: {e}")
                    break

            if input_type == "file" and not results:
                print("No input provided in file!")
            for result in results:
                print(f"Created figure: {result}")
    except ValueError as e:
        print(f"Error: {e}")

class Triangle(Figure, Prototype):
    __slots__ = ('__a', '__b', '__c')

    def __init__(self, a, b, c):
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)) or not isinstance(c, (int, float)):
            raise TypeError('a, b, c must be integers or floats!')
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError('a, b, c must be positive and non-zero!')
        if a + b + c > (10 ** 8):
            raise OverflowError('Dimensions are too big!')
        if not (a + b > c and a + c > b and b + c > a):
            raise ValueError('Triangle inequality is violated!')

        self.__a = a
        self.__b = b
        self.__c = c

    @property
    def a(self):
        return self.__a

    @property
    def b(self):
        return self.__b

    @property
    def c(self):
        return self.__c

    def get_perimeter(self):
        return self.__a + self.__b + self.__c

    def __str__(self):
        return f'triangle {self.__a} {self.__b} {self.__c}'

    def clone(self):
        return deepcopy(self)

class Square(Figure, Prototype):
    __slots__ = ('__a',)

    def __init__(self, a):
        if not isinstance(a, (int, float)):
            raise TypeError('a must be an integer or float!')
        if a <= 0:
            raise ValueError('a must be positive and non-zero!')
        if 4 * a > (10 ** 8):
            raise OverflowError('Dimensions are too big!')

        self.__a = a

    @property
    def a(self):
        return self.__a

    def get_perimeter(self):
        return 4 * self.__a

    def __str__(self):
        return f'square {self.__a}'

    def clone(self):
        return deepcopy(self)


class Rectangle(Figure, Prototype):
    __slots__ = ('__a', '__b')

    def __init__(self, a, b):
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError('a, b must be integers or floats!')
        if a <= 0 or b <= 0:
            raise ValueError('a, b must be positive and non-zero!')
        if 2 * (a + b) > (10 ** 8):
            raise OverflowError('Dimensions are too big!')

        self.__a = a
        self.__b = b

    @property
    def a(self):
        return self.__a

    @property
    def b(self):
        return self.__b

    def get_perimeter(self):
        return 2 * (self.__a + self.__b)

    def __str__(self):
        return f'rectangle {self.__a} {self.__b}'

    def clone(self):
        return deepcopy(self)

class Circle(Figure, Prototype):
    __slots__ = ('__radius',)

    def __init__(self, radius):
        if not isinstance(radius, (int, float)):
            raise TypeError('Radius must be an integer or float!')
        if radius <= 0:
            raise ValueError('Radius must be positive and non-zero!')
        if math.pi * radius > (10 ** 8):
            raise OverflowError('Radius is too big!')

        self.__radius = radius

    @property
    def radius(self):
        return self.__radius

    def get_perimeter(self):
        perimeter = 2 * math.pi * self.__radius
        return round(perimeter, 2)

    def __str__(self):
        return f'circle {self.__radius}'

    def clone(self):
        return deepcopy(self)

if __name__ == "__main__":
    main()
