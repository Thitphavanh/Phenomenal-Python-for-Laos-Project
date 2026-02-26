# QR Code Debug Guide - คำแนะนำການແก้ไขปัญหา QR Code

## ວິທີກວດສອບ QR Code Data

### 1. ກວດສອບ QR Data ໃນ Django Shell

```bash
python manage.py shell
```

```python
from events.models import BCELOnePayPayment

# ເອົາ payment ຫຼ້າສຸດ
payment = BCELOnePayPayment.objects.last()

# ສະແດງ QR data
print("QR Code Data:")
print(payment.qr_code_data)
print()

# ແຍກວິເຄາະ EMVCo tags
data = payment.qr_code_data
print("EMVCo Tag Analysis:")
print(f"00 (Payload Format): {data[0:6]}")
print(f"01 (Init Method): {data[6:12]}")
print(f"29 (Merchant Info): {data[12:38]}")  # May vary by length
print(f"52 (Category): {data[38:46]}")
print(f"53 (Currency): {data[46:53]}")
print(f"54 (Amount): starts at position ~53")
print()

# ສະແດງຂໍ້ມູນອື່ນໆ
print(f"Merchant ID: {payment.merchant_id}")
print(f"Amount: {payment.amount}")
print(f"Currency: {payment.currency}")
print(f"Status: {payment.status}")
print(f"QR Image: {payment.qr_code_image.url if payment.qr_code_image else 'Not generated'}")
```

### 2. ສ້າງ QR Code ໃໝ່

```python
# ສ້າງ QR code ໃໝ່ສຳລັບ payment ທີ່ມີຢູ່ແລ້ວ
payment = BCELOnePayPayment.objects.last()
payment.generate_qr_code()
print(f"New QR generated: {payment.qr_code_image.url}")
```

### 3. ທົດສອບ CRC Calculation

```python
# Test CRC calculation
payment = BCELOnePayPayment.objects.last()
test_data = "000201010212292400160mch5f0e5f1d512c852040000530341854085000.005802LA5916Python for Laos6009Vientiane624901380cbf6237f-fa4f-41e7-baf9-bd6304"

crc = payment._calculate_crc16(test_data.encode('utf-8'))
print(f"CRC: {crc}")
```

## ວິທີອ່ານ EMVCo QR String

### Tag-Length-Value Format

```
000201
├── 00: Tag (Payload Format Indicator)
├── 02: Length (2 characters)
└── 01: Value (version 01)

010212
├── 01: Tag (Point of Initiation Method)
├── 02: Length (2 characters)
└── 12: Value (dynamic QR)

292400160mch5f0e5f1d512c8
├── 29: Tag (Merchant Account Information)
├── 24: Length (24 characters)
└── 00160mch5f0e5f1d512c8: Value
    ├── 00: Sub-tag (Merchant ID)
    ├── 16: Sub-length (16 chars)
    └── mch5f0e5f1d512c8: Merchant ID
```

### ຕົວຢ່າງການວິເຄາະ

```python
def parse_emvco_qr(qr_string):
    """Parse EMVCo QR string"""
    i = 0
    tags = {}

    while i < len(qr_string) - 4:  # -4 for final CRC
        try:
            tag = qr_string[i:i+2]
            length = int(qr_string[i+2:i+4])
            value = qr_string[i+4:i+4+length]

            tags[tag] = {
                'length': length,
                'value': value
            }

            i += 4 + length
        except:
            break

    return tags

# ໃຊ້ງານ
payment = BCELOnePayPayment.objects.last()
parsed = parse_emvco_qr(payment.qr_code_data)

for tag, data in parsed.items():
    print(f"Tag {tag}: {data['value']}")
```

## ການແກ້ບັນຫາທົ່ວໄປ

### ບັນຫາ 1: QR Code ບໍ່ສະແດງ

**ກວດສອບ:**
```python
payment = BCELOnePayPayment.objects.last()
print(payment.qr_code_image)  # Should show path
print(payment.qr_code_data)   # Should show EMVCo string
```

**ແກ້ໄຂ:**
```python
# Re-generate QR
payment.generate_qr_code()
```

### ບັນຫາ 2: QR Code Data ບໍ່ຖືກຕ້ອງ

**ກວດສອບແຕ່ລະສ່ວນ:**
```python
payment = BCELOnePayPayment.objects.last()
qr = payment.qr_code_data

# Check tags
checks = {
    'Payload Format': qr.startswith('0002'),
    'Init Method': '0102' in qr,
    'Merchant Info': '29' in qr,
    'Currency LAK': '5303418' in qr,
    'Country LA': '5802LA' in qr,
    'Merchant Name': 'Python for Laos' in qr,
    'City': 'Vientiane' in qr,
}

for check, result in checks.items():
    print(f"{check}: {'✅' if result else '❌'}")
```

### ບັນຫາ 3: BCEL One ສະແກນບໍ່ໄດ້

**ສິ່ງທີ່ຕ້ອງກວດ:**

1. **QR Error Correction Level**
```python
# ໃນ models.py, ປັບໃນ generate_qr_code():
error_correction=qrcode.constants.ERROR_CORRECT_H  # Try HIGH
```

2. **QR Size**
```python
# ເພີ່ມຂະໜາດ
box_size=15  # ແທນທີ່ຈະເປັນ 10
```

3. **Merchant Tag**
```python
# ລອງປ່ຽນ tag 29 ເປັນ tag ອື່ນ (26, 27, 28)
# ໃນ _build_emvco_qr_string():
components.append(f"26{merchant_info_length}{merchant_info}")  # ແທນ 29
```

### ບັນຫາ 4: Amount ບໍ່ຖືກຕ້ອງ

**ກວດສອບ:**
```python
payment = BCELOnePayPayment.objects.last()
print(f"Amount in DB: {payment.amount}")
print(f"Amount in QR: {payment.qr_code_data}")

# Find amount tag (54)
qr = payment.qr_code_data
idx = qr.find('54')
if idx != -1:
    length = int(qr[idx+2:idx+4])
    amount = qr[idx+4:idx+4+length]
    print(f"Amount in QR tag: {amount}")
```

## ການທົດສອບ QR Code ດ້ວຍ Online Tools

### 1. Decode QR Code
ອັບໂຫຼດ QR image ໄປທີ່:
- https://zxing.org/w/decode
- https://www.qr-code-generator.com/qr-code-scanner/

### 2. ກວດສອບ EMVCo Format
```python
# Export QR data to text file for analysis
payment = BCELOnePayPayment.objects.last()

with open('qr_data.txt', 'w') as f:
    f.write(payment.qr_code_data)

print("QR data exported to qr_data.txt")
```

## ຕົວຢ່າງ QR Data ທີ່ຖືກຕ້ອງ

```
000201                           # Payload Format: 01
010212                           # Init Method: 12 (dynamic)
292400160mch5f0e5f1d512c8        # Merchant: mch5f0e5f1d512c8
52040000                         # Category: 0000
5303418                          # Currency: 418 (LAK)
54085000.00                      # Amount: 5000.00
5802LA                           # Country: LA
5916Python for Laos              # Merchant Name
6009Vientiane                    # City
6249013...                       # Reference (payment UUID)
6304XXXX                         # CRC checksum
```

## ຄຳສັ່ງທີ່ເປັນປະໂຫຍດ

```bash
# ເບິ່ງ media files
ls -lh media/payments/qr_codes/

# ລຶບ QR codes ເກົ່າທັງໝົດ
rm media/payments/qr_codes/*

# ສ້າງ QR ໃໝ່ສຳລັບທຸກ payment
python manage.py shell -c "
from events.models import BCELOnePayPayment
for p in BCELOnePayPayment.objects.all():
    p.generate_qr_code()
    print(f'Generated QR for payment {p.payment_id}')
"

# ກວດສອບ server logs
tail -f nohup.out  # ຖ້າໃຊ້ nohup
# ຫຼື ເບິ່ງໃນ terminal ທີ່ run server
```

## Contact BCEL OnePay

ຖ້າຍັງມີບັນຫາ, ກະລຸນາຕິດຕໍ່ BCEL ເພື່ອ:
1. ຂໍເອກະສານ QR Code specifications
2. ຢືນຢັນ Merchant ID format
3. ຂໍຂໍ້ມູນ tag numbers ທີ່ຖືກຕ້ອງ
4. ທົດສອບ QR Code ກັບ BCEL OnePay sandbox

## ສະຫຼຸບ Checklist

ເມື່ອມີບັນຫາ QR Code, ກວດສອບຕາມລຳດັບ:

- [ ] QR Code image ສ້າງແລ້ວແລະສະແດງໄດ້
- [ ] QR data ມີຂໍ້ມູນຄົບຖ້ວນ (merchant, amount, currency)
- [ ] EMVCo format ຖືກຕ້ອງ (tags ຄົບ)
- [ ] CRC checksum ຖືກຄິດໄລ່ຖືກຕ້ອງ
- [ ] Merchant ID ຖືກຕ້ອງ
- [ ] Amount ຕົງກັນກັບຖານຂໍ້ມູນ
- [ ] Currency code = 418 (LAK)
- [ ] Country code = LA
- [ ] QR size ແລະ error correction ເໝາະສົມ
- [ ] ທົດສອບສະແກນດ້ວຍ BCEL One app

**ຖ້າທຸກຢ່າງຖືກຕ້ອງແຕ່ຍັງສະແກນບໍ່ໄດ້, ອາດຈະຕ້ອງປັບ tag numbers ຫຼື format ຕາມທີ່ BCEL ກຳນົດ** 🔍
