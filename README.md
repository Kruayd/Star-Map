# 3DStarmapTool

## Introduction and Purposes

This project consists of a Python script which aims to provide an easy to use, portable tool for displaying sci-fi table-top RPG starmaps. The current pre-release version (**0.2.0-alpha**) should be intended as a demo of the general idea behind it, and not as a representation of the final product.

## Setting up

Since the script has been written and tested with `Python 3.7`, running it with the aforementioned Python version is highly recommended but any `Python3` previous or subsequent release should be fine, though I cannot grant anything. `Python2` won't work for sure!!!

### Bash script installation

give execution right with `chmod +x` and then simply run `setup.sh`

### Manual installation

To manually install all the dependecies just use

```
pip install numpy pandas Pillow PyOpenGL PyOpenGL_accelerate regex pygame
```

if your default version is a `Python3` version, otherwise you have to

```
pip3 install numpy pandas Pillow PyOpenGL PyOpenGL_accelerate regex pygame
```

You can also do

```
pythonX.Y -m pip install numpy pandas Pillow PyOpenGL PyOpenGL_accelerate regex pygame
```

in order to install them for the specific `X.Y` Python version.

#### Warnings!!!

If you want to run it with `Python3.8`, substitute `pygame` with `pygame==2.0.0.dev10`

## Running

Simply double-click on `Star_Map.py` if your main version is a `Python3` version or try typing in terminal:

```
python3 /path to/Star_Map.py
```

To run it with any `X.Y` version:

```
pythonX.Y /path to/Star_Map.py
```

## Commands

Use `w`, `a`, `s`, `d`, `r`, `f` and arrow keys to move

## Other info

### Authors

- **Luca Cinnirella** - *creator* - [Kruayd (yep, it's me)](https://github.com/Kruayd)

### License

This project is licensed under the **GNU GPLv3** - see the [LICENSE.md](LICENSE.md) file for details

### Warnings

See the [WARNINGS.md](WARNINGS.md) file for details

### Acknowledgments

- Thanks to [The Cherno](https://www.youtube.com/user/TheChernoProject) for its awesome [OpenGL Crash Course](https://www.youtube.com/watch?v=W3gAzLwfIP0&list=PLlrATfBNZ98foTJPJ_Ev03o2oq3-GGOS2)
- Thanks to [L3viathan](https://stackoverflow.com/users/1016216/l3viathan) for the [Range dictionary class](https://stackoverflow.com/questions/39358092/range-as-dictionary-key-in-python) solution
- Thanks to the [Celestia](https://celestia.space) team for providing open-source [data](https://github.com/CelestiaProject/Celestia/tree/master/data)

### Roadmap

- [x] Adding comments
- [x] Implementing Celestia data reading
- [X] Tweaking stars fragment shader
- [ ] Adding some GUI functions
- [ ] Debugging
- [ ] Official release
