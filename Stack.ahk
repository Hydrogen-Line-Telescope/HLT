#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

; Initialize
global array := []
return



; Pop
^+x::
Var1 := array.Pop()
Send, %Var1%
return

; Push
^+c::

Clipboard := ""

Send, ^c
ClipWait, 1, 1

Var = %Clipboard%

array.Push(Var)

return

;Paste
^+v::
Send, % array[array.MaxIndex()]
return

; View Stack
^+z::

i := array.MaxIndex()

Loop
{	
	MsgBox % array[i]
	i := i -1

	if (i = 0 or i < 0)
	{
		break
	}
}

return

; Clear Stack
^+0::

i := array.MaxIndex()

Loop
{
	array.Delete(i)
	i := i - 1
	
	if(i = 0 or i < 0)
	{
		MsgBox, "Stack is Clear"
		break
	}
}

return