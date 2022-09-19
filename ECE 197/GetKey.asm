		
PortA		equ	$1740
PortADDR	equ	$1741
GetKey		equ	$1F6A

		org	$0200

		

		code
		cld
		ldx	#$00
		stx	PortADDR
Scan:		jsr	GetKey
		cmp	#$15
		beq	Scan
		sta	$0300
		brk


