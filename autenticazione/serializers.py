from rest_framework import serializers 
from autenticazione.models import Foto

from rest_framework.exceptions import ValidationError

import time, datetime
import json


class FotoSerializer(serializers.BaseSerializer):

	def to_representation(self, obj):


		return dict(obj)


	def to_internal_value(self, data):

		fields = (('image', True),
				  ('compass', True),
				  ('latitude', True),
				  ('longitude', True),
				  ('created_at', True),
				  ('id', True),
				  ('accuracy', False),
				  ('color', True),
				  ('affinity', False))

		results = {}

		for field in fields:

			tmpValue = None

			try:
				tmpValue = data.get(field[0], None)
			except:

				print field[0], field[1]
				if field[1]:
					tmpValue = getattr(data, field[0])

			if field[1] and not tmpValue:
				# Campo richiesto! Non puo essere nullo!
				raise ValidationError({
					field[0] : "Questo campo non puo essere vuoto"
					})

			# Validazione andata a buon fine
			results[field[0]] = tmpValue

		results['created_at'] = int(time.mktime(results['created_at'].timetuple())*1000)

		return { i:results[i] for i in results if results[i] != None}

		"""
		if not accuracy and not color:

			return {
				'image': image_path,
				'compass': compass,
				'latitude' : latitude,
				'longitude': longitude,
				'id': foto_id,
				'created_at': created_at
			}

		return {
				'image': image_path,
				'compass': compass,
				'latitude' : latitude,
				'longitude': longitude,
				'id': foto_id,
				'created_at': created_at,
				'accuracy': accuracy
			}
		"""


	def create(self, validated_data):

		# Funzione chiamata quando viene creato un oggetto 
		# a partire dai dati ValidationError

		# Togliamo l'id o potrebbe dare errori!
		del validated_data['id']
		del validated_data['created_at']
		del validated_data['accuracy']

		return Foto.objects.create(**validated_data)
