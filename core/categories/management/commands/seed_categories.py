# -*- coding: utf-8 -*-
from django.core.management import BaseCommand
from django.db import transaction
from categories.models import Category


class Command(BaseCommand):
    help = "Seeds Category rows in Postgres with hierarchy (parent) based on a flat list (fa, en, slug, parent_slug)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be written without committing changes.",
        )
        parser.add_argument(
            "--update-names",
            action="store_true",
            help="Also update existing categories' name/english_name/is_active=True if they differ.",
        )

    def handle(self, *args, **opts):
        dry = opts["dry_run"]
        update_names = opts["update_names"]

        # --------------------------
        # Category data (flattened)
        # Each item: (fa_name, en_name, slug, parent_slug_or_None)
        # --------------------------
        data = [

            # 1. Women’s Products (محصولات زنانه)
            ("محصولات زنانه", "Women’s Products", "womens-products", None),

            ("گردنبند زنانه", "Women’s Necklaces", "womens-necklaces", "womens-products"),
            ("گردنبند کارتیر", "Cartier Necklace", "cartier-necklace", "womens-necklaces"),
            ("گردنبند چشم و نظر", "Evil Eye Necklace", "evil-eye-necklace", "womens-necklaces"),
            ("گردنبند مروارید", "Pearl Necklace", "pearl-necklace", "womens-necklaces"),
            ("گردنبند صلیب", "Cross Necklace", "cross-necklace", "womens-necklaces"),
            ("گردنبند فیروزه", "Turquoise Necklace", "turquoise-necklace", "womens-necklaces"),
            ("گردنبند ونکلیف", "Van Cleef Necklace", "van-cleef-necklace", "womens-necklaces"),
            ("گردنبند زنجیری", "Chain Necklace", "chain-necklace", "womens-necklaces"),
            ("گردنبند ظریف", "Delicate Necklace", "delicate-necklace", "womens-necklaces"),
            ("گردنبند قلب", "Heart Necklace", "heart-necklace", "womens-necklaces"),
            ("گردنبند عقیق", "Agate Necklace", "agate-necklace", "womens-necklaces"),
            ("گردنبند سنگی", "Stone Necklace", "stone-necklace", "womens-necklaces"),
            ("گردنبند چرمی", "Leather Necklace", "leather-necklace", "womens-necklaces"),

            ("دستبند زنانه", "Women’s Bracelets", "womens-bracelets", "womens-products"),
            ("دستبند کارتیر", "Cartier Bracelet", "cartier-bracelet", "womens-bracelets"),
            ("دستبند چرم", "Leather Bracelet", "leather-bracelet", "womens-bracelets"),
            ("دستبند زنجیری", "Chain Bracelet", "chain-bracelet", "womens-bracelets"),
            ("دستبند سنگی", "Stone Bracelet", "stone-bracelet", "womens-bracelets"),
            ("دستبند بافت", "Woven Bracelet", "woven-bracelet", "womens-bracelets"),
            ("دستبند مهره ای", "Beaded Bracelet", "beaded-bracelet", "womens-bracelets"),
            ("دستبند فیروزه", "Turquoise Bracelet", "turquoise-bracelet", "womens-bracelets"),
            ("دستبند مروارید", "Pearl Bracelet", "pearl-bracelet", "womens-bracelets"),
            ("دستبند چشم نظر", "Evil Eye Bracelet", "evil-eye-bracelet", "womens-bracelets"),
            ("دستبند النگویی", "Bangle Bracelet", "bangle-bracelet", "womens-bracelets"),
            ("دستبند پهن", "Wide Bracelet", "wide-bracelet", "womens-bracelets"),
            ("دستبند ونکلیف", "Van Cleef Bracelet", "van-cleef-bracelet", "womens-bracelets"),

            ("انگشتر زنانه", "Women’s Rings", "womens-rings", "womens-products"),
            ("انگشتر نگین دار", "Gemstone Ring", "gemstone-ring", "womens-rings"),
            ("انگشتر بدون نگین", "Plain Ring", "plain-ring", "womens-rings"),
            ("انگشتر کارتیر", "Cartier Ring", "cartier-ring", "womens-rings"),
            ("انگشتر فیروزه", "Turquoise Ring", "turquoise-ring", "womens-rings"),
            ("انگشتر عقیق", "Agate Ring", "agate-ring", "womens-rings"),
            ("انگشتر یاقوت", "Ruby Ring", "ruby-ring", "womens-rings"),
            ("حلقه ازدواج", "Wedding Band", "wedding-band", "womens-rings"),
            ("انگشتر برلیان", "Diamond Ring", "diamond-ring", "womens-rings"),
            ("انگشتر مروارید", "Pearl Ring", "pearl-ring", "womens-rings"),
            ("انگشتر فانتزی", "Fancy Ring", "fancy-ring", "womens-rings"),

            ("زنجیر زنانه", "Women’s Chains", "womens-chains", "womens-products"),
            ("زنجیر کارتیه", "Cartier Chain", "cartier-chain", "womens-chains"),
            ("زنجیر رولو", "Rolo Chain", "rolo-chain", "womens-chains"),
            ("زنجیر فلامینگو", "Flamingo Chain", "flamingo-chain", "womens-chains"),

            ("گوشواره زنانه", "Women’s Earrings", "womens-earrings", "womens-products"),
            ("گوشواره کارتیر", "Cartier Earring", "cartier-earring", "womens-earrings"),
            ("گوشواره حلقه ای", "Hoop Earring", "hoop-earring", "womens-earrings"),
            ("گوشواره میخی", "Stud Earring", "stud-earring", "womens-earrings"),
            ("گوشواره بخیه ای", "Threader Earring", "threader-earring", "womens-earrings"),
            ("گوشواره زنجیری", "Chain Earring", "chain-earring", "womens-earrings"),
            ("گوشواره مروارید", "Pearl Earring", "pearl-earring", "womens-earrings"),
            ("گوشواره آویزی", "Dangle Earring", "dangle-earring", "womens-earrings"),
            ("گوشواره کلیپسی", "Clip-on Earring", "clip-on-earring", "womens-earrings"),
            ("ایرکاف", "Ear Cuff", "ear-cuff", "womens-earrings"),

            ("النگو زنانه", "Women’s Bangles", "womens-bangles", "womens-products"),
            ("النگو باریک", "Thin Bangle", "thin-bangle", "womens-bangles"),
            ("النگو دستبندی", "Bracelet Bangle", "bracelet-bangle", "womens-bangles"),

            ("اکسسوری", "Women’s Accessories", "womens-accessories", "womens-products"),
            ("آویز", "Pendant", "pendant", "womens-accessories"),
            ("آویز ساعت", "Watch Charm", "watch-charm", "womens-accessories"),
            ("پابند", "Anklet", "anklet", "womens-accessories"),
            ("بند عینک", "Eyeglass Chain", "eyeglass-chain", "womens-accessories"),
            ("پیرسینگ", "Piercings", "piercings", "womens-accessories"),
            ("پیرسینگ بینی", "Nose Piercing", "nose-piercing", "piercings"),
            ("پیرسینگ ناف", "Navel Piercing", "navel-piercing", "piercings"),
            ("پیرسینگ گوش", "Ear Piercing", "ear-piercing", "piercings"),

            ("ست و نیم‌ست", "Sets", "sets", "womens-products"),
            ("نیم‌ست", "Half Set", "half-set", "sets"),
            ("ست کامل", "Full Set", "full-set", "sets"),

            # 2. Men’s Products (محصولات مردانه)
            ("محصولات مردانه", "Men’s Products", "mens-products", None),

            ("گردنبند مردانه", "Men’s Necklaces", "mens-necklaces", "mens-products"),
            ("گردنبند زنجیری", "Men’s Chain Necklace", "mens-chain-necklace", "mens-necklaces"),
            ("گردنبند سنگی", "Men’s Stone Necklace", "mens-stone-necklace", "mens-necklaces"),
            ("گردنبند کارتیر", "Men’s Cartier Necklace", "mens-cartier-necklace", "mens-necklaces"),

            ("زنجیر مردانه", "Men’s Chains", "mens-chains", "mens-products"),
            ("زنجیر کارتیر", "Men’s Cartier Chain", "mens-cartier-chain", "mens-chains"),

            ("دستبند مردانه", "Men’s Bracelets", "mens-bracelets", "mens-products"),
            ("دستبند چرم", "Men’s Leather Bracelet", "mens-leather-bracelet", "mens-bracelets"),
            ("دستبند کارتیر", "Men’s Cartier Bracelet", "mens-cartier-bracelet", "mens-bracelets"),
            ("دستبند زنجیری", "Men’s Chain Bracelet", "mens-chain-bracelet", "mens-bracelets"),
            ("دستبند سنگی", "Men’s Stone Bracelet", "mens-stone-bracelet", "mens-bracelets"),
            ("دستبند فیروزه", "Men’s Turquoise Bracelet", "mens-turquoise-bracelet", "mens-bracelets"),

            ("انگشتر مردانه", "Men’s Rings", "mens-rings", "mens-products"),
            ("انگشتر عقیق", "Men’s Agate Ring", "mens-agate-ring", "mens-rings"),
            ("انگشتر فیروزه", "Men’s Turquoise Ring", "mens-turquoise-ring", "mens-rings"),
            ("انگشتر بدون نگین", "Men’s Plain Ring", "mens-plain-ring", "mens-rings"),
            ("انگشتر نگین دار", "Men’s Gemstone Ring", "mens-gemstone-ring", "mens-rings"),

            ("اکسسوری مردانه", "Men’s Accessories", "mens-accessories", "mens-products"),
            ("دکمه سردست", "Cufflinks", "cufflinks", "mens-accessories"),
            ("بند عینک", "Men’s Eyeglass Chain", "mens-eyeglass-chain", "mens-accessories"),

            ("محصولات آماده ارسال مردانه", "Men’s Ready To Ship", "mens-ready-to-ship", "mens-products"),

            # 3. Kids (بچه‌گانه)
            ("بچه‌گانه", "Kids", "kids", None),

            ("محصولات دخترانه", "Girls’ Jewelry", "girls-jewelry", "kids"),
            ("گردنبند دخترانه", "Girls’ Necklace", "girls-necklace", "girls-jewelry"),
            ("دستبند دخترانه", "Girls’ Bracelet", "girls-bracelet", "girls-jewelry"),
            ("سنجاق سینه دخترانه", "Girls’ Brooch", "girls-brooch", "girls-jewelry"),
            ("همه محصولات دخترانه", "All Girls’ Products", "all-girls-products", "girls-jewelry"),

            ("محصولات پسرانه", "Boys’ Jewelry", "boys-jewelry", "kids"),
            ("گردنبند پسرانه", "Boys’ Necklace", "boys-necklace", "boys-jewelry"),
            ("دستبند پسرانه", "Boys’ Bracelet", "boys-bracelet", "boys-jewelry"),
            ("سنجاق سینه پسرانه", "Boys’ Brooch", "boys-brooch", "boys-jewelry"),
            ("همه محصولات پسرانه", "All Boys’ Products", "all-boys-products", "boys-jewelry"),

            # 4. Product Type (نوع محصول)
            ("نوع محصول", "Product Type", "product-type", None),
            ("کم اجرت", "Low Cost", "low-cost", "product-type"),
            ("آب‌شده", "Melted Gold", "melted-gold", "product-type"),
            ("نقره", "Silver", "silver", "product-type"),

            # 5. Parasteh World (دنیای پرسته)
            ("دنیای پرسته", "Parasteh World", "parasteh-world", None),
            ("درباره پرسته", "About Parasteh", "about-parasteh", "parasteh-world"),
            ("بلاگ پرسته", "Parasteh Blog", "parasteh-blog", "parasteh-world"),
            ("شعب پرسته", "Parasteh Branches", "parasteh-branches", "parasteh-world"),
            ("طراحی اسم", "Name Design", "name-design", "parasteh-world"),
            ("حکاکی", "Engraving", "engraving", "parasteh-world"),
            ("گردنبند طلا", "Gold Necklaces", "gold-necklaces", "parasteh-world"),
            ("دستبند طلا", "Gold Bracelets", "gold-bracelets", "parasteh-world"),
            ("گوشواره طلا", "Gold Earrings", "gold-earrings", "parasteh-world"),
            ("انگشتر طلا", "Gold Rings", "gold-rings", "parasteh-world"),
            ("زنجیر طلا", "Gold Chains", "gold-chains", "parasteh-world"),
            ("النگو طلا", "Gold Bangles", "gold-bangles", "parasteh-world"),
            ("پلاک طلا", "Gold Pendants", "gold-pendants", "parasteh-world"),
            ("لایف‌استایل", "Lifestyle", "lifestyle", "parasteh-world"),
            ("هودی", "Hoodie", "hoodie", "parasteh-world"),
            ("شمع", "Candle", "candle", "parasteh-world"),
            ("جعبه جواهرات", "Jewelry Box", "jewelry-box", "parasteh-world"),
            ("اجرت کم", "Low Wage", "low-wage", "parasteh-world"),

            # 6. Collections (کالکشن‌ها)
            ("کالکشن‌ها", "Collections", "collections", None),
            ("کالکشن نسیما", "Nasima Collection", "nasima-collection", "collections"),
            ("کالکشن صحرا", "Sahra Collection", "sahra-collection", "collections"),
            ("کالکشن دلبر", "Delbar Collection", "delbar-collection", "collections"),
            ("کالکشن آرونا", "Arona Collection", "arona-collection", "collections"),
            ("کالکشن ایشتار", "Ishtar Collection", "ishtar-collection", "collections"),
            ("کالکشن خورشید", "Sun Collection", "sun-collection", "collections"),
            ("کالکشن تاج محل", "Taj Mahal Collection", "taj-mahal-collection", "collections"),
            ("کالکشن تخت جمشید", "Persepolis Collection", "persepolis-collection", "collections"),
            ("کالکشن هستی", "Hasti Collection", "hasti-collection", "collections"),

            # 7. Shopping Guide (راهنمای خرید)
            ("راهنمای خرید", "Shopping Guide", "shopping-guide", None),
            ("هدیه", "Gifts", "gifts", "shopping-guide"),
            ("حراج پرسته", "Parasteh Sale", "parasteh-sale", "shopping-guide"),
            ("مینا کاری", "Enamel", "enamel", "shopping-guide"),
            ("زیورآلات صدف", "Shell Jewelry", "shell-jewelry", "shopping-guide"),
            ("زیورآلات چشم و نظر", "Evil Eye Jewelry", "evil-eye-jewelry", "shopping-guide"),
            ("مروارید", "Pearl", "pearl-jewelry", "shopping-guide"),
            ("هدیه مردانه", "Men’s Gifts", "mens-gifts", "shopping-guide"),
            ("خرید نقره", "Buy Silver", "buy-silver", "shopping-guide"),
            ("شمع", "Gift Candle", "gift-candle", "shopping-guide"),
            ("جعبه جواهرات", "Gift Jewelry Box", "gift-jewelry-box", "shopping-guide"),
            ("هدیه سفارشی", "Custom Gifts", "custom-gifts", "shopping-guide"),
            ("حکاکی", "Custom Engraving", "custom-engraving", "shopping-guide"),
            ("نماد ماه تولد", "Birth Sign", "birth-sign", "shopping-guide"),
            ("حروف", "Letters", "letters", "shopping-guide"),

            ("هدیه بر اساس قیمت", "Gifts by Price", "gifts-by-price", "shopping-guide"),
            ("تا 1 میلیون تومان", "Under 1M", "under-1m", "gifts-by-price"),
            ("تا 1.5 میلیون تومان", "Under 1.5M", "under-1-5m", "gifts-by-price"),
            ("تا 2 میلیون تومان", "Under 2M", "under-2m", "gifts-by-price"),
            ("تا 3 میلیون تومان", "Under 3M", "under-3m", "gifts-by-price"),

            ("مناسبت‌ها", "Occasions", "occasions", "shopping-guide"),
            ("کادو روز مادر", "Mother’s Day Gift", "mothers-day-gift", "occasions"),
            ("کادو ولنتاین", "Valentine’s Gift", "valentines-gift", "occasions"),

            ("راهنمای خرید", "Buying Guide", "buying-guide", "shopping-guide"),
            ("مراقبت از پیرسینگ", "Piercing Care", "piercing-care", "shopping-guide"),
            ("راهنمای سایز", "Size Guide", "size-guide", "shopping-guide"),
        ]

        # ---------- Plan / Lookups ----------
        all_existing = {c.slug: c for c in Category.objects.all()}
        to_create = []
        will_update = []
        for fa, en, slug, parent_slug in data:
            obj = all_existing.get(slug)
            if obj is None:
                to_create.append(Category(name=fa, english_name=en, slug=slug, is_active=True))
            else:
                if update_names:
                    changed = False
                    if obj.name != fa:
                        obj.name = fa
                        changed = True
                    if obj.english_name != en:
                        obj.english_name = en
                        changed = True
                    if not obj.is_active:
                        obj.is_active = True
                        changed = True
                    if changed:
                        will_update.append(obj)

        # ---------- DRY RUN ----------
        if dry:
            created_count = len(to_create)
            updated_count = len(will_update) if update_names else 0

            # Parent link plan
            parent_fix = 0
            for fa, en, slug, parent_slug in data:
                child_exists = slug in all_existing or any(x.slug == slug for x in to_create)
                if not child_exists:
                    continue
                if parent_slug:
                    parent_exists = parent_slug in all_existing or any(x.slug == parent_slug for x in to_create)
                    if not parent_exists:
                        self.stdout.write(self.style.ERROR(f"[DRY] Missing parent for slug='{slug}', parent='{parent_slug}'"))
                    else:
                        parent_fix += 1
                else:
                    parent_fix += 1  # ensure root

            self.stdout.write(self.style.WARNING(f"[DRY-RUN] Would create: {created_count}, update: {updated_count}, set parent links: ~{parent_fix}"))
            self.stdout.write(self.style.SUCCESS("✅ Dry-run complete (no DB writes)."))
            return

        # ---------- WRITE ----------
        with transaction.atomic():
            # Pass 1: create + update names (if requested)
            if to_create:
                Category.objects.bulk_create(to_create, ignore_conflicts=True)
            if will_update:
                Category.objects.bulk_update(will_update, ["name", "english_name", "is_active"])

            # Refresh map after writes
            all_existing = {c.slug: c for c in Category.objects.all()}

            # Pass 2: set parents
            to_link = []
            for fa, en, slug, parent_slug in data:
                child = all_existing.get(slug)
                if not child:
                    continue
                desired_parent = all_existing.get(parent_slug) if parent_slug else None
                desired_parent_id = desired_parent.id if desired_parent else None
                if child.parent_id != desired_parent_id:
                    child.parent = desired_parent
                    to_link.append(child)
            if to_link:
                Category.objects.bulk_update(to_link, ["parent"])

        self.stdout.write(self.style.SUCCESS("✅ Category seeding complete."))
