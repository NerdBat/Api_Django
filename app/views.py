from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from django.core.paginator import Paginator
import json

DATA = {
    'liliar34': {
        'name': 'John Doe',
        'age': 25,
        'location': 'Paris',
        'is_active': False,
    }
}

@csrf_exempt
def greeting_post(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            name = body.get("name")
            if name in DATA:
                return JsonResponse(DATA[name])
            else:
                return JsonResponse({'error': 'User not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Only POST allowed'}, status=405)

def test_json_view(request):
    return JsonResponse(DATA["liliar34"])

def get_all_products(request):
    products = Product.objects.all()
    data = list(products.values())
    return JsonResponse(data,safe=False)
    
def get_most_expensive_product(request):
    product = Product.objects.order_by('-price').first()
    if product:
        data = {
            'name': product.name,
            'price': float(product.price),
            'description': product.description,
        }
        return JsonResponse(data)
    return JsonResponse({'error': 'No product found'}, status=404)

@csrf_exempt
def add_product(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product = Product.objects.create(
            name=data['name'],
            price=data['price'],
            description=data.get('description', '')
        )
        return JsonResponse({'message': 'Product added', 'id': product.id})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def update_product(request, product_id):
    if request.method == 'PUT':
        try:
            product = Product.objects.get(id=product_id)
            data = json.loads(request.body)
            product.name = data.get('name', product.name)
            product.price = data.get('price', product.price)
            product.description = data.get('description', product.description)
            product.save()
            return JsonResponse({'message': 'Product updated'})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    return JsonResponse({'error': 'Invalid method'}, status=405)

def has_permission(user, action):
    try:
        rights = AccessRight.objects.get(user=user)
        return getattr(rights, f'can_{action}', False)
    except AccessRight.DoesNotExist:
        return False
    if not has_permission(request.user, 'view'):
        return JsonResponse({'error': 'Unauthorized'}, status=403)



def paginated_products(request):
    products = Product.objects.all()
    paginator = Paginator(products, 3)  
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    data = list(page_obj.object_list.values())
    return JsonResponse({
        'products': data,
        'page': page_obj.number,
        'num_pages': paginator.num_pages,
    })

