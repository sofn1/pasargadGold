from django.db import models
from django.utils.text import slugify
from django.core.validators import RegexValidator

HEX_COLOR_RE = r"^#(?:[0-9a-fA-F]{3}){1,2}$"


class Tag(models.Model):
    name = models.CharField("نام", max_length=64, unique=True)
    slug = models.SlugField("اسلاگ", max_length=64, unique=True, help_text="فقط حروف انگلیسی و خط تیره")
    color = models.CharField(
        "رنگ (اختیاری)",
        max_length=7,
        blank=True,
        validators=[RegexValidator(HEX_COLOR_RE, message="فرمت رنگ باید #RRGGBB باشد")],
        help_text="مثال: #1C39BB",
    )
    description = models.CharField("توضیح کوتاه (اختیاری)", max_length=160, blank=True)
    created_at = models.DateTimeField("ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("به‌روزرسانی", auto_now=True)

    class Meta:
        verbose_name = "برچسب"
        verbose_name_plural = "برچسب‌ها"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # اگر اسلاگ خالی بود از نام بساز
        if not self.slug and self.name:
            base = slugify(self.name)
            candidate = base
            i = 2
            while Tag.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base}-{i}"
                i += 1
            self.slug = candidate
        super().save(*args, **kwargs)
