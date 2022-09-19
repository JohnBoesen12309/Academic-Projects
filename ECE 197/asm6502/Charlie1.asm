;Displays a name on the Kim-1 board		

PortA		equ	$1740
PortADDR	equ	$1741
PortB		equ	$1742
PortBDDR	equ	$1743

		org	$0200
						; A is the Digit Select Data
						; X = 0 and is used turn off all segments beteen digit data changes
						; Y is the Segment Data
		code
		ldx	#$ff
		stx	PortADDR	; Set Port A to output
		stx	PortBDDR	; Set PrtB to output
		inx			; X = 0
FirstDigit:	lda	#$06		; Set A to the first digit
		sta	PortB
		ldy	#$59
		jsr	DisplayADigit
		ldy	#$59
		jsr	DisplayADigit
		ldy	#$59
		jsr	DisplayADigit
		ldy	#$59
		jsr	DisplayADigit
		ldy	#$59
		jsr	DisplayADigit
		ldy	#$59
		jsr	DisplayADigit
		jmp	FirstDigit
;
;
DisplayADigit:	stx	PortA		; Segments Off
		sty	PortA		; New Data
		rts


