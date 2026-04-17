from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order
from .forms import OrderClientForm, OrderManagerForm, OrderAdminForm


def get_user_role(user):
    if not user.is_authenticated:
        return 'guest'
    if user.is_superuser:
        return 'admin'
    if user.groups.filter(name='Менеджеры').exists():
        return 'manager'
    if user.groups.filter(name='Клиенты').exists():
        return 'client'
    return 'guest'


@login_required
def order_list(request):
    role = get_user_role(request.user)
    if role == 'client':
        orders = Order.objects.filter(client=request.user).select_related('product', 'client')
    elif role in ('manager', 'admin'):
        orders = Order.objects.all().select_related('product', 'client')
    else:
        messages.error(request, 'У вас нет доступа к заказам.')
        return redirect('products:product_list')
    return render(request, 'orders/order_list.html', {'orders': orders, 'user_role': role})


@login_required
def order_create(request):
    role = get_user_role(request.user)
    if role not in ('client', 'admin'):
        messages.error(request, 'Создавать заказы могут только клиенты и администраторы.')
        return redirect('orders:order_list')

    FormClass = OrderClientForm if role == 'client' else OrderAdminForm

    if request.method == 'POST':
        form = FormClass(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if role == 'client':
                order.client = request.user
            order.save()
            messages.success(request, 'Заказ успешно создан.')
            return redirect('orders:order_list')
    else:
        form = FormClass()

    return render(request, 'orders/order_form.html', {
        'form': form,
        'title': 'Создать заказ',
        'user_role': role,
    })


@login_required
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    role = get_user_role(request.user)

    if role == 'guest' or role == 'client':
        messages.error(request, 'У вас нет прав для редактирования заказов.')
        return redirect('orders:order_list')

    FormClass = OrderManagerForm if role == 'manager' else OrderAdminForm

    if request.method == 'POST':
        form = FormClass(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заказ успешно обновлён.')
            return redirect('orders:order_list')
    else:
        form = FormClass(instance=order)

    return render(request, 'orders/order_form.html', {
        'form': form,
        'title': 'Редактировать заказ',
        'order': order,
        'user_role': role,
    })


@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    role = get_user_role(request.user)

    if role != 'admin':
        messages.error(request, 'Только администратор может удалять заказы.')
        return redirect('orders:order_list')

    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Заказ успешно удалён.')
        return redirect('orders:order_list')

    return render(request, 'orders/order_confirm_delete.html', {
        'order': order,
        'user_role': role,
    })
