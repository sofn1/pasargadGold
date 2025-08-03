
# مستندات API داشبورد مشتری، نویسنده و ادمین (فارسی)

این مستند شامل تمام اندپوینت‌های توسعه‌یافته برای هر نقش کاربری است.

---

## 🔐 احراز هویت
تمام اندپوینت‌ها نیاز به توکن دارند (`IsAuthenticated`).

---

## 🧑‍💼 داشبورد ادمین

### ۱. `GET /api/admin/dashboard/summary/`
- **توضیح:** آمار کلی سایت.

### ۲. `GET /api/admin/dashboard/sellers/`
- **توضیح:** لیست فروشندگان و تعداد محصولات/سفارشات.

### ۳. `GET /api/admin/dashboard/writers/`
- **توضیح:** لیست نویسندگان و سطح دسترسی آن‌ها.

### ۴. `GET/PATCH /api/admin/dashboard/comments/flagged/`
- **توضیح:** مدیریت کامنت‌های ریپورت شده.

### ۵. `GET /api/admin/dashboard/alerts/low-stock/`
- **توضیح:** هشدار موجودی کم برای محصولات.

### ۶. `GET /api/admin/dashboard/payments/failed/`
- **توضیح:** پرداخت‌های ناموفق اخیر.

### ۷. `POST /api/admin/dashboard/sellers/create/`
- **توضیح:** ساخت فروشنده جدید.

### ۸. `PUT/DELETE /api/admin/dashboard/sellers/<id>/`
- **توضیح:** ویرایش یا حذف فروشنده.

### ۹. `PATCH /api/admin/dashboard/writers/<writer_id>/permissions/`
- **توضیح:** ویرایش سطح دسترسی نویسنده.

### ۱۰. `GET/POST/PATCH/DELETE /api/admin/dashboard/admins/manage/`
- **توضیح:** مدیریت ادمین‌ها.

### ۱۱. `POST /api/admin/dashboard/admins/invite/`
- **توضیح:** دعوت ادمین جدید از طریق ایمیل.

### ۱۲. `POST /api/admin/dashboard/admins/activate/`
- **توضیح:** فعالسازی نقش ادمین با توکن.

### ۱۳. `PATCH /api/admin/dashboard/admins/suspend/`
- **توضیح:** تعلیق یا محدودیت ادمین.

### ۱۴. `GET /api/admin/dashboard/logs/`
- **توضیح:** مشاهده لاگ‌ها با فیلتر تاریخ یا ادمین.

### ۱۵. `GET /api/admin/dashboard/logs/export/`
- **توضیح:** خروجی اکسل از لاگ‌ها.

### ۱۶. `GET /api/admin/dashboard/growth/`
- **توضیح:** گزارش رشد تعداد ادمین‌ها.

### ۱۷. `POST /api/admin/dashboard/impersonate/`
- **توضیح:** ورود موقت به حساب ادمین دیگر.

---

## ✍️ داشبورد نویسنده

### ۱. `GET /api/writer/dashboard/summary/`
- **توضیح:** خلاصه فعالیت نویسنده.

### ۲. `POST /api/writer/dashboard/seo/`
- **توضیح:** تحلیل SEO و خوانایی.

### ۳. `GET /api/writer/dashboard/trends/`
- **توضیح:** تحلیل زمانی تولید محتوا.

### ۴. `GET /api/writer/dashboard/top/`
- **توضیح:** بهترین محتواها بر اساس بازدید.

### ۵. `GET /api/writer/dashboard/export/`
- **توضیح:** خروجی اکسل محتواها.

### ۶. `GET/POST /api/writer/blogs/`
- **توضیح:** لیست و ایجاد بلاگ.

### ۷. `GET/PUT/DELETE /api/writer/blogs/<id>/`
- **توضیح:** مشاهده، ویرایش یا حذف بلاگ.

### ۸. `GET/POST /api/writer/news/`
- **توضیح:** لیست و ایجاد خبر.

### ۹. `GET/PUT/DELETE /api/writer/news/<id>/`
- **توضیح:** مشاهده، ویرایش یا حذف خبر.

### ۱۰. `GET /api/writer/blogs/<blog_id>/comments/`
- **توضیح:** لیست کامنت‌های بلاگ.

### ۱۱. `GET /api/writer/news/<news_id>/comments/`
- **توضیح:** لیست کامنت‌های خبر.

### ۱۲. `POST /api/writer/comments/<comment_id>/reply/`
- **توضیح:** پاسخ به یک کامنت.

---

## 👤 داشبورد مشتری

### ۱. `GET /api/customer/dashboard/notifications/`
- **توضیح:** لیست اعلان‌های مشتری.

### ۲. `PATCH /api/customer/dashboard/notifications/<id>/mark-read/`
- **توضیح:** خوانده‌شدن اعلان.

### ۳. `GET /api/customer/dashboard/tickets/`
- **توضیح:** لیست تیکت‌های پشتیبانی.

### ۴. `POST /api/customer/dashboard/tickets/`
- **توضیح:** ثبت تیکت جدید.

### ۵. `GET /api/customer/dashboard/tickets/<id>/`
- **توضیح:** مشاهده جزئیات تیکت.

### ۶. `POST /api/customer/dashboard/tickets/<id>/reply/`
- **توضیح:** ارسال پاسخ به تیکت.

---

تمام اندپوینت‌ها از پاسخ‌های استاندارد DRF پشتیبانی می‌کنند.


---

## 📁 ادامه مستندات اپلیکیشن‌ها

### 🔐 accounts (حساب کاربری)

- `/api/accounts/register/` – ثبت‌نام کاربر جدید.
- `/api/accounts/login/` – ورود با شماره موبایل و رمز عبور.
- `/api/accounts/profile/` – مشاهده و ویرایش پروفایل (نیاز به احراز هویت).
- `/api/accounts/change-password/` – تغییر رمز عبور.
- `/api/accounts/send-code/` – ارسال کد تأیید برای ورود یا بازیابی.
- `/api/accounts/verify-code/` – بررسی صحت کد تأیید.

### 📝 blogs (وبلاگ‌ها)

- `/api/blogs/` – لیست عمومی وبلاگ‌ها.
- `/api/blogs/<id>/` – جزئیات یک وبلاگ خاص.
- `/api/blogs/<id>/like/` – پسندیدن یک وبلاگ (نیاز به احراز هویت).
- `/api/blogs/writer/` – لیست و ایجاد وبلاگ توسط نویسنده.
- `/api/blogs/writer/<id>/` – بروزرسانی یا حذف وبلاگ توسط نویسنده.

### 💬 comments (نظرات)

- `/api/comments/` – ارسال نظر جدید (نیاز به احراز هویت).
- `/api/comments/<id>/like/` – لایک یا لغو لایک یک نظر.
- `/api/comments/<content_type>/<object_id>/` – دریافت نظرات مرتبط با یک شیء خاص.

### 🧾 logs (لاگ‌ها)

- `/api/admin/dashboard/logs/` – مشاهده لاگ‌های مدیر با فیلتر تاریخ یا نام مدیر.
- `/api/admin/dashboard/logs/export/` – خروجی گرفتن لاگ‌ها به فایل اکسل.
- `/api/admin/dashboard/logs/summary/` – خلاصه عملکرد برای نمودار.

### 🗞️ news (اخبار)

- `/api/news/` – لیست عمومی اخبار.
- `/api/news/<id>/` – جزئیات یک خبر خاص.
- `/api/news/writer/` – لیست و ایجاد خبر توسط نویسنده.
- `/api/news/writer/<id>/` – بروزرسانی یا حذف خبر توسط نویسنده.

### 🛒 orders (سفارش‌ها)

- `/api/orders/` – لیست یا ثبت سفارش جدید (نیاز به احراز هویت).
- `/api/orders/<id>/` – دریافت، بروزرسانی یا حذف یک سفارش خاص.

### 💳 payments (پرداخت‌ها)

- `/api/payments/failures/` – لیست پرداخت‌های ناموفق (فقط برای ادمین).

### 🛍️ products (محصولات)

- `/api/products/` – مشاهده لیست محصولات.
- `/api/products/<id>/` – مشاهده، بروزرسانی یا حذف یک محصول.
- `/api/products/seller/` – لیست و ایجاد محصولات فروشنده.
- `/api/products/low-stock/` – هشدار کمبود موجودی برای مدیر.

### ⚙️ core (تنظیمات اصلی پروژه)

- `core/settings.py` – تنظیمات پروژه، لاگ‌ها، توکن، ایمیل و ...
- `core/urls.py` – روت اصلی API که همه اپلیکیشن‌ها را شامل می‌شود.
