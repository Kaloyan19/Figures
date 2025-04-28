import math
import unittest
from copy import deepcopy
from io import StringIO
from collections import Counter
from unittest.mock import patch, mock_open
import inspect

from Figures.Code.figures import Triangle, Square, Rectangle, Circle, FigureFactory, StreamFigureFactory, main, RandomFigureFactory, AbstractFigureFactory, Figure


class TestTriangle(unittest.TestCase):

    def test_triangle_float(self):
        a, b, c = 3.5, 4.2, 5.1
        triangle = Triangle(a, b, c)
        self.assertEqual(triangle.get_perimeter(), 12.8)

    def test_if_dimensions_are_negative(self):
        a = -1
        b = 5
        c = 3

        with self.assertRaises(ValueError) as ex:
            triangle = Triangle(a, b, c)

        self.assertEqual(str(ex.exception), "a, b, c must be positive and non-zero!")

    def test_if_dimensions_are_too_big(self):
        a = 10000000
        b = 10000000
        c = 90000000

        with self.assertRaises(OverflowError) as ex:
            triangle = Triangle(a, b, c)

        self.assertEqual(str(ex.exception), "Dimensions are too big!")

    def test_if_dimensions_are_zero(self):
        a = 0
        b = 3
        c = 4

        with self.assertRaises(ValueError) as ex:
            triangle = Triangle(a, b, c)

        self.assertEqual(str(ex.exception), "a, b, c must be positive and non-zero!")

    def test_for_inequality_1(self):
        a = 2
        b = 2
        c = 4

        with self.assertRaises(ValueError) as ex:
            triangle = Triangle(a, b, c)

        self.assertEqual(str(ex.exception), 'Triangle inequality is violated!')

    def test_for_inequality_2(self):
        a = 3
        b = 9
        c = 5

        with self.assertRaises(ValueError) as ex:
            triangle = Triangle(a, b, c)

        self.assertEqual(str(ex.exception), 'Triangle inequality is violated!')

    def test_init(self):
        a = 3
        b = 3
        c = 5

        triangle = Triangle(a, b, c)

        self.assertEqual(triangle.a, 3)
        self.assertEqual(triangle.b, 3)
        self.assertEqual(triangle.c, 5)

    def test_get_perimeter_triangle(self):
        a = 3
        b = 3
        c = 5

        triangle = Triangle(a, b, c)

        self.assertEqual(triangle.get_perimeter(), 11)

    def test_if_input_is_int(self):
        a = '3'
        b = '3'
        c = '5'

        with self.assertRaises(TypeError) as ex:
            triangle = Triangle(a, b, c)

        self.assertEqual(str(ex.exception), 'a, b, c must be integers or floats!')

    def test_str_method(self):
        a = 3
        b = 3
        c = 5

        triangle = Triangle(a, b, c)

        self.assertEqual(str(triangle), 'triangle 3 3 5')

    def test_cloning_independence_of_objects(self):
        original = Triangle(3, 4, 5)

        def a_setter(self, value):
            if not isinstance(value, (int, float)):
                raise TypeError("a must be an integer or float!")
            if value <= 0:
                raise ValueError("a must be positive and non-zero!")
            self._Triangle__a = value

        def b_setter(self, value):
            if not isinstance(value, (int, float)):
                raise TypeError("b must be an integer or float!")
            if value <= 0:
                raise ValueError("b must be positive and non-zero!")
            self._Triangle__b = value

        def c_setter(self, value):
            if not isinstance(value, (int, float)):
                raise TypeError("c must be an integer or float!")
            if value <= 0:
                raise ValueError("c must be positive and non-zero!")
            self._Triangle__c = value

        Triangle.a = Triangle.a.setter(a_setter)
        Triangle.b = Triangle.b.setter(b_setter)
        Triangle.c = Triangle.c.setter(c_setter)

        clone = deepcopy(original)
        clone.a = 6
        clone.b = 8
        clone.c = 10
        self.assertNotEqual(original.a, clone.a)
        self.assertNotEqual(original.b, clone.b)
        self.assertNotEqual(original.c, clone.c)

        del Triangle.a
        del Triangle.b
        del Triangle.c

    def test_cloning_preservation_of_state(self):
        original = Triangle(3, 4, 5)
        clone = deepcopy(original)

        self.assertEqual(original.a, clone.a)
        self.assertEqual(original.b, clone.b)
        self.assertEqual(original.c, clone.c)
        self.assertEqual(str(original), str(clone))

class TestSquare(unittest.TestCase):
    def test_square_float(self):
        a = 3.5
        square = Square(a)
        self.assertEqual(square.get_perimeter(), 14.0)

    def test_if_a_is_int(self):
        a = '3'

        with self.assertRaises(TypeError) as ex:
            square = Square(a)

        self.assertEqual(str(ex.exception), 'a must be an integer or float!')

    def test_if_a_is_negative(self):
        a = -1

        with self.assertRaises(ValueError) as ex:
            square = Square(a)

        self.assertEqual(str(ex.exception), 'a must be positive and non-zero!')

    def test_if_a_is_zero(self):
        a = 0

        with self.assertRaises(ValueError) as ex:
            square = Square(a)

        self.assertEqual(str(ex.exception), 'a must be positive and non-zero!')

    def test_if_a_is_too_big(self):
        a = 30000000

        with self.assertRaises(OverflowError) as ex:
            square = Square(a)

        self.assertEqual(str(ex.exception), 'Dimensions are too big!')

    def test_init(self):
        a = 3

        square = Square(a)

        self.assertEqual(square.a, 3)

    def test_get_perimeter_square(self):
        a = 3

        square = Square(a)

        self.assertEqual(square.get_perimeter(), 12)

    def test_str_method(self):
        a = 3

        square = Square(a)

        self.assertEqual(str(square), 'square 3')

    def test_cloning_independence_of_objects(self):
        original = Square(3)

        def a_setter(self, value):
            if not isinstance(value, (int, float)):
                raise TypeError("a must be an integer or float!")
            if value <= 0:
                raise ValueError("a must be positive and non-zero!")
            if math.pi * value > 10 ** 8:
                raise OverflowError('Dimensions are too big!')
            self.Square__a = value

            Square.a = Square.a.setter(a_setter)

            clone = deepcopy(original)
            clone.a = 4
            self.assertNotEqual(original.a, clone.a)

            del Square.a

    def test_cloning_preservation_of_state(self):
        original = Square(3)
        clone = deepcopy(original)

        self.assertEqual(original.a, clone.a)
        self.assertEqual(str(original.a), str(clone.a))

class TestRectangle(unittest.TestCase):
    def test_rectangle_float(self):
        a, b = 3.5, 4.8
        rectangle = Rectangle(a, b)
        self.assertEqual(rectangle.get_perimeter(), 16.6)

    def test_if_dimensions_are_int(self):
        a = '3'
        b = '4'

        with self.assertRaises(TypeError) as ex:
            rectangle = Rectangle(a, b)

        self.assertEqual(str(ex.exception), 'a, b must be integers or floats!')

    def test_if_dimensions_are_negative(self):
        a = -2
        b = -3

        with self.assertRaises(ValueError) as ex:
            rectangle = Rectangle(a, b)

        self.assertEqual(str(ex.exception), 'a, b must be positive and non-zero!')

    def test_if_dimensions_are_zero(self):
        a = 0
        b = 0

        with self.assertRaises(ValueError) as ex:
            rectangle = Rectangle(a, b)

        self.assertEqual(str(ex.exception), 'a, b must be positive and non-zero!')

    def test_if_dimensions_are_too_big(self):
        a = 30000000
        b = 25000000

        with self.assertRaises(OverflowError) as ex:
            rectangle = Rectangle(a, b)

        self.assertEqual(str(ex.exception), 'Dimensions are too big!')

    def test_init(self):
        a = 3
        b = 4

        rectangle = Rectangle(a, b)

        self.assertEqual(rectangle.a, 3)
        self.assertEqual(rectangle.b, 4)

    def test_get_perimeter_rectangle(self):
        a = 3
        b = 4

        rectangle = Rectangle(a, b)

        self.assertEqual(rectangle.get_perimeter(), 14)

    def test_str_method(self):
        a = 3
        b = 4

        rectangle = Rectangle(a, b)

        self.assertEqual(str(rectangle), 'rectangle 3 4')

    def test_cloning_independence_of_objects(self):
        original = Rectangle(5, 7)

        def a_setter(self, value):
            if not isinstance(value, (int, float)):
                raise TypeError("a must be an integer or float!")
            if value <= 0:
                raise ValueError("a must be positive and non-zero!")
            self._Rectangle__a = value

        def b_setter(self, value):
            if not isinstance(value, (int, float)):
                raise TypeError("b must be an integer or float!")
            if value <= 0:
                raise ValueError("b must be positive and non-zero!")
            self._Rectangle__b = value

        Rectangle.a = Rectangle.a.setter(a_setter)
        Rectangle.b = Rectangle.b.setter(b_setter)

        clone = deepcopy(original)
        clone.a = 10
        clone.b = 14
        self.assertNotEqual(original.a, clone.a)
        self.assertNotEqual(original.b, clone.b)

        del Rectangle.a
        del Rectangle.b

    def test_cloning_preservation_of_state(self):
        original = Rectangle(5, 7)
        clone = deepcopy(original)

        self.assertEqual(original.a, clone.a)
        self.assertEqual(original.b, clone.b)
        self.assertEqual(str(original), str(clone))

class TestCircle(unittest.TestCase):
    def test_circle_float(self):
        radius = 3.7
        circle = Circle(radius)
        self.assertAlmostEqual(circle.get_perimeter(), 23.25, places=2)

    def test_if_dimensions_are_int(self):
        radius = '3'

        with self.assertRaises(TypeError) as ex:
            circle = Circle(radius)

        self.assertEqual(str(ex.exception), 'Radius must be an integer or float!')

    def test_if_dimensions_are_negative(self):
        radius = -2

        with self.assertRaises(ValueError) as ex:
            circle = Circle(radius)

        self.assertEqual(str(ex.exception), 'Radius must be positive and non-zero!')

    def test_if_dimensions_are_zero(self):
        radius = 0

        with self.assertRaises(ValueError) as ex:
            circle = Circle(radius)

        self.assertEqual(str(ex.exception), 'Radius must be positive and non-zero!')

    def test_if_dimensions_are_too_big(self):
        radius = 35000000

        with self.assertRaises(OverflowError) as ex:
            circle = Circle(radius)

        self.assertEqual(str(ex.exception), 'Radius is too big!')

    def test_init(self):
        radius = 3

        circle = Circle(radius)

        self.assertEqual(circle.radius, 3)

    def test_get_perimeter_circle(self):
        radius = 3

        circle = Circle(radius)

        self.assertEqual(circle.get_perimeter(), 18.85)

    def test_str_method(self):
        radius = 3

        circle = Circle(radius)

        self.assertEqual(str(circle), 'circle 3')

    def test_cloning_independence_of_objects(self):
        original = Circle(5)

        def radius_setter(self, value):
            if not isinstance(value, (int, float)):
                raise TypeError("Radius must be an integer or float!")
            if value <= 0:
                raise ValueError("Radius must be positive and non-zero!")
            if math.pi * value > 10 ** 8:
                raise OverflowError('Radius is too big!')
            self._Circle__radius = value

        Circle.radius = Circle.radius.setter(radius_setter)

        clone = deepcopy(original)
        clone.radius = 4
        self.assertNotEqual(original.radius, clone.radius)

        del Circle.radius

    def test_cloning_preservation_of_state(self):
        original = Circle(5)
        clone = deepcopy(original)
        self.assertEqual(original.radius, clone.radius)
        self.assertEqual(str(original), str(clone))

class TestFigureFactory(unittest.TestCase):
    def test_create_triangle(self):
        figure = FigureFactory.create_figure("Triangle 3 4 5")
        self.assertIsInstance(figure, Triangle)
        self.assertEqual(figure.a, 3)
        self.assertEqual(figure.b, 4)
        self.assertEqual(figure.c, 5)

    def test_create_square(self):
        figure = FigureFactory.create_figure("Square 4")
        self.assertIsInstance(figure, Square)
        self.assertEqual(figure.a, 4)

    def test_create_rectangle(self):
        figure = FigureFactory.create_figure("Rectangle 5 6")
        self.assertIsInstance(figure, Rectangle)
        self.assertEqual(figure.a, 5)
        self.assertEqual(figure.b, 6)

    def test_create_circle(self):
        figure = FigureFactory.create_figure("Circle 7")
        self.assertIsInstance(figure, Circle)
        self.assertEqual(figure.radius, 7)

    def test_invalid_figure_type(self):
        with self.assertRaises(ValueError) as ex:
            FigureFactory.create_figure("Gosho 15")
        self.assertEqual(str(ex.exception), "Unknown figure type or incorrect number of parameters: gosho")

    def test_invalid_dimensions(self):
        with self.assertRaises(ValueError):
            FigureFactory.create_figure("Triangle 3 4")

    def test_if_dimensions_are_negative(self):
        with self.assertRaises(ValueError) as ex:
            FigureFactory.create_figure("Triangle -3 4 5")
        self.assertEqual(str(ex.exception), "a, b, c must be positive and non-zero!")

    def test_if_dimensions_are_ill_formed(self):
        with self.assertRaises(ValueError) as ex:
            FigureFactory.create_figure("Triangle 3 abc -5")
        self.assertEqual(str(ex.exception), "could not convert string to float: 'abc'")

class TestInputAndOutputMethods(unittest.TestCase):
    def test_empty_file_raises_error(self):
        with open("empty_figures.txt", "w") as empty_file:
            pass

        try:
            with open("empty_figures.txt", "r") as file_stream:
                factory = StreamFigureFactory(file_stream, input_mode="file")
                factory.create_figure()
        except ValueError as e:
            self.assertEqual(str(e), "No input provided in file!")

    def test_empty_stdin_raises_error(self):
        empty_stdin = StringIO("")
        factory = StreamFigureFactory(empty_stdin, input_mode="stdin")
        with self.assertRaises(ValueError) as e:
            factory.create_figure()
        self.assertEqual(str(e.exception), "No input provided in STDIN!")

    def test_valid_file_input(self):
        file_path = "fig.txt"

        try:
            with open(file_path, 'r') as file_stream:
                factory = StreamFigureFactory(file_stream, input_mode="file")
                results = []
                while True:
                    figure = factory.create_figure()
                    if figure is None:
                        break
                    results.append(str(figure))
        except FileNotFoundError:
            self.fail(f"File not found: {file_path}")
        except ValueError as e:
            self.fail(f"Unexpected ValueError: {e}")

        self.assertEqual(results, ["circle 5.0"])

    def test_valid_stdin_input(self):
        stdin_content = "triangle 3 4 5\ncircle 7\nsquare 4\nrectangle 8 5\nexit\n"
        stdin_stream = StringIO(stdin_content)
        factory = StreamFigureFactory(stdin_stream, input_mode="stdin")
        results = []
        while True:
            figure = factory.create_figure()
            if figure == "exit" or figure is None:
                break
            results.append(str(figure))
        self.assertEqual(results, ["triangle 3.0 4.0 5.0", "circle 7.0", "square 4.0", "rectangle 8.0 5.0"])

class TestRandom(unittest.TestCase):
    def test_for_overflow(self):
        num_figures = 1001
        random_figure_factory = RandomFigureFactory()

        with self.assertRaises(OverflowError) as ex:
            random_figure_factory = random_figure_factory.create_random_figures(num_figures)

        self.assertEqual(str(ex.exception), "The number of figures cannot be greater than 1000!")

    def test_negative_number_raises_error(self):
        with self.assertRaises(ValueError) as e:
            random_figure_factory = RandomFigureFactory()
            num_figures = -5
            if num_figures <= 0:
                raise ValueError("The number of figures must be a positive integer greater than zero!")
        self.assertEqual(str(e.exception), "The number of figures must be a positive integer greater than zero!")

    def test_zero_raises_error(self):
        with self.assertRaises(ValueError) as e:
            random_figure_factory = RandomFigureFactory()
            num_figures = 0
            if num_figures <= 0:
                raise ValueError("The number of figures must be a positive integer greater than zero!")
        self.assertEqual(str(e.exception), "The number of figures must be a positive integer greater than zero!")

    def test_random_figures_range(self):
        random_figure_factory = RandomFigureFactory()
        num_figures = 696
        figures = random_figure_factory.create_random_figures(num_figures)

        for figure in figures:
            if isinstance(figure, Triangle):
                self.assertGreaterEqual(figure.a, 1)
                self.assertGreaterEqual(figure.b, 1)
                self.assertGreaterEqual(figure.c, 1)
                self.assertLessEqual(figure.a, 2000)
                self.assertLessEqual(figure.b, 2000)
                self.assertLessEqual(figure.c, 2000)
                self.assertTrue(figure.a + figure.b > figure.c)
                self.assertTrue(figure.a + figure.c > figure.b)
                self.assertTrue(figure.b + figure.c > figure.a)
            elif isinstance(figure, Square):
                self.assertGreaterEqual(figure.a, 1)
                self.assertLessEqual(figure.a, 2000)
            elif isinstance(figure, Rectangle):
                self.assertGreaterEqual(figure.a, 1)
                self.assertGreaterEqual(figure.b, 1)
                self.assertLessEqual(figure.a, 2000)
                self.assertLessEqual(figure.b, 2000)
            elif isinstance(figure, Circle):
                self.assertGreaterEqual(figure.radius, 1)
                self.assertLessEqual(figure.radius, 2000)

    def test_random_figures_distribution(self):
        random_figure_factory = RandomFigureFactory()
        num_figures = 999
        figures = random_figure_factory.create_random_figures(num_figures)

        counts = Counter(type(figure).__name__ for figure in figures)

        print("Figure distribution:", counts)

        self.assertIn('Triangle', counts)
        self.assertIn('Square', counts)
        self.assertIn('Rectangle', counts)
        self.assertIn('Circle', counts)

        expected_count = num_figures / 4
        tolerance = 0.1 * expected_count
        for figure_type in ['Triangle', 'Square', 'Rectangle', 'Circle']:
            self.assertAlmostEqual(counts[figure_type], expected_count, delta=tolerance)

class TestAbstractFigureFactory(unittest.TestCase):

    def test_file_factory_creation(self):
        with patch("builtins.input", return_value="test_file.txt"):
            with patch("builtins.open", mock_open(read_data="triangle 3 4 5")):
                factory = AbstractFigureFactory.get_factory("file")
                self.assertIsInstance(factory, StreamFigureFactory)

    def test_stdin_factory_creation(self):
        with patch("sys.stdin", new_callable=lambda: StringIO("circle 5")):
            factory = AbstractFigureFactory.get_factory("stdin")
            self.assertIsInstance(factory, StreamFigureFactory)

    def test_random_factory_creation(self):
        factory = AbstractFigureFactory.get_factory("random")
        self.assertIsInstance(factory, RandomFigureFactory)

    def test_invalid_input_type(self):
        with self.assertRaises(ValueError) as context:
            AbstractFigureFactory.get_factory("unsupported")
        self.assertEqual(str(context.exception), "Invalid input type: unsupported")

    def test_empty_input_type(self):
        with self.assertRaises(ValueError) as context:
            AbstractFigureFactory.get_factory("")
        self.assertEqual(str(context.exception), "Invalid input type: ")

    def test_integer_input_type(self):
        with self.assertRaises(ValueError) as context:
            AbstractFigureFactory.get_factory(123)
        self.assertEqual(str(context.exception), "Invalid input type: 123")

    def test_file_not_found(self):
        with patch("builtins.input", return_value="invalid_path.txt"):
            factory = AbstractFigureFactory.get_factory("file")
            self.assertIsNone(factory)

class TestReflection(unittest.TestCase):
    def test_valid_triangle_creation(self):
        factory = FigureFactory()
        triangle = factory.create_figure("triangle 3 4 5")
        self.assertIsInstance(triangle, Triangle)
        self.assertEqual(triangle.a, 3)
        self.assertEqual(triangle.b, 4)
        self.assertEqual(triangle.c, 5)

    def test_invalid_figure_type(self):
        factory = FigureFactory()
        with self.assertRaises(ValueError) as context:
            factory.create_figure("pentagon 10")
        self.assertEqual(str(context.exception), "Unknown or invalid figure type: Pentagon")

    def test_invalid_parameters(self):
        factory = FigureFactory()
        with self.assertRaises(ValueError) as context:
            factory.create_figure("triangle 3")
        self.assertIn("Incorrect parameters", str(context.exception))

    def test_triangle_constraint_violation(self):
        factory = FigureFactory()
        with self.assertRaises(ValueError) as context:
            factory.create_figure("triangle 1 2 10")
        self.assertEqual(str(context.exception), "Triangle inequality is violated!")

    def test_random_creation(self):
        factory = RandomFigureFactory()
        figures = factory.create_random_figures(5)
        self.assertEqual(len(figures), 5)

        for figure in figures:
            self.assertTrue(isinstance(figure, Figure),f"Object {figure} is not a subclass of Figure")

    def test_triangle_random_creation(self):
        factory = RandomFigureFactory()
        triangles = [factory._create_random_triangle() for _ in range(5)]

        for triangle in triangles:
            self.assertIsInstance(triangle, Triangle)
            self.assertTrue(triangle.a + triangle.b > triangle.c and triangle.a + triangle.c > triangle.b and triangle.b + triangle.c > triangle.a,"Triangle inequality violated")

    def test_file_input(self):
        with patch("builtins.input", return_value="test_file.txt"):
            with patch("builtins.open", mock_open(read_data="triangle 3 4 5\ncircle 10")):
                factory = AbstractFigureFactory.get_factory("file")
                self.assertIsInstance(factory, StreamFigureFactory)

                figures = []
                while True:
                    figure = factory.create_figure()
                    if not figure:
                        break
                    figures.append(figure)

                self.assertEqual(len(figures), 2)
                self.assertIsInstance(figures[0], Triangle)
                self.assertIsInstance(figures[1], Circle)

    def test_stdin_input(self):
        mock_stdin = StringIO("square 20\nexit")
        with patch("sys.stdin", mock_stdin):
            factory = AbstractFigureFactory.get_factory("stdin")
            self.assertIsInstance(factory, StreamFigureFactory)

            figures = []
            while True:
                figure = factory.create_figure()
                if not figure:
                    break
                figures.append(figure)

            self.assertEqual(len(figures), 1)
            self.assertIsInstance(figures[0], Square)

    def test_random_input(self):
        factory = AbstractFigureFactory.get_factory("random")
        self.assertIsInstance(factory, RandomFigureFactory)

        figures = factory.create_random_figures(5)
        self.assertEqual(len(figures), 5)
        for figure in figures:
            self.assertIsInstance(figure, Figure)