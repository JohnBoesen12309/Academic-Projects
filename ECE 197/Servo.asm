
PortAS		equ	$1700
PortASDDR	equ	$1701

		org	$0200

		code
		lda	$01
		sta	PortAS
		lda	$01
		sta	PortASDDR
Start:		ldy	#$0F
Delay1:		jsr	Delay100
		dey
		bne	Delay1
		lda	#$00
		sta	PortAS
		ldy	#$C8
Delay2:		jsr	Delay100
		dey
		bne	Delay2
		jmp	Start
;
;
Delay100: 		ldx	#$14
Jump:		dex
		bne	Jump
		rts
	