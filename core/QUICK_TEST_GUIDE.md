# ຄູ່ມືການທົດສອບດ່ວນ - Quick Test Guide

## 🚀 ການທົດສອບ BCEL OnePay QR Code

### ຂັ້ນຕອນທີ່ 1: ກວດສອບ Server

```bash
# ກວດສອບວ່າ server ເຮັດວຽກ
# Server ຄວນແສດງ:
Django version 5.2.8, using settings 'core.settings.dev'
Starting development server at http://0.0.0.0:8000/
```

**Status**: ✅ Server ເຮັດວຽກປົກກະຕິແລ້ວ

---

### ຂັ້ນຕອນທີ່ 2: ເຂົ້າໄປໜ້າ Payment

1. ເປີດ browser ໄປທີ່:
```
http://localhost:8000/events/django-bootcamp-2025/
```

2. ກົດປຸ່ມ "ລົງທະບຽນເຂົ້າງານ" (Register)

3. ເລືອກຈຳນວນປີ້ ແລະກົດ "ດຳເນີນການຕໍ່"

4. ເລືອກວິທີຈ່າຍເງິນ: **BCEL OnePay**

5. ທ່ານຈະໄປຮອດໜ້າ:
```
http://localhost:8000/events/django-bootcamp-2025/payment/BCEL/
```

---

### ຂັ້ນຕອນທີ່ 3: ກວດສອບໜ້າ Payment

ຄວນເຫັນ:

✅ **QR Code ສະແດງ** (ຂະໜາດ 256x256 pixels)
```
ຮູບ QR Code ສີດຳ-ຂາວ
ຢູ່ໃນກອບສີແດງ
```

✅ **Merchant ID ສະແດງ**
```
ID: mch5f0e5f1d512c8
```

✅ **Payment Details ສະແດງ**
```
Merchant ID: mch5f0e5f1d512c8
Order Ref: 000001 (ຫຼືຕົວເລກອື່ນ)
Amount: ₭50,000 (ຫຼືຈຳນວນອື່ນ)
```

✅ **Timer ນັບຖອຍຫຼັງ**
```
Time remaining: 14:59
```

---

### ຂັ້ນຕອນທີ່ 4: ທົດສອບການສະແກນ QR

#### Option A: ທົດສອບດ້ວຍ BCEL One App (ແນະນຳ)

1. **ເປີດ BCEL One app** ບົນມືຖື
2. **Login** ເຂົ້າບັນຊີຂອງທ່ານ
3. **ເລືອກເມນູ "Scan to Pay"** ຫຼື "ສະແກນຈ່າຍ"
4. **ສະແກນ QR Code** ຈາກໜ້າຈໍຄອມພິວເຕີ
5. **ກວດສອບຂໍ້ມູນ** ທີ່ສະແດງໃນ app:
   - Merchant: Python for Laos
   - Amount: ຕົງກັບຈຳນວນເງິນ
   - Reference: Payment ID
6. **ຢືນຢັນການຈ່າຍເງິນ**

#### Option B: ທົດສອບການອ່ານ QR (ກວດເບື້ອງຕົ້ນ)

1. ໃຊ້ໂທລະສັບສະແກນ QR Code
2. ຄວນເຫັນຂໍ້ຄວາມຍາວໆທີ່ເລີ່ມຕົ້ນດ້ວຍ:
```
0002010102...
```
3. ນີ້ແມ່ນ EMVCo QR data ✅

#### Option C: ທົດສອບດ້ວຍ Online QR Decoder

1. Right-click ເທິງ QR Code → "Save image as..."
2. ບັນທຶກເປັນ `test-qr.png`
3. ອັບໂຫຼດໄປທີ່: https://zxing.org/w/decode
4. ກວດສອບວ່າ decoded text ມີໂຄງສ້າງ EMVCo

---

### ຂັ້ນຕອນທີ່ 5: ກວດສອບ QR Data (Advanced)

```bash
python manage.py shell
```

```python
from events.models import BCELOnePayPayment

# ເອົາ payment ຫຼ້າສຸດ
payment = BCELOnePayPayment.objects.last()

# ສະແດງຂໍ້ມູນ
print("=" * 60)
print("QR CODE DATA")
print("=" * 60)
print(f"Merchant ID: {payment.merchant_id}")
print(f"Amount: {payment.amount} {payment.currency}")
print(f"Payment ID: {payment.payment_id}")
print()
print("QR Code String:")
print(payment.qr_code_data)
print()

# ກວດສອບ tags
qr = payment.qr_code_data
print("EMVCo Tags:")
print(f"✅ Payload Format (00): {qr[0:6]}")
print(f"✅ Init Method (01): {qr[6:12]}")
print(f"✅ Currency LAK: {'5303418' in qr}")
print(f"✅ Country LA: {'5802LA' in qr}")
print(f"✅ Merchant Name: {'Python for Laos' in qr}")
print(f"✅ City: {'Vientiane' in qr}")
print()

# ກວດສອບ QR image
if payment.qr_code_image:
    print(f"✅ QR Image: {payment.qr_code_image.url}")
else:
    print("❌ QR Image: Not generated")
```

**Expected Output**:
```
============================================================
QR CODE DATA
============================================================
Merchant ID: mch5f0e5f1d512c8
Amount: 50000.00 LAK
Payment ID: cbf6237f-fa4f-41e7-baf9-bd0e689cd1de

QR Code String:
000201010212292400160mch5f0e5f1d512c852040000530341854085000.005802LA5916Python for Laos6009Vientiane624901380cbf6237f-fa4f-41e7-baf9-bd63041234

EMVCo Tags:
✅ Payload Format (00): 000201
✅ Init Method (01): 010212
✅ Currency LAK: True
✅ Country LA: True
✅ Merchant Name: True
✅ City: True

✅ QR Image: /media/payments/qr_codes/qr_payment_cbf6237f-fa4f-41e7-baf9-bd0e689cd1de.png
```

---

## 📱 ຜົນທີ່ຄາດຫວັງ

### ✅ ຖ້າສຳເລັດ:
- BCEL One app ອ່ານ QR Code ໄດ້
- ສະແດງຂໍ້ມູນການຈ່າຍເງິນຖືກຕ້ອງ
- ສາມາດຢືນຢັນແລະຈ່າຍເງິນໄດ້

### ⚠️ ຖ້າຍັງມີບັນຫາ:

#### ບັນຫາ 1: BCEL One ບໍ່ຮູ້ຈັກ QR
**ສາເຫດເປັນໄປໄດ້**:
- Tag number ບໍ່ຖືກຕ້ອງ (ລອງປ່ຽນ tag 29 ເປັນ 26, 27, 28)
- Merchant ID format ບໍ່ຕົງກັບ BCEL ກຳນົດ
- BCEL OnePay ໃຊ້ specifications ພິເສດ

**ວິທີແກ້**:
1. ອ່ານ `QR_DEBUG_GUIDE.md`
2. ປ່ຽນ tag number ໃນ `events/models.py`
3. ຕິດຕໍ່ BCEL ຂໍເອກະສານ

#### ບັນຫາ 2: QR Code ບໍ່ຊັດເຈນ
**ວິທີແກ້**:
```python
# ໃນ events/models.py, generate_qr_code():
box_size=15,  # ເພີ່ມຂະໜາດ
error_correction=qrcode.constants.ERROR_CORRECT_H  # ເພີ່ມ error correction
```

#### ບັນຫາ 3: Amount ບໍ່ຖືກຕ້ອງ
**ກວດສອບ**:
```python
payment = BCELOnePayPayment.objects.last()
print(f"Amount in DB: {payment.amount}")

# ຊອກຫາ amount tag (54) ໃນ QR data
qr = payment.qr_code_data
idx = qr.find('54')
if idx != -1:
    length = int(qr[idx+2:idx+4])
    amount = qr[idx+4:idx+4+length]
    print(f"Amount in QR: {amount}")
```

---

## 🔧 Troubleshooting Commands

```bash
# ລຶບ QR codes ເກົ່າທັງໝົດ
rm media/payments/qr_codes/*

# ສ້າງ QR ໃໝ່
python manage.py shell -c "
from events.models import BCELOnePayPayment
p = BCELOnePayPayment.objects.last()
p.generate_qr_code()
print(f'✅ QR generated: {p.qr_code_image.url}')
"

# ກວດສອບ server logs
tail -20 nohup.out

# Restart server
# CTRL+C ໃນ terminal ທີ່ໃຊ້ runserver
# ຫຼັງຈາກນັ້ນ:
python manage.py runserver
```

---

## 📞 ຕິດຕໍ່ສະໜັບສະໜູນ

### ຖ້າຍັງມີບັນຫາ, ຕິດຕໍ່:

**BCEL OnePay Support**:
- Email: support@bcel.com.la
- Phone: +856 21 213 536
- ເວັບໄຊ: https://www.bcel.com.la

**ຂໍເອກະສານເຫຼົ່ານີ້**:
1. BCEL OnePay QR Code Specification
2. EMVCo Tag Numbers for BCEL
3. Merchant ID Format Requirements
4. Sandbox Environment Access

---

## 📚 ເອກະສານອ້າງອີງ

- `EMVCO_QR_IMPLEMENTATION.md` - ລາຍລະອຽດການ implement
- `QR_DEBUG_GUIDE.md` - ວິທີແກ້ບັນຫາ
- `IMPLEMENTATION_SUMMARY.md` - ສະຫຼຸບທັງໝົດ
- `PAYMENT_QR_FIX.md` - ປະຫວັດການແກ້ໄຂ

---

## ✅ Checklist

ກ່ອນທົດສອບກັບ BCEL One, ກວດສອບວ່າ:

- [ ] Server ເຮັດວຽກ (http://localhost:8000)
- [ ] QR Code ສະແດງໃນໜ້າ payment
- [ ] Merchant ID ສະແດງ: mch5f0e5f1d512c8
- [ ] Amount ຖືກຕ້ອງ
- [ ] QR data ເປັນ EMVCo format (ເລີ່ມຕົ້ນດ້ວຍ "0002")
- [ ] QR image ຖືກ save ແລ້ວໃນ media/payments/qr_codes/
- [ ] Timer ເຮັດວຽກ (ນັບຖອຍຫຼັງຈາກ 15:00)

---

**ພ້ອມທົດສອບແລ້ວ!** 🚀

ສະແກນ QR Code ດ້ວຍ BCEL One app ແລະແຈ້ງຜົນທັນທີ! 📱
