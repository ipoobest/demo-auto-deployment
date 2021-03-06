# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse, reverse_lazy
from django.utils.six import BytesIO
from django.views.generic import TemplateView

import xhtml2pdf.pisa as pisa

from ..models import AgentTransport
from customer.models import Shipper
from ndd.settings import STATICFILES_DIRS


class AgentTransportPrintView(TemplateView):
    
    def get(self, request, pk, template):
        if template == 'forward':
            template_name = 'pdf_template/agent_transport_fw_template.html'
        elif template == 'backward':
            template_name = 'pdf_template/agent_transport_bw_template.html'
        else:
            template_name = 'pdf_template/agent_transport_full_template.html'

        agent_transport = get_object_or_404(AgentTransport, pk=pk)

        if agent_transport.address == 'other':
            address = agent_transport.address_other
        elif agent_transport.address == 'shipper':
            try:
                shipper = Shipper.objects.get(name=agent_transport.shipper)
                address = shipper.address
            except Shipper.DoesNotExist:
                address = ''
        else:
            address = ''

        return self.render(template_name, {'agent_transport': agent_transport, 'address': address,'static_dir': STATICFILES_DIRS[0]})

    def render(self, path, params):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response, encoding="UTF-8")
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)
            