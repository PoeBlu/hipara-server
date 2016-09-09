from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
import json
import datetime


class CsrfExemptSessionAuthentication(SessionAuthentication):
	def enforce_csrf(self, request):
		return


class LogsViewSet(viewsets.ViewSet):
	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

	def store_alerts(self, request, *args, **kwargs):
		result = {'data': {'error': "You have to login First"}, 'status': 403}
		if request.user.is_authenticated():
			result = {'data': {'error': 'No alerts given'}, 'status': 422}
			try:
				alerts = json.loads(request.body.decode("utf-8"));
				if alerts.get('alerts') and isinstance(alerts['alerts'], list):
					alerts = alerts['alerts']
					for alert in alerts:
						if (alert.get('hostName') and alert.get('alertType') and
							alert['alertType'] in ('ALERT_FILE', 'ALERT_CMD') and alert.get('alertMessage') and
								alert.get('timeStamp') and validate_date(alert['timeStamp'])):
							if alert['alertType'] == 'ALERT_FILE' and alert.get('fileName'):
								pass
							elif alert['alertType'] == 'ALERT_CMD' and alert.get('command') and alert.get('parentProcessId'):
								try:
									number = int(alert['parentProcessId'])
								except ValueError:
									raise ValueError('Invalid Json Format (parentProcessId should be integer)')
								else:
									if number > 0:
										pass
									else:
										raise ValueError('Invalid Json Format (parentProcessId should be integer)')
							else:
								raise ValueError('Invalid Json Format')
						else:
							raise ValueError('Invalid Json Format')
				else:
					raise ValueError('No alerts given')
				from .models import Alert, Host
				import os
				script_dir = os.path.dirname(__file__)
				rel_path = "logs/alert_cmd.json"
				file_path = os.path.join(script_dir, rel_path)
				user = request.user
				for alert in alerts:
					if alert['alertType'] == 'ALERT_FILE':
						host = Host.objects.update_or_create(
							name=alert['hostName'],
							uuid=alert['host_uuid'] if alert.get('host_uuid') else None,
							last_seen=datetime.datetime.now()
						)
						Alert.objects.create(
							host=host[0],
							fileName=alert['fileName'],
							alertMessage=alert['alertMessage'],
							alertType=alert['alertType'],
							timeStamp=validate_date(alert['timeStamp']),
							created_by=user,
							process_name=alert['process_name'] if 'process_name' in alert else None,
							host_ipaddr=alert['host_ipaddr'] if 'host_ipaddr' in alert else None,
						)
					else:
						json_data = json.dumps(alert) + ",\n"
						with open(file_path, "ab") as f:
							f.write(bytes(json_data, 'utf-8'))
				result = {'data': {'message': "alerts successfully recorded"}, 'status': 200}
			except ValueError as e:
				result = {'data': {'error': str(e)}, 'status': 422}
		return Response(data=result['data'], status=result['status'])

	def view_alerts(self, request, *args, **kwargs):
		result = {'data': {'error': "You have to login First"}, 'status': 403}
		if request.user.is_authenticated():
			if request.user.metadata.role_id < 3:
				result = {'data': {'error': 'No alerts Found'}, 'status': 204}
				try:
					page_number = request.GET.get('page_number')
					page_size = request.GET.get('page_size')
					search = request.GET.get('search')
					if not page_number:
						page_number = 1
					if not page_size:
						page_size = 10
					if not search:
						search = ""
					from .models import Alert
					from django.db.models import Q
					from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
					alerts = Alert.objects.filter(Q(host__name__icontains=search) | Q(fileName__icontains=search) | Q(
						alertMessage__icontains=search) | Q(process_name__icontains=search) | Q(
						host__uuid__icontains=search) | Q(host_ipaddr__icontains=search)).order_by('-timeStamp')
					length = len(alerts)
					if length:
						value = []
						for alert in alerts:
							user = alert.created_by
							user = {
								'first_name': user.first_name,
								'last_name': user.last_name,
								'email': user.email
							}
							tempValue = {
								'alert_id': alert.alert_id,
								'hostName': alert.host.name,
								'fileName': alert.fileName,
								'alertMessage': alert.alertMessage,
								'timeStamp': alert.timeStamp.strftime("%d %b, %Y %I:%M %P"),
								'created_by': user,
								'created_at': alert.created_at.strftime("%d %b, %Y %I:%M %P"),
								'alertEval': alert.alertEval,
								'process_name': alert.process_name,
								'host_uuid': alert.host.uuid,
								'host_ipaddr': alert.host_ipaddr

							}
							value.append(tempValue)
						paginator = Paginator(value, page_size)
						try:
							value = paginator.page(page_number)
							data = {
								'alerts': value.object_list,
							}
							result = {'data': data, 'status': 200}
						except PageNotAnInteger:
							value = paginator.page(1)
							data = {
								'alerts': value.object_list,
							}
							result = {'data': data, 'status': 200}
						except EmptyPage:
							pass
				except Exception as e:
					result = {'data': {'error': str(e)}, 'status': 422}
			else:
				result = {'data': "Not Allowed to Service User", 'status': 401}
		return Response(data=result['data'], status=result['status'])

	def update_alert_eval(self, request, alert_id=None, EVAL=None):
		result = {'data': {'error': "You have to login First"}, 'status': 403}
		if request.user.is_authenticated():
			if request.user.metadata.role_id < 3:
				from .models import Alert
				alert = Alert.objects.filter(alert_id=alert_id).first()
				if alert and EVAL:
					alert.alertEval = int(EVAL)
					alert.save()
					result = {'data': "success", 'status': 200}
				else:
					result = {'data': "Alert not found", 'status': 404}
			else:
				result = {'data': "Not Allowed to Service User", 'status': 401}
		return Response(data=result['data'], status=result['status'])


def validate_date(date_text):
	try:
		return datetime.datetime.strptime(date_text, '%H:%M, %d/%m/%Y').strftime("%Y-%m-%d %H:%M")
	except ValueError as e:
		raise ValueError("Incorrect data format, should be hh:mm, dd/mm/yyyy")
	return False
