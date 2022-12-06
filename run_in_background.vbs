Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /k ""cd app & py clipboard_to_catbox.py"""
oShell.Run strArgs, 0, false