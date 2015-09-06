from django.shortcuts import get_object_or_404
from django.views.generic import View

from django.views.decorators.csrf import csrf_exempt

import os

#from django.db import *

from rest_framework import status, generics, permissions, views
from rest_framework.response import Response

from autenticazione.serializers import FotoSerializer

from autenticazione.processing import findMainColor, findSURFMatch

import sys

class Upload(views.APIView):

	@csrf_exempt
	def post(self, request):

		try:
			# Qui ci aspettiamo una request contentente:
			# image, compass, longitude e latitude (e user a breve TODO)

			image = request.data.get('image', None)
			compass = request.data.get('compass', -1)
			longitude = request.data.get('long', -1)
			latitude = request.data.get('lat', -1)
			nomefile = request.data.get('nomefile', None)

			# Salvo il file in locale
			if image:

				try:
					image = image.decode('base64')
				except:
					# L'immagine non e in base 64!
					pass

				# TODO: PATH Assoluto usando variabili d'ambiente!
				if nomefile:
					nomefile = nomefile
				else:
					nomefile = "upload.jpg"

				path = os.path.dirname(os.path.abspath(__file__)) + "/static/" + nomefile

				fh = open(path, 'wb+')
				fh.write(image)

				if compass:
					compass = int(compass)

				# Salviamo una nuova istanza di Foto

				# TODO:
				# Fare la media dei colori dell'immagine e uscire il colore di media della foto
				# (per colorare il titolo della card e alcuni dettagli)
				# OPENCV

				mainColor = findMainColor(nomefile)

				newFoto = Foto.objects.create(image=nomefile, compass=compass, latitude=latitude, longitude=longitude, color=mainColor)
				newFotoSerial = FotoSerializer(data=newFoto)

				if newFotoSerial.is_valid():
					return Response({'foto': newFotoSerial.data}, status=status.HTTP_201_CREATED)
				else: 
					return Response({"error": "Foto con campi non validi!", 'foto': newFotoSerial.data}, status=status.HTTP_400_BAD_REQUEST)
				
			return Response({'status': "Immagine non pervenuta"}, status=status.HTTP_400_BAD_REQUEST)

		except Exception as e:

			errors = {
				'type': str(type(e)),
				'args': list(e.args),
				'message' : str(e)
			}

			return Response({'error': errors}, status=status.HTTP_400_BAD_REQUEST)

class FindPhotos(views.APIView):

	def get(self, request, format=None):

		lat = request.GET.get('lat', None)
		long = request.GET.get('long', None)
		id = request.GET.get('id', None)

		if lat and long and id:
			# Siamo interessati ad averle entrambe

			lat = float(lat)
			long = float(long)

			# Dimensioni del "quadrato" in cui andiamo a cercare
			accuracy = 0.0100000

			lat_lt = lat + accuracy
			lat_gt = lat - accuracy

			long_lt = long + accuracy
			long_gt = long - accuracy

			# Cerchiamo nel DB per foto corrispondenti
			querySet = Foto.objects.filter(latitude__gt = lat_gt, latitude__lt = lat_lt,
											longitude__gt = long_gt, longitude__lt = long_lt)

			if lat == 0 and long == 0:
				querySet = Foto.objects.all()

			# Ordiniamo la lista secondo la differenza 
			# delle coordinate da quella di riferimento 

			listaFoto = []

			for foto in querySet:

				accuracy = abs(foto.latitude - lat) + abs(foto.longitude - long)

				newFoto = {
					'image': foto.image,
					'compass': foto.compass,
					'longitude': foto.longitude,
					'latitude': foto.latitude,
					'created_at': foto.created_at,
					'id': foto.id,
					'accuracy': accuracy,
					'color': foto.color
				}

				listaFoto.append(newFoto)

			querySet = sorted(listaFoto, key= lambda k: k['accuracy'])

			# Faccio il processing delle prime 4 immagini

			processedImage = querySet[:3]

			sourceImg = Foto.objects.filter(pk=id)[0]

			if sourceImg:
				for index, image in enumerate(processedImage):

					affinity = findSURFMatch(sourceImg.image, image['image'])
					querySet[index]['affinity'] = int(affinity)
			
			serialData = FotoSerializer(data=querySet, many=True)

			if serialData.is_valid():
				return Response({'data': serialData.data}, status=status.HTTP_200_OK)
			else:
				return Response({'errors': serialData.errors}, status=status.HTTP_400_BAD_REQUEST)
			
		else: 
			return Response({'error': "No lat or long"}, status=status.HTTP_400_BAD_REQUEST)

