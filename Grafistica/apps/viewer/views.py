import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from .forms import LoginForm
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from Grafistica.apps.viewer.models import FileTemp, Chart
from .models import ExcelData, GraphExcelData, DataAnalytic
from .functions import excel_to_json, json_to_dataframe
from django.template.loader import render_to_string
from Grafistica.apps.utils.email import send_email
from django.utils.translation import ugettext as _
from Grafistica.core.json_reader import json_settings
from django.contrib import messages
from Grafistica.apps.utils.messages import error, info


settings = json_settings()


class IndexView(View):
    template_name = "index.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            name = request.POST['name']
            email = request.POST['email']
            subject = request.POST['subject']
            message = request.POST['message']

            to_email = "diego.arcos.witness@gmail.com"
            mail_template = "mail/contact_email.html"
            content = render_to_string(mail_template, {'url_server': settings['URL_SERVER'],
                                                       'user_name': name,
                                                       'email': email,
                                                       'message': message,
                                                       })
            send_email(_(subject),
                       content=content, to=[to_email], content_type="text/html")
            messages.success(request, "Gracias por ponerte en contácto con nosotros.")
        except:
            return self.get(request)
        return self.get(request)


class BaseAdminView(LoginRequiredMixin, View):
    template_name = "base_admin.html"

    def get(self, request):
        return render(request, self.template_name)


class ExcelListView(LoginRequiredMixin, View):
    """
    Listado de archivos
    """
    template_name = "file_list.html"
    item_menu = "files"

    def get(self, request):
        files = DataAnalytic.objects.filter(user=request.user)
        return render(request, self.template_name, {'files': files, 'item_menu': self.item_menu})


class ExcelFileDetailView(LoginRequiredMixin, View):
    """
    Detalle de un excel.
    """
    template_name = "file_detail.html"
    item_menu = "files"

    def get(self, request, data_id):
        data = DataAnalytic.objects.get(id=data_id)
        return render(request, self.template_name, {'data': data, 'item_menu': self.item_menu})

    def post(self, request, data_id):
        data = DataAnalytic.objects.get(id=data_id)
        data.name = request.POST.get('name')
        data.save()
        return self.get(request, data_id)


class ExcelFileDeleteView(View):
    """
    Eliminamos el archivo de base de datos.
    """

    def get(self, request, data_id):
        data = DataAnalytic.objects.get(id=data_id)
        data.delete()
        my_url = reverse('viewer:file-list')
        return HttpResponseRedirect(my_url)


class ExcelFileToJsonView(View):
    """
    Devolvemos el archivo editado en formato json
    """

    def get(self, request, data_id):
        data = DataAnalytic.objects.get(id=data_id)
        response = HttpResponse(data.json, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename={0}.json'.format(data.name)
        return response


class ImportFileView(LoginRequiredMixin, View):
    """
    Step 1.
    """
    template_name = "import_file.html"
    item_menu = "analytics"

    def get(self, request):
        ctx = {'step': 1, "item_menu": self.item_menu}
        return render(request, self.template_name, ctx)

    def post(self, request):
        try:
            the_file = request.FILES['myfile']
        except:
            the_file = None
        if the_file:
            data = DataAnalytic()
            data.file = the_file
            data.user = request.user
            data.save()
            data.json = excel_to_json(data)
            data.save()
            my_url = reverse('viewer:view-file', kwargs={'data_id': data.id})
            return HttpResponseRedirect(my_url)
        else:  # Si no recibimos el archivo entonces solo recargamos la página.
            return self.get(request)


class ViewFileView(LoginRequiredMixin, View):
    """
    Step 2
    """
    template_name = "import_file.html"
    item_menu = "analytics"

    def get(self, request, data_id):
        data = DataAnalytic.objects.get(id=data_id)
        json_data = json.loads(data.json)
        ctx = {'json_data': json_data, 'step': 2, 'data': data, 'item_menu': self.item_menu}
        return render(request, self.template_name, ctx)

    def post(self, request, data_id):
        """
        Recibe el nuevo json para que lo reemplacemos por el bueno.
        :param request: request user
        :param data_id: id del archivo excel
        :return: None, generamos un HttpResponseRedirect
        """
        data = DataAnalytic.objects.get(id=data_id)
        new_json = request.POST.get('jsondata')
        data.json = new_json
        data.save()
        my_url = reverse('viewer:graph-file', kwargs={'data_id': data.id, 'step': 3})
        return HttpResponseRedirect(my_url)


class GraphFileView(LoginRequiredMixin, View):
    """
    Step 3 (Dashboard)
    """
    template_name = "graph_file.html"
    item_menu = "analytics"

    def get(self, request, data_id, step):
        data = DataAnalytic.objects.get(id=data_id)
        # json_data = json.loads(data.json)
        json_data = json_to_dataframe(data.json)
        chart = None

        # step = 3
        step = int(step)
        if step == 4:
            if data.chart_set.exists():
                chart = data.chart_set.first()
                step = 4
        ctx = {'json_data': json_data, 'step': step, 'data': data, "item_menu": self.item_menu, 'chart': chart}
        return render(request, self.template_name, ctx)

    def post(self, request, data_id, step):
        chart_selected = request.POST.get('radio')
        data = DataAnalytic.objects.get(id=data_id)
        if data.chart_set.exists():
            chart = data.chart_set.first()
            chart.type_key = chart_selected
            # chart.data_file = data
            chart.save()
        else:
            chart = Chart()
            chart.type_key = chart_selected
            chart.data_file = data
            chart.save()
        # json_data = json.loads(data.json)
        # ctx = {'json_data': json_data, 'step': 4, 'data': data, "item_menu": self.item_menu}
        # return render(request, self.template_name, ctx)
        return HttpResponseRedirect(reverse('viewer:graph-file', kwargs={'data_id': data_id, 'step': 4}))


class LoginView(View):
    template_name = "login.html"
    form = LoginForm

    def get(self, request):
        default_email = request.GET['email'] if 'email' in request.GET else ""
        if 'next' in request.GET and request.GET['next']:
            next_url = request.GET['next']
        else:
            next_url = None
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('viewer:file-list'))
        else:
            ctx = {'form': self.form(), 'next_url': next_url, 'default_email': default_email}
            return render(request, self.template_name, ctx)

    def post(self, request):
        logout(request)  # Deslogeamos primero antes de realizar un login.
        form = self.form(request.POST)
        if 'next' in request.POST and request.POST['next']:
            next_url = request.POST['next']
        else:
            next_url = reverse('viewer:file-list')
        if form.is_valid():
            login(request, form.my_user)
            return HttpResponseRedirect(next_url)
        else:
            ctx = {'form': form}
            return render(request, self.template_name, ctx)


class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")

