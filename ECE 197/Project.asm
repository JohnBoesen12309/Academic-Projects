
PortAS		equ	$1700
PortASDDR	equ	$1701
PortAK		equ	$1740
PortAKDDR	equ	$1741
GetKey		equ	$1F6A

		org	$0200

		code
;---------------------------------------------------------------------------------------------
;----------------------- Scans for the key press andstores it in register y -----------
;---------------------------------------------------------------------------------------------


Scan:		ldx	#$00
		stx	PortAKDDR
		jsr	GetKey
		cmp	#$15
		beq	Scan
		tay
;---------------------------------------------------------------------------------------------
;--------------- Takes Register Y data and moves the servo to angle---------------
;---------------------------------------------------------------------------------------------

Start:		lda	$01
		sta	PortAS
		lda	$01
		sta	PortASDDR
Delay1:		jsr	Delay100
		dey
		bne	Delay1
		lda	#$00
		sta	PortAS
		ldy	#$C8
Delay2:		jsr	Delay100
		dey
		bne	Delay2
		jmp	Scan
;
;
Delay100: 		ldx	#$14
Jump:		dex
		bne	Jump
		rts
	