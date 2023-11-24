from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category
from .forms import ProductForm

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    # Initial setup
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    # Check if there are query parameters in the request
    if request.GET:
        # Sorting logic
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                # Sort by product name (case-insensitive)
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                # Sort by category name
                sortkey = 'category__name'
            if 'direction' in request.GET:
                # Check sorting direction
                direction = request.GET['direction']
                if direction == 'desc':
                    # Reverse sorting order if descending
                    sortkey = f'-{sortkey}'
            # Apply sorting to products
            products = products.order_by(sortkey)

        # Filtering by category logic
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        # Search query logic
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                # Display an error message if search criteria is empty
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            # Define search criteria using Q objects
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            # Apply search filter to products
            products = products.filter(queries)

    # Set up context data
    current_sorting = f'{sort}_{direction}'
    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    # Render the template with the context data
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    # Retrieve the product with the specified ID, or return a 404 response
    product = get_object_or_404(Product, pk=product_id)

    # Set up context data
    context = {
        'product': product,
    }

    # Render the template with the context data
    return render(request, 'products/product_detail.html', context)


def add_product(request):
    """ Add a product to the store """

    # Initialize a new ProductForm instance
    form = ProductForm()
    # Set the template name
    template = 'products/add_product.html'
    # Set up context data
    context = {
        'form': form,
    }

    # Render the template with the context data
    return render(request, template, context)
