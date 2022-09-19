;  This is a program to scroll a Smiley Face across all 6 displays on the KIM-1.

		

PortA		equ	$1740		; Address of Port A Data Register
PortADDR	equ	$1741		; Address of Port A Data Direction register
PortB		equ	$1742		; Address of Port B Data Register
PortBDDR	equ	$1743		; Address of Port B Data Direction register

SmilyFace	equ	$1d		; Indicates which segments to turn on for the smiley face (reguires some imagination - feel free to impove!)

		org	$0200
						; A is used to set the Digit Select Data the first time only
						; X = 0 and is used turn off all segments beteen digit data changes
						; Y is the Segment Data
		code
		cld			;Clear Decimal Mode JUST IN CASE
		ldx	#$ff
		stx	PortADDR	; Set Port A to output
		stx	PortBDDR	; Set PrtB to output
		ldx	#$00		; X = 0
FirstDigit:	lda	#$06		; Set A to the first digit (-2 becasue we inc it twice in the DisplayADigit Routine)
		sta	PortB
		ldy	#SmilyFace	; Load Y with Smily Face data
		jsr	DisplayADigit	; Display Y Data in Digit 1 (left most digit)
		jsr	Delay		; Leave it there for a bit, wasting time in "Delay" routine
		jsr	DisplayADigit	; Display Y Data in Digit 2
		jsr	Delay		; Leave it there for a bit, wasting time in "Delay" routine
		jsr	DisplayADigit	; Display Y Data in Digit 3
		jsr	Delay		; Leave it there for a bit, wasting time in "Delay" routine
		jsr	DisplayADigit	; Display Y Data in Digit 4
		jsr	Delay		; Leave it there for a bit, wasting time in "Delay" routine
		jsr	DisplayADigit	; Display Y Data in Digit 5
		jsr	Delay		; Leave it there for a bit, wasting time in "Delay" routine
		jsr	DisplayADigit	; Display Y Data in Digit 6
		jsr	Delay		; Leave it there for a bit, wasting time in "Delay" routine
		jmp	FirstDigit	; Go back to Digit 1


;
;------------------------------------------------------------------------------------------
;----------------  This Subroutine Displays the Data in Y on the next Digit  --------------
;------------------------------------------------------------------------------------------
;
DisplayADigit:	stx	PortA		; Segments Off
		inc	PortB		; Next Digit
		inc	PortB		; Next Digit
		sty	PortA		; New Data
		rts			; Now return from the subroutine


;
;------------------------------------------------------------------------------------------
;----------------  This Subroutine Delays about 1/4 second  -------------------------------
; It clobbers the X and Y registers, so it saves them on the stack first, then restores them
;------------------------------------------------------------------------------------------
;
Delay:		txa			;Save X on the Stack
		pha
		tya			;Save Y on the stack
		pha
		ldy	#$ff		;Put the start value in Y
Delay1:		ldx	#$ff		;Put the start value in X
Delay2:		dex
		bne	Delay2		;Loop back until X = 0
		dey				;Once x = 0, then dec Y
		bne	Delay1			;And loop back until Y = 0
		pla			;Restore Y from the stack
		tay
		pla			;Restore X from the stack
		tax
		rts			;Now return from the subroutine
