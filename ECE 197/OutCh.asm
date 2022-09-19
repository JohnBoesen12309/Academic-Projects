OutCh		equ	$1EA0

		org	$0200

		

		code
		cld
Print:		lda	#$4A
		jsr	OutCh
		lda	#$6F
		jsr	OutCh
		lda	#$68
		jsr	OutCh
		lda	#$6E
		jsr	OutCh
		lda	#$0B
		jsr	OutCh
		jmp	Print


