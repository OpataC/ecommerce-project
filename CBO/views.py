from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm, RegisterForm
from .models import Product, SizeGuide, StoreSettings


# ==========================================
# HELPER FUNCTIONS
# ==========================================
def is_staff_user(user):
  """Check whether the logged-in user has staff/admin privileges."""
  return user.is_staff


# ==========================================
# PUBLIC PAGES
# ==========================================
def home(request):
  """Display the store homepage with live database categories, stock counts,

  featured arrivals, size guide, and boutique info.
  """
  # Count products per category in a single database query
  counts_qs = Product.objects.values('category').annotate(total=Count('id'))
  category_counts = {item['category']: item['total'] for item in counts_qs}

  # Display metadata mapped to Product.CATEGORY_CHOICES keys
  category_meta = {
      'Casual': {
          'slug': 'casual',
          'tagline': 'Everyday Essentials',
          'description': (
              'Comfortable t-shirts, denim jeans, casual shirts, and trendy'
              ' dresses crafted for everyday style and lasting comfort.'
          ),
          'highlights': 'Tees • Denim • Dresses',
      },
      'Formal': {
          'slug': 'formal',
          'tagline': 'Executive Edit',
          'description': (
              'Tailored suits, crisp button-down shirts, blazers, and smart'
              ' trousers designed to keep you sharp for work and special'
              ' events.'
          ),
          'highlights': 'Suits • Blazers • Trousers',
      },
      'Kids': {
          'slug': 'kids',
          'tagline': 'Family & Extras',
          'description': (
              "Durable children's outfits, stylish footwear, belts, bags, and"
              ' seasonal outerwear to complete every wardrobe.'
          ),
          'highlights': 'Kids • Shoes • Bags',
      },
  }

  # Build dynamic category cards from model choices + live DB counts
  categories = []
  for code, label in Product.CATEGORY_CHOICES:
    meta = category_meta.get(code, {})
    categories.append({
        'code': code,
        'name': label,
        'slug': meta.get('slug', code.lower()),
        'tagline': meta.get('tagline', 'Boutique Collection'),
        'description': meta.get('description', ''),
        'highlights': meta.get('highlights', ''),
        'product_count': category_counts.get(code, 0),
    })

  # Fetch latest arrivals, inventory totals, size guide, and store settings
  featured_products = Product.objects.order_by('-id')[:4]
  total_products = Product.objects.count()
  in_stock_count = Product.objects.filter(stock__gt=0).count()
  size_guides = SizeGuide.objects.all()
  store_info = StoreSettings.objects.first()

  context = {
      'categories': categories,
      'featured_products': featured_products,
      'total_products': total_products,
      'in_stock_count': in_stock_count,
      'size_guides': size_guides,
      'store_info': store_info,
  }
  return render(request, 'home.html', context)


# ==========================================
# USER AUTHENTICATION (Register, Login, Logout)
# ==========================================
def register_view(request):
  """Handle new customer account registration."""
  if request.method == 'POST':
    form = RegisterForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(
          request, 'Account created successfully! Please log in.'
      )
      return redirect('login')
    messages.error(request, 'Please correct the errors below.')
  else:
    form = RegisterForm()

  return render(request, 'register.html', {'form': form})


def login_view(request):
  """Authenticate user credentials and route based on staff vs.

  regular role.
  """
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      messages.success(request, f'Welcome back, {user.username}!')

      # Staff go to inventory dashboard; regular users go to customer dashboard
      if user.is_staff:
        return redirect('products')
      return redirect('userdashboard')

    messages.error(request, 'Invalid username or password. Please try again.')

  return render(request, 'login.html')


def logout_user(request):
  """End the current user session and redirect to the login screen."""
  logout(request)
  messages.info(request, 'You have been logged out.')
  return redirect('login')


# ==========================================
# USER DASHBOARD
# ==========================================
@login_required(login_url='login')
def user_dashboard(request):
  """Display the dashboard and available catalog for logged-in customers."""
  products_list = Product.objects.filter(stock__gt=0).order_by('-id')
  return render(
      request, 'Users/user_dashboard.html', {'products': products_list}
  )


# ==========================================
# ADMIN PRODUCT MANAGEMENT (CRUD - Staff Only)
# ==========================================
@login_required(login_url='login')
@user_passes_test(is_staff_user, login_url='login')
def products(request):
  """READ: Display all inventory items in the Admin Dashboard.

  Supports optional category filtering via query string (?category=Casual).
  """
  selected_category = request.GET.get('category', '').capitalize()
  all_products = Product.objects.all().order_by('-id')

  valid_categories = dict(Product.CATEGORY_CHOICES).keys()
  if selected_category in valid_categories:
    all_products = all_products.filter(category=selected_category)

  context = {
      'products': all_products,
      'selected_category': selected_category,
  }
  return render(request, 'admin_dashboard.html', context)


@login_required(login_url='login')
@user_passes_test(is_staff_user, login_url='login')
def add_product(request):
  """CREATE: Add a new clothing item to the store inventory."""
  if request.method == 'POST':
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      messages.success(
          request, 'New clothing item has been added to inventory!'
      )
      return redirect('products')
  else:
    form = ProductForm()

  return render(request, 'add_product.html', {'form': form})


@login_required(login_url='login')
@user_passes_test(is_staff_user, login_url='login')
def update_product(request, id):
  """UPDATE: Edit an existing product's details, stock, or image."""
  product = get_object_or_404(Product, id=id)

  if request.method == 'POST':
    form = ProductForm(request.POST, request.FILES, instance=product)
    if form.is_valid():
      form.save()
      messages.success(request, 'Product updated successfully!')
      return redirect('products')
  else:
    form = ProductForm(instance=product)

  return render(request, 'add_product.html', {'form': form, 'product': product})


@login_required(login_url='login')
@user_passes_test(is_staff_user, login_url='login')
def delete_product(request, id):
  """DELETE: Permanently remove a product from the database."""
  product = get_object_or_404(Product, id=id)
  product.delete()
  messages.success(request, 'Product deleted successfully.')
  return redirect('products')
