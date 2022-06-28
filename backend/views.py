from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from backend.models import Order, Entry, Cash
from backend.forms import OrderForm, EntryForm, CashForm


def index(request):
    # Home page
    return render(request, 'backend/index.html')


def check_order_owner(owner, request):
    if owner != request.user:
        raise Http404


@login_required()
def orders(request):
    orders = Order.objects.filter(owner=request.user).order_by('-date_added')
    context = {'orders': orders}
    return render(request, 'backend/orders.html', context)


@login_required()
def order(request, order_id):
    order = Order.objects.get(id=order_id)
    # Проверка того, что тема принадлежит текущему пользователю
    check_order_owner(order.owner, request)
    entries = order.entry.order_by('-date_added')
    context = {'order': order, 'entries': entries}
    return render(request, 'backend/order.html', context)


@login_required()
def new_order(request):
    #создаем заказ
    if request.method != 'POST':
        # Данные не отправляются, создается пустая форма
        form = OrderForm()
    else:
        form = OrderForm(data=request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.owner = request.user
            form.save()
            return redirect('backend:orders')

    # Вывести пустую иди недействительную форму
    context = {'form': form}
    return render(request, 'backend/new_order.html', context)


@login_required()
def new_entry(request, order_id):
    """Добавляем коммент к заказу"""
    order = Order.objects.get(id=order_id)
    if request.method != 'POST':
        check_order_owner(order.owner, request)
        # Данные не отправляются, создается пустая форма
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.order = order
            new_entry.save()
            return redirect('backend:order', order_id=order_id)

    # Вывести пустую иди недействительную форму
    context = {'order': order, 'form': form}
    return render(request, 'backend/new_entry.html', context)


@login_required()
def edit_entry(request, entry_id):
    """"Редактирует запись конкретной темы"""
    entry = Entry.objects.get(id=entry_id)
    order = entry.order
    # Проверка того, что тема принадлежит текущему пользователю
    check_order_owner(order.owner, request)
    if request.method != 'POST':
        """Исходный запрос, форма заполняется данными текущей записи"""
        form = EntryForm(instance=entry)
    else:
        """Отправка данных POST"""
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            print('POST')
            return redirect('backend:order', order_id=order.id)

    context = {'entry': entry, 'order': order, 'form': form}
    return render(request, 'backend/edit_entry.html', context)


@login_required()
def all_cash(request):
    all_cash = Cash.objects.filter(user=request.user).order_by('id')
    context = {'all_cash': all_cash}
    return render(request, 'backend/all_cash.html', context)


@login_required()
def cash(request, cash_id):
    cash = Cash.objects.get(id=cash_id)
    check_order_owner(cash.user, request)
    context = {'cash': cash}
    return render(request, 'backend/cash.html', context)


@login_required()
def new_cash(request):
    """"Создаем кассу"""
    if request.method != 'POST':
        # Данные не отправляются, создается пустая форма
        form = CashForm()
    else:
        form = CashForm(data=request.POST)
        if form.is_valid():
            new_cash = form.save(commit=False)
            new_cash.user = request.user
            form.save()
            return redirect('backend:all_cash')

    # Вывести пустую иди недействительную форму
    context = {'form': form}
    return render(request, 'backend/new_cash.html', context)