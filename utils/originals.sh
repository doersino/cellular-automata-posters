# Generate the posters (or at least close approximations) from the original
# Imgur album posted by /u/collatz_conjecture (see `README.md` for a link).
# Run this script from the root directory of the repository.

CAP_RULE=30  CAP_INITIALCONDITION='random' CAP_COLORSCHEME='yellow'   CAP_WIDTH=250 CAP_CELLSHAPE='circle'               python3 cap.py
CAP_RULE=90  CAP_INITIALCONDITION='middle' CAP_COLORSCHEME='green'    CAP_WIDTH=400 CAP_CELLSHAPE='circle' CAP_OFFSET=64 python3 cap.py
CAP_RULE=105 CAP_INITIALCONDITION='middle' CAP_COLORSCHEME='pink'     CAP_WIDTH=200 CAP_CELLSHAPE='circle'               python3 cap.py
CAP_RULE=110 CAP_INITIALCONDITION='random' CAP_COLORSCHEME='salmon'   CAP_WIDTH=340 CAP_CELLSHAPE='circle'               python3 cap.py
CAP_RULE=153 CAP_INITIALCONDITION='random' CAP_COLORSCHEME='red'      CAP_WIDTH=300 CAP_CELLSHAPE='circle'               python3 cap.py
CAP_RULE=57  CAP_INITIALCONDITION='middle' CAP_COLORSCHEME='blue'     CAP_WIDTH=270 CAP_CELLSHAPE='circle'               python3 cap.py
CAP_RULE=73  CAP_INITIALCONDITION='random' CAP_COLORSCHEME='lime'     CAP_WIDTH=260 CAP_CELLSHAPE='circle' CAP_OFFSET=50 python3 cap.py
CAP_RULE=73  CAP_INITIALCONDITION='middle' CAP_COLORSCHEME='orange'   CAP_WIDTH=310 CAP_CELLSHAPE='circle'               python3 cap.py
CAP_RULE=90  CAP_INITIALCONDITION='random' CAP_COLORSCHEME='darkblue' CAP_WIDTH=600 CAP_CELLSHAPE='circle' CAP_OFFSET=20 python3 cap.py
CAP_RULE=106 CAP_INITIALCONDITION='random' CAP_COLORSCHEME='violet'   CAP_WIDTH=270 CAP_CELLSHAPE='circle' CAP_OFFSET=20 python3 cap.py
