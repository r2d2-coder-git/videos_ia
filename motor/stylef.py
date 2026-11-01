"""SF Mono (variable) helper + GitHub-dark syntax palette."""
from PIL import ImageFont
import render as R
SFM = "/System/Library/Fonts/SFNSMono.ttf"
_c = {}
def MO(size, w=400):
    k = (size, w)
    if k not in _c:
        f = ImageFont.truetype(SFM, size); f.set_variation_by_axes([w, w]); _c[k] = f
    return _c[k]
BSYN = {R.SYN["kw"]: (255, 123, 114), R.SYN["str"]: (165, 214, 255), R.SYN["fn"]: (210, 168, 255),
        R.SYN["var"]: (220, 226, 234), R.SYN["num"]: (121, 192, 255), R.SYN["const"]: (121, 192, 255), R.SYN["p"]: (160, 170, 185)}
