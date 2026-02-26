# ການແກ້ໄຂບັນຫາ QR Code ແລະ MERCHANT_ID

## ບັນຫາທີ່ພົບ
1. ✅ QR Code ບໍ່ສະແດງໃນໜ້າ `/events/django-bootcamp-2025/payment/BCEL/`
2. ✅ MERCHANT_ID ບໍ່ສະແດງ

## ສາເຫດ
- View `event_payment_process` ບໍ່ໄດ້ສົ່ງຂໍ້ມູນ `qr_data` ແລະ `merchant_id` ໄປໃຫ້ template

## ການແກ້ໄຂທີ່ເຮັດແລ້ວ

### 1. ປັບປຸງ `events/views.py` (line 198-206)
```python
context = {
    'event': event,
    'registration': registration,
    'payment': payment,
    'method': method,
    'qr_data': payment.qr_code_data,      # ✅ ເພີ່ມ
    'merchant_id': payment.merchant_id,    # ✅ ເພີ່ມ
}
return render(request, 'events/payment_process.html', context)
```

### 2. ປັບປຸງ Template `payment_process.html` (line 22-27)
```html
<!-- ກ່ອນແກ້: ໃຊ້ພຽງ external API -->
<img src="https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={{ qr_data }}">

<!-- ຫຼັງແກ້: ໃຊ້ QR image ຈາກ Django ກ່ອນ, ຖ້າບໍ່ມີຈຶ່ງໃຊ້ API -->
{% if payment.qr_code_image %}
<img src="{{ payment.qr_code_image.url }}" alt="BCEL OnePay QR Code">
{% else %}
<img src="https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={{ qr_data }}">
{% endif %}
```

## ວິທີການເຮັດວຽກ

1. **ເມື່ອສ້າງ Payment** (ໃນ `BCELOnePayService.create_payment()`):
   - ສ້າງ `BCELOnePayPayment` object
   - ເອີ້ນ `payment.generate_qr_code()`
   - ສ້າງ QR image ແລະ ບັນທຶກໄວ້ຢູ່ `media/payments/qr_codes/`

2. **ໃນ Template**:
   - ສະແດງ QR Code image ຈາກ `payment.qr_code_image.url`
   - ສະແດງ Merchant ID: `{{ payment.merchant_id }}` = `mch5f0e5f1d512c8`

## ກວດສອບວ່າເຮັດວຽກ

1. ເຂົ້າໄປທີ່: `http://localhost:8000/events/django-bootcamp-2025/payment/BCEL/`

2. ທ່ານຄວນຈະເຫັນ:
   - ✅ QR Code ສະແດງ (ຈາກ media files ຫຼື external API)
   - ✅ Merchant ID: mch5f0e5f1d512c8
   - ✅ Order Ref ແລະ Amount

## Configuration ທີ່ຕ້ອງມີ

### core/settings/base.py
```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

### core/urls.py
```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## ໂຄງສ້າງ Media Files
```
media/
└── payments/
    └── qr_codes/
        └── qr_payment_<uuid>.png
```

## ຕົວຢ່າງ QR Data Format
```
mch5f0e5f1d512c8|50000.00|LAK|<payment-uuid>
```

## ການທົດສອບ

```bash
# 1. Restart server
python manage.py runserver

# 2. ເຂົ້າໄປທີ່ payment page
http://localhost:8000/events/<event-slug>/payment/BCEL/

# 3. ກວດສອບວ່າ:
- QR Code ສະແດງ ✅
- Merchant ID ສະແດງ ✅
- Amount ຖືກຕ້ອງ ✅
```

## ສິ່ງທີ່ຕ້ອງກວດເພີ່ມເຕີມ

1. ✅ qrcode module ຕິດຕັ້ງແລ້ວ
2. ✅ Pillow ຕິດຕັ້ງແລ້ວ
3. ✅ MEDIA settings ຖືກຕ້ອງ
4. ✅ URL patterns ຮອງຮັບ media files

## ສະຫຼຸບ

ທຸກຢ່າງພ້ອມແລ້ວ! QR Code ແລະ MERCHANT_ID ຄວນຈະສະແດງຖືກຕ້ອງແລ້ວ. 🎉
