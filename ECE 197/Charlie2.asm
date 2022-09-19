		

PortA		equ	$1740
PortADDR	equ	$1741
PortB		equ	$1742
PortBDDR	equ	$1743

		org	$0000
						; A is the Digit Data
						; X = 0 and is used turn off all segments beteen digit data changes
						; Y is the Index to the Segment Data

SegmentData:	db	$58,$74,$77,$50,$34,$79

		org	$0200

		code
		ldx	#$ff
		stx	PortADDR	; Set Port A to output
		stx	PortBDDR	; Set PrtB to output
		inx			; X = 0
FirstDigit:	lda	#$06		; Set A to the one before the first digit
		sta	PortB
		ldy	#$00

NextDigit:	stx	PortA		; Segments Off
		inc	PortB		; Next Digit
		inc	PortB		; Next Digit
		lda	SegmentData,y	; Get New Data
		sta	PortA		; Output New Data
		iny
		cpy	#7
		bne	NextDigit
		beq	FirstDigit
		