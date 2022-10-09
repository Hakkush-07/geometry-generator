# Geometry Generator

This project is largely inspired by [GeoGen](https://github.com/PatrikBak/GeoGen)

`python main.py` creates a folder containing an `asymptote` figure of a randomly created configuration consisting of points, lines, circles by constantly adding new objects, a `tex` description file, and a `tex` file of unknown properties of the configuration in `outputs` folder.

Compile `asy` and `tex` files. (For `latexmk`, a `latexmkrc` file is also included in the output folder, use `latexmk -aux-directory=auxs -pdf` to compile)

In case of an `AssertionError`, try running again. This means that figure is too big etc.