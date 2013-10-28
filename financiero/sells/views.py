# from ajax_view import ajax_view

from django.shortcuts import render_to_response
from django.template import RequestContext


def nueva_venta(request):
	return render_to_response ('template_base.html', request.session, context_instance=RequestContext(request))

