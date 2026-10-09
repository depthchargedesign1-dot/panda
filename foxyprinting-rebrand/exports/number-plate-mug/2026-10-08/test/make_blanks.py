import sys, os
sys.path.insert(0, "/home/user/panda/foxyprinting-rebrand/tools/artwork")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import any_name_number_plate_mug as an, number_plate_mugs as npm
import number_plate_mug_local_mockups as lm
out = sys.argv[1]
for c in npm.COUNTRIES:
    tex = os.path.join(out, f"blank-{c[1]}-wrap.png")
    an.texture("", "", c, tex)
    lm.flat(tex).save(os.path.join(out, f"FOXY-SUB-PNPMANOT-preview-blank-{c[1]}.jpg"), quality=90)
    print(c)
