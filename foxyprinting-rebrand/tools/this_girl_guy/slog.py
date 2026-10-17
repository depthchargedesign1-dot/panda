import re
def slogan(t):
    s=t
    s=re.sub(r'\s*(Printed Office Mug|Printed Mug FUNNY|Mug Personalised ADULT OFFICE MUG|Personalised ADULT OFFICE MUG|INSPIRED STYLE Mug Gift( Printed Mug)?|Printed Mug|Mug)\s*$','',s,flags=re.I)
    s=re.sub(r'\s+2$','',s)
    return s.strip()
