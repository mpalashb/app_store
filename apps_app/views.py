from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from django.views.generic import ListView, DetailView
from apps_app.models import AppProduct, Category
from customizer.models import HeroCustomizer


class AppDetailView(DetailView):
    model = AppProduct
    template_name = "app-detail.html"
    context_object_name = "app_obj"
    # pk_url_kwarg = "app_pk"
    slug_url_kwarg = "app_slug"


class AppsListView(ListView):
    model = AppProduct
    template_name = "appsList.html"
    context_object_name = 'apps_list'
    ordering = '-id'

    cat_top = None
    cats = []

    try:
        cat_top = Category.objects.first()
        cats = Category.objects.all()
    except Exception as p:
        print("===================================")
        print("Category Exception AppsListView ", p)
        print("===================================")

    extra_context = {'top': cat_top,
                     'cats': cats}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['customizer'] = HeroCustomizer.objects.last()

        return context


class SearchListView(ListView):
    model = AppProduct
    template_name = "apps-search.html"
    context_object_name = "apps_list"
    ordering = '-id'

    def get_queryset(self):
        apps_query = self.request.GET.get("apps-search-query")
        print("apps_query", apps_query)

        serach_data = AppProduct.objects.filter(

            Q(name__icontains=apps_query) |
            Q(slug__icontains=apps_query) |
            Q(website__icontains=apps_query) |
            Q(desc__icontains=apps_query)


        )

        print(serach_data.count() == 0)

        if serach_data.count() == 0:
            search_items_count_msg = 'No result!'
        else:
            search_items_count_msg = f'{str(serach_data.count())} items found!'

        self.extra_context = {
            'count_msg': search_items_count_msg}

        return serach_data


class FilterView(ListView):
    model = AppProduct
    template_name = "appsListFilter.html"
    context_object_name = "apps_list"
    ordering = '-id'

    def get_queryset(self):
        cat_item = self.kwargs.get("cat")

        cat_top = None
        cats = []

        try:
            cat_top = Category.objects.first()
            cats = Category.objects.all()
        except Exception as p:
            print("===================================")
            print("Category Exception FilterView ", p)
            print("===================================")

        self.extra_context = {

            'filter_cat': str(cat_item).title(),
            'customizer': HeroCustomizer.objects.last(),
            'top': cat_top,
            'cats': cats

        }

        # obj_fil_cat = get_object_or_404(Category, name=str(cat_item))

        queryFilter = AppProduct.objects.filter(
            # category=obj_fil_cat
            category__name=str(cat_item)
        )

        if queryFilter.exists():
            return queryFilter.all()

        else:
            try:

                Category.objects.get(name=str(cat_item).title())
                self.extra_context = {

                    'filter_cat': str(cat_item).title(),
                    'filter_cat_info': f""" No apps for -- """,
                    'customizer': HeroCustomizer.objects.last(),
                    'top': cat_top,
                    'cats': cats

                }
            except:
                self.extra_context = {

                    'filter_cat': str(cat_item).title(),
                    'filter_cat_info': "No available category and products are found! filter --",
                    'customizer': HeroCustomizer.objects.last(),
                    'top': cat_top,
                    'cats': cats

                }

        return queryFilter.all()
