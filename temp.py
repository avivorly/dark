

try:
    1/0
except Exception:

    import re
    import traceback
    s = traceback.format_exc()


    print(s)