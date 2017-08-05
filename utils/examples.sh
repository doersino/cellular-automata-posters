# Generate the example image embedded in `README.md`. Make sure you've got the
# pdf2svg utility installed, fill in your Wolfram|Alpha AppID below, then run
# this script from the root directory of the repository. The end result (apart
# from the PDFs and SVGs) will be a file `example.html` which you can open in
# your browser, zoom in a bit and take a screenshot.

WAAID=''

CAP_RULE=30      CAP_INITIALCONDITION='random' CAP_COLORSCHEME='yellow'   CAP_WIDTH=290 CAP_GRIDMODE='None'                                    CAP_PAGEWIDTH=1350 CAP_PAGEHEIGHT=650  python3 cap.py  # _
CAP_RULE=57      CAP_INITIALCONDITION='middle' CAP_COLORSCHEME='blue'     CAP_WIDTH=199 CAP_CELLSHAPE='circle' CAP_WOLFRAMALPHAAPPID="$WAAID"  CAP_PAGEWIDTH=650  CAP_PAGEHEIGHT=650  python3 cap.py  # .
CAP_RULE=73      CAP_INITIALCONDITION='random' CAP_COLORSCHEME='lime'     CAP_WIDTH=130 CAP_GRIDMODE='living' CAP_OFFSET=40 CAP_ANGLE=-8       CAP_PAGEWIDTH=650  CAP_PAGEHEIGHT=650  python3 cap.py  # .
CAP_RULE=90      CAP_INITIALCONDITION='middle' CAP_COLORSCHEME='green'    CAP_WIDTH=160 CAP_WOLFRAMALPHAAPPID="$WAAID"                         CAP_PAGEWIDTH=650  CAP_PAGEHEIGHT=1000 python3 cap.py  # n
CAP_RULE=105     CAP_INITIALCONDITION='middle' CAP_COLORSCHEME='pink'     CAP_WIDTH=141 CAP_GRIDMODE='None' CAP_ANGLE=8                        CAP_PAGEWIDTH=650  CAP_PAGEHEIGHT=650  python3 cap.py  # .
CAP_RULE=106     CAP_INITIALCONDITION='random' CAP_COLORSCHEME='violet'   CAP_WIDTH=180 CAP_GRIDMODE='None' CAP_OFFSET=20                      CAP_PAGEWIDTH=650  CAP_PAGEHEIGHT=2050 python3 cap.py  # |
CAP_RULE=110     CAP_INITIALCONDITION='random' CAP_COLORSCHEME='salmon'   CAP_WIDTH=200 CAP_CELLSHAPE='circle' CAP_SHOWLABEL='False'           CAP_PAGEWIDTH=1350 CAP_PAGEHEIGHT=650  python3 cap.py  # _
CAP_RULE=838020  CAP_INITIALCONDITION='random' CAP_COLORSCHEME='gray'     CAP_WIDTH=150 CAP_CELLSHAPE='circle' CAP_OFFSET=20                   CAP_PAGEWIDTH=650  CAP_PAGEHEIGHT=1000 python3 cap.py  # n
CAP_RULE=1738243 CAP_INITIALCONDITION='random' CAP_COLORSCHEME='darkblue' CAP_WIDTH=250 CAP_CELLSHAPE='square'                                 CAP_PAGEWIDTH=1350 CAP_PAGEHEIGHT=650  python3 cap.py  # _

pdf2svg rule30.pdf rule30.svg
pdf2svg rule57.pdf rule57.svg
pdf2svg rule73.pdf rule73.svg
pdf2svg rule90.pdf rule90.svg
pdf2svg rule105.pdf rule105.svg
pdf2svg rule106.pdf rule106.svg
pdf2svg rule110.pdf rule110.svg
pdf2svg rule838020.pdf rule838020.svg
pdf2svg rule1738243.pdf rule1738243.svg

cat <<EOF > examples.html
<style>
    * {
        font-size: 0;
        margin: 0;
        padding: 0;
        line-height: 0;
        vertical-align: top;
        border-collapse: collapse;
    }
    img {
        padding-right: 5px;
        padding-bottom: 5px;
    }
</style>

<table>
<thead>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
</thead>
<tbody>
    <tr>
        <td rowspan="3" width="70px">
            <img src="rule106.svg" width="65px" height="205px">
        </td>
        <td width="70px">
            <img src="rule57.svg" width="65px" height="65px">
        </td>
        <td colspan="2" width="140px">
            <img src="rule30.svg" width="135px" height="65px">
        </td>
        <td rowspan="3">
            <img src="rule838020.svg" width="65px" height="100px">
            <br>
            <img src="rule90.svg" width="65px" height="100px">
        </td>
    </tr>
    <tr>
        <td colspan="2" width="140px">
            <img src="rule110.svg" width="135px" height="65px">
        </td>
        <td width="70px">
            <img src="rule73.svg" width="65px" height="65px">
        </td>
    </tr>
    <tr>
        <td width="70px">
            <img src="rule105.svg" width="65px" height="65px">
        </td>
        <td colspan="2" width="140px">
            <img src="rule1738243.svg" width="135px" height="65px">
        </td>
    </tr>
</tbody>
</table>
EOF
