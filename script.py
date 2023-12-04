import socket
import time
import cv2
import numpy as np

#pyautogui.alert('test init code', "Title")

#upperbody_detector = cv2.CascadeClassifier('haarcascade_upperbody.xml')
#cap = cv2.VideoCapture(0)


if _name=="main_":
	#rapiberry IP: 192.168.0.29 -> wlan- -> inet ip no wifi de casa
	host = "" #como raspi é o host, não precisa por IP
	port = 3365
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((host,port))
	
	print("Server started. Waiting for connection")
	s.listen()
	c, addr = s.accept()
	print("Connection from: ", addr)
	
	
	face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	cap = cv2.VideoCapture(0) 
	i = 0
	
	while True:
		# Verificar se a câmera foi aberta corretamente
		if not cap.isOpened():
			raise Exception("Não foi possível abrir a câmera")

			# Ler o próximo quadro da câmera
		ret, frame = cap.read()

			# Se não for possível ler o quadro, sair do loop
		if not ret:
			break

		frame_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		face = face_detector.detectMultiScale(frame_cinza,
									  scaleFactor = 1.07, minNeighbors = 8,minSize =(80,80))
		deteccoes = len(face)
		print('deteccoes = ',deteccoes)
		string = str(deteccoes)
		
		i = i + 1 
		print(i)
		
		if i == 30:
			c.send(string.encode('utf-8')) 
			i = 0  
			

		for (x,y,w,h) in face:
			cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
			
		cv2.imshow('Cascade', frame)
	
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()