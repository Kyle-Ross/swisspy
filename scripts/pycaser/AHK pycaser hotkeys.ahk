; Ensure this file remains in the same location as the .py and .bat files to maintain the relative references

^+7::
Send, {Ctrl Down}c{Ctrl Up}
Run, "run pycaser proper.bat",, Hide
Sleep 250
Send, {Ctrl Down}v{Ctrl Up}
return

^+8::
Send, {Ctrl Down}c{Ctrl Up}
Run, "run pycaser lower.bat",, Hide
Sleep 250
Send, {Ctrl Down}v{Ctrl Up}
return

^+9::
Send, {Ctrl Down}c{Ctrl Up}
Run, "run pycaser upper.bat",, Hide
Sleep 250
Send, {Ctrl Down}v{Ctrl Up}
return

^+0::
Send, {Ctrl Down}c{Ctrl Up}
Run, "run pycaser alternating.bat",, Hide
Sleep 250
Send, {Ctrl Down}v{Ctrl Up}
return