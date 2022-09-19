
temp01		equ	$0300

		org	$0200

		code
		ldx	#$0
top:		inx
		stx	temp01
		jmp	top
