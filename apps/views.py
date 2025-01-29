import json
import os

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, FormView
import telebot
from .form import ProductForm, FinishProductModelForm
from .models import Product, Category, FinishProduct, FinishCategory, ProductHistory, FinishProductHistory
from dotenv import load_dotenv

load_dotenv()


class ProductListView(ListView):
    queryset = Product.objects.filter(soni__gt=0).all()
    template_name = 'product_list.html'
    context_object_name = 'products'


@csrf_exempt
def sell_product(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # JSON ma'lumotlarni olish
            product_id = data.get('product_id')  # Mahsulot ID
            decrease_amount = int(data.get('decrease_amount'))  # Kamaytirish miqdori

            # Mahsulotni ma'lumotlar bazasidan olish
            product = Product.objects.get(id=product_id)

            # Kamaytirish miqdorini tekshirish
            if decrease_amount > product.soni:
                return JsonResponse({'success': False, 'error': 'Kiritilgan miqdor mavjuddan oshib ketdi!'})

            product.soni -= decrease_amount
            product.save()
            text = (f"Yarm Tayor Maxsulot Chiqdi \n"
                    f"🅿️Nomi : {product.nomi.nomi}\n"
                    f"↗️Chiqib ketdi : {decrease_amount}\n"
                    f"🔢Qoldi : {product.soni}")
            bot = telebot.TeleBot(os.getenv('TOKEN'))
            ProductHistory.objects.create(nomi=product.nomi, soni=decrease_amount,
                                           status=ProductHistory.StatusType.CHIQDI)
            try:
                bot.send_message(chat_id=(os.getenv('ID')), text=text)
            except Exception as e:
                return e

            return JsonResponse({'success': True, 'new_quantity': product.soni})  # Yangi miqdorni qaytarish
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Mahsulot topilmadi!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Noto‘g‘ri so‘rov turi.'})


class ProductFormView(FormView, ListView):
    template_name = 'product_add.html'
    form_class = ProductForm
    queryset = Category.objects.all()
    success_url = reverse_lazy('product_list')
    context_object_name = 'categories'

    def form_valid(self, form):
        nomi_id = form.cleaned_data['nomi']
        soni = form.cleaned_data['soni']

        product = Product.objects.filter(nomi_id=nomi_id).first()

        if product:
            product.soni += soni
            product.save()
            text = (f"Yarm Tayor Maxsulot qushildi \n"
                    f"🅿️Nomi : {product.nomi.nomi}\n"
                    f"↘️Qushildi : {soni}\n"
                    f"🔢Jami : {product.soni}")
        else:
            category = Category.objects.filter(id=nomi_id.pk).first()
            if category:
                text = (f"Yarm Tayor Maxsulot qushildi \n"
                        f"🅿️Nomi : {category.nomi}\n"
                        f"↘️Qushildi : {soni}\n"
                        f"🔢Jami : {soni}")
            else:
                text = "Kategoriya topilmadi."
            form.save()
        TOKEN = os.getenv('TOKEN')
        bot = telebot.TeleBot(TOKEN)
        ProductHistory.objects.create(nomi=nomi_id, soni=soni, status=ProductHistory.StatusType.QABUL)

        try:
            bot.send_message(chat_id=(os.getenv('ID')), text=text)
        except Exception as e:
            pass
        # Asosiy form_valid chaqiriladi
        return super().form_valid(form)


class FinishProductListView(ListView):
    queryset = FinishProduct.objects.filter(soni__gt=0).all()
    template_name = 'finish_product_list.html'
    context_object_name = 'finish_products'


@csrf_exempt
def sell_finish_product(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # JSON ma'lumotlarni olish
            product_id = data.get('product_id')  # Mahsulot ID
            decrease_amount = int(data.get('decrease_amount'))  # Kamaytirish miqdori

            # Mahsulotni ma'lumotlar bazasidan olish
            product = FinishProduct.objects.get(id=product_id)

            # Kamaytirish miqdorini tekshirish
            if decrease_amount > product.soni:
                return JsonResponse({'success': False, 'error': 'Kiritilgan miqdor mavjuddan oshib ketdi!'})

            # Miqdorni yangilash
            product.soni -= decrease_amount
            product.save()
            text = (f"Tayor Maxsulot Chiqdi \n"
                    f"🅿️Nomi : {product.nomi.nomi}\n"
                    f"↗️Chiqib ketdi : {decrease_amount}\n"
                    f"🔢Qoldi : {product.soni}")
            bot = telebot.TeleBot(os.getenv('TOKEN'))
            FinishProductHistory.objects.create(nomi=product.nomi, soni=decrease_amount,
                                                 status=FinishProductHistory.StatusType.CHIQDI)

            try:
                bot.send_message(chat_id=(os.getenv('ID')), text=text)
            except Exception as e:
                pass

            return JsonResponse({'success': True, 'new_quantity': product.soni})  # Yangi miqdorni qaytarish
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Mahsulot topilmadi!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Noto‘g‘ri so‘rov turi.'})


class FinishProductFormView(FormView, ListView):
    template_name = 'finish_product_add.html'
    form_class = FinishProductModelForm
    queryset = FinishCategory.objects.all()
    success_url = reverse_lazy('finish_product_list')
    context_object_name = 'categories'

    def form_valid(self, form):
        nomi_id = form.cleaned_data['nomi']
        soni = form.cleaned_data['soni']

        product = FinishProduct.objects.filter(nomi_id=nomi_id).first()

        if product:
            product.soni += soni
            product.save()
            text = (f"Tayor Maxsulot qushildi \n"
                    f"🅿️Nomi : {product.nomi.nomi}\n"
                    f"↘️Qushildi : {soni}\n"
                    f"🔢Jami : {product.soni}")
        else:
            finish_category = FinishCategory.objects.filter(id=nomi_id.pk).first()
            text = (f"Tayor Maxsulot qushildi \n"
                    f"🅿️Nomi : {finish_category.nomi}\n"
                    f"↘️Qushildi : {soni}\n"
                    f"🔢Jami : {soni}")
            form.save()
        bot = telebot.TeleBot(os.getenv('TOKEN'))
        FinishProductHistory.objects.create(nomi=nomi_id, soni=soni, status=FinishProductHistory.StatusType.QABUL)
        try:
            bot.send_message(chat_id=(os.getenv('ID')), text=text)
        except Exception as e:
            pass
        # Asosiy form_valid chaqiriladi
        return super().form_valid(form)
