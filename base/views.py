from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic.base import TemplateView, View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q

from .models import City, Company, JobOffer, Branch
from .forms import MyCompanyCreationForm, CompanyForm
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class LoginView(TemplateView):
    template_name = 'base/login.html'
    context = {}

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            company = Company.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
            return super().get(request, *args, **kwargs)

        company = authenticate(request, username=username, password=password)

        if company is not None:
            login(request, company)
            return redirect('home')
        else:
            messages.error(request, 'User OR password does not exist')

        return super().get(request, *args, **kwargs)


class LogoutView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


class RegisterView(TemplateView):
    template_name = 'base/register.html'
    form = MyCompanyCreationForm()

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context = {'form': self.form}

        return context

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = MyCompanyCreationForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.username = company.username.lower()
            company.save()
            login(request, company)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
        return super().get(request, *args, **kwargs)


class ManageAccountView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = '/login/'

    template_name = 'base/manage_account.html'
    form = CompanyForm()

    def post(self, request, *args, **kwargs):
        company = self.request.user
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            return redirect('login')

    def get_context_data(self, **kwargs):
        context = super(ManageAccountView, self).get_context_data(**kwargs)
        context['company_name'] = self.request.user.company_name
        context['description'] = self.request.user.description
        context['avatar'] = self.request.user.avatar
        context['form'] = self.form

        return context


class HomeView(TemplateView):
    template_name = 'base/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        context['popular_job_offers'] = JobOffer.objects.all()
        if len(context['popular_job_offers']) > 10:
            context['popular_job_offers'] = context['popular_job_offers'][-10:]

        context['popular_categories'] = Branch.objects.all()[:7]
        context['popular_locations'] = City.objects.all()[:7]

        context['categories'] = Branch.objects.all()
        context['locations'] = City.objects.all()

        return context

    def post(self, request, *args, **kwargs):
        position = request.POST.get('search')
        branch_name = request.POST.get('branch')
        location = request.POST.get('location')
        working_mode = request.POST.get('working_mode')

        return redirect(reverse('jobs') + f'?p={position}&c={branch_name}&l={location}&wm={working_mode}')


class AboutUsView(TemplateView):
    template_name = 'base/about_us.html'


class ContactView(TemplateView):
    template_name = 'base/contact.html'


class OfferView(TemplateView):
    template_name = 'base/single.html'

    def get_context_data(self, pk, **kwargs):
        context = super(OfferView, self).get_context_data(**kwargs)

        context['popular_job_offers'] = JobOffer.objects.all()
        if len(context['popular_job_offers']) > 10:
            context['popular_job_offers'] = context['popular_job_offers'][-10:]

        context['popular_categories'] = Branch.objects.all()[:7]
        context['popular_locations'] = City.objects.all()[:7]

        context['offer'] = JobOffer.objects.get(id=pk)

        return context


class CreateOfferView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = '/login/'

    template_name = 'base/create_offer.html'

    def post(self, request, *args, **kwargs):

        branch_name = request.POST.get('branch')
        if not branch_name:
            branch_name = 'Unknown'
        branch, created = Branch.objects.get_or_create(name=branch_name)

        city_name = request.POST.get('city')
        if not city_name:
            city_name = 'Unknown'
        city, created = City.objects.get_or_create(name=city_name)

        JobOffer.objects.create(
            company=request.user,
            position=request.POST.get('position'),
            address=request.POST.get('address'),
            working_mode=request.POST.get('working_mode'),
            min_salary=request.POST.get('min_salary'),
            max_salary=request.POST.get('max_salary'),
            currency=request.POST.get('currency'),
            description=request.POST.get('description'),
            requirements=request.POST.get('requirements'),
            overview=request.POST.get('overview'),
            branch=branch,
            city=city,
        )

        return redirect('home')


class JobsView(TemplateView):
    template_name = 'base/jobs.html'

    def get_context_data(self, **kwargs):
        p = self.request.GET.get(
            'p') if self.request.GET.get('p') != None else ''
        l = self.request.GET.get(
            'l') if self.request.GET.get('l') != None else ''
        c = self.request.GET.get(
            'c') if self.request.GET.get('c') != None else ''
        wm = self.request.GET.get(
            'wm') if self.request.GET.get('wm') != None else ''

        context = super(JobsView, self).get_context_data(**kwargs)

        context['job_offers'] = JobOffer.objects.filter(
            Q(position__icontains=p) &
            Q(city__name__icontains=l) &
            Q(branch__name__icontains=c) &
            Q(working_mode__icontains=wm)
        )

        context['popular_job_offers'] = JobOffer.objects.all()
        if len(context['popular_job_offers']) > 10:
            context['popular_job_offers'] = context['popular_job_offers'][-10:]

        context['popular_categories'] = Branch.objects.all()[:7]
        context['popular_locations'] = City.objects.all()[:7]

        context['categories'] = Branch.objects.all()
        context['locations'] = City.objects.all()

        return context

    def post(self, request, *args, **kwargs):
        position = request.POST.get('search')
        branch_name = request.POST.get('branch')
        location = request.POST.get('location')
        working_mode = request.POST.get('working_mode')

        return redirect(reverse('jobs') + f'?p={position}&c={branch_name}&l={location}&wm={working_mode}')


class MyOffersView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = '/login/'

    template_name = 'base/my_offers.html'

    def get_context_data(self, **kwargs):
        context = super(MyOffersView, self).get_context_data(**kwargs)
        context['job_offers'] = JobOffer.objects.filter(
            company=self.request.user)

        return context
