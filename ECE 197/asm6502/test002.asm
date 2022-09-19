
PortA		equ	$1740
PortADDR	equ	$1741
PortB		equ	$1742
PortBDDR	equ	$1743

		org	$0200

		code
		ldx	#$ff
		stx	PortADDR
		stx	PortBDDR
		inx
First:		lda	#$06
		sta	PortB
		ldy	#$7C
		jsr	Display
		jmp	First


Display:		stx	PortA
		sty	PortA
		rts