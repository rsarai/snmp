#!/usr/bin/env python
#-*- coding: utf-8 -*-

def get_snmp_answer(endIP, Port): 
		import socket
		import struct

		#Digita Alvo
		#endIP = raw_input('Digite o endereco do alvo: ')
		#Port = int(raw_input('Digite a porta do alvo: ')) # 161 ou 9002
		endIP = str(endIP)
		Port = int(Port)

		# endIP = '192.168.25.220'
		# Port = 9002
		
		#prepara socket e conecta a interface - sem o 3o. argumento (protocol)
		#nao ha filtragem do tipo de protocolo na recepcao
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.settimeout(10)
		s.bind(('', 0))

		#Monta mensagem SNMP (Q)
		Q = []
		#Sequence / structure
		Q.append(chr(0x30)) # structure / sequence
		#Q.append(chr(0x28)) ###### comprimento = 40 bytes
		Q.append(chr(0x27))
		#Versão
		Q.append(chr(0x2)) # Type int
		Q.append(chr(0x1)) # comprimento = 1 byte
		Q.append(chr(0x0)) # valor, versão = 0 (SNMPv1)
		#Community
		Q.append(chr(0x4)) # type string
		Q.append(chr(0x6)) # comprimento = 6 bytes
		Q.append('p') #
		Q.append('u') #
		Q.append('b') #
		Q.append('l') #
		Q.append('i') #
		Q.append('c') #
		#PDU type
		Q.append(chr(0xa0)) # GETREQUEST
		#Q.append(chr(0x1b)) ###### comprimento = 27 bytes
		Q.append(chr(0x1a))
		#ID do request
		Q.append(chr(0x02)) # type int
		Q.append(chr(0x01)) # comprimento = 1 byte
		Q.append(chr(0x01)) # valor = 1, ID do request
		#Error
		Q.append(chr(0x02)) # type int
		Q.append(chr(0x01)) # comprimento = 1 byte
		Q.append(chr(0x00)) # valor = 0, request não usa
		#Error Index
		Q.append(chr(0x02)) # type int
		Q.append(chr(0x01)) # comprimento = 1 byte
		Q.append(chr(0x00)) # valor = 0, request não usa
		#Sequence / structure
		Q.append(chr(0x30)) # structure / sequence
		#Q.append(chr(0x10)) ###### comprimento = 16 bytes
		Q.append(chr(0x0f))
		#Sequence / structure
		Q.append(chr(0x30)) # structure / sequence
		#Q.append(chr(0x0e)) ###### comprimento = 14bytes
		Q.append(chr(0x0d))
		#Object
		Q.append(chr(0x06)) # type = OID
		#Q.append(chr(0x0a)) ####### comprimento = 10 bytes
		Q.append(chr(0x09))
		# 1.3.6.1.2.1.2.2.1
		Q.append(chr(0x2b)) # ISO (1)+ ORG (3)
		Q.append(chr(0x06)) # DoD
		Q.append(chr(0x01)) # Internet
		Q.append(chr(0x02)) # management
		Q.append(chr(0x01)) # MIB
		Q.append(chr(0x02)) # System
		Q.append(chr(0x02)) # Interfaces
		Q.append(chr(0x01)) # ifTable
		Q.append(chr(0x02)) # ifEntry

		#Value
		Q.append(chr(0x05)) # Type = Null
		Q.append(chr(0x00)) # comprimento = 0 bytes
		#
		#print Q
		#converte de lista para string
		Qs = ''.join(Q)
		#print Q
		# Qs = str.encode(Qs)
		#envia frame
		s.sendto(Qs, (endIP, Port))
		print 'Quadro enviado ...'

		#recebe resposta snmp
		while True:
			try:
				Rxbuf = s.recv(4096)
				print 'Resposta Recebida!'
				lbuf = list(Rxbuf)
				print Rxbuf
				print lbuf
				break
			except socket.timeout:
				print 'TIME OUT!!!'
				exit()

		s.close()
		return lbuf
