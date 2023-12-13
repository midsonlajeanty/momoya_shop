from django.views.generic import ListView, DetailView

from apps.catalog.models.product import Product


# Create your views here.
class ProductListView(ListView):
    template_name = "catalog/product_list.html"
    queryset = Product.objects.available()
    paginate_by = 10


class ProductDetailView(DetailView):
    template_name = "catalog/product_detail.html"
    queryset = Product.objects.available_with_images()
