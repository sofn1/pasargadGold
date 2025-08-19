# core/products/management/commands/seed_categories.py
from django.core.management import BaseCommand
from bson import ObjectId
from django.conf import settings

# If you already have a Mongo client factory, import and use it instead.
from pymongo import MongoClient, UpdateOne, ASCENDING

# ====== CONFIGURE THIS IF NEEDED ======
MONGODB_URI = getattr(settings, "MONGO_URI", "mongodb://admin:securepassword@127.0.0.1:27017/goldsite?authSource=admin")
MONGODB_DB = getattr(settings, "MONGO_DB_NAME", "goldsite")
CATEGORIES_COLLECTION = getattr(settings, "MONGODB_CATEGORIES_COLLECTION", "product_categories")
# =============================================

def get_db():
    client = MongoClient(MONGODB_URI)
    return client[MONGODB_DB]

class Command(BaseCommand):
    help = "Seeds MongoDB product categories with hierarchy, parentId, and subCategories."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Show what would be written without committing changes.")

    def handle(self, *args, **opts):
        dry = opts["dry_run"]
        db = get_db()
        col = db[CATEGORIES_COLLECTION]

        # Ensure unique index on slug (so admin mistakes can’t create dupes)
        col.create_index([("slug", ASCENDING)], unique=True)

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

        # Pass 1: upsert all categories without parentId first (collect _ids by slug)
        slug_to_id = {}
        ops = []
        # for fa, en, slug, parent_slug in data:
        #     doc_filter = {"slug": slug}
        #     base_doc = {
        #         "name": fa,
        #         "englishName": en,
        #         "slug": slug,
        #         "is_active": True,
        #     }
        #     # Do not set parentId yet (second pass), ensure subCategories exists
        #     set_on_insert = {**base_doc, "subCategories": []}

        #     ops.append(
        #         UpdateOne(
        #             doc_filter,
        #             {
        #                 "$set": base_doc,
        #                 "$setOnInsert": set_on_insert
        #             },
        #             upsert=True
        #         )
        #     )

        # base_doc is fine:
        base_doc = {
            "name": fa,
            "englishName": en,
            "slug": slug,
            "is_active": True,
        }

        # only insert-time fields go here:
        set_on_insert = {
            "subCategories": []
        }

        ops.append(
            UpdateOne(
                {"slug": slug},
                {
                    "$set": base_doc,
                    "$setOnInsert": set_on_insert
                },
                upsert=True
            )
        )

        if dry:
            self.stdout.write(self.style.WARNING("[DRY-RUN] Would upsert base categories (without parentId)"))
        else:
            res = col.bulk_write(ops, ordered=False)
            self.stdout.write(self.style.SUCCESS(f"Upserted {res.upserted_count} (inserted) / matched {res.matched_count} categories."))

        # Load IDs after upsert
        for doc in col.find({}, {"slug": 1}):
            slug_to_id[doc["slug"]] = doc["_id"]

        # Pass 2: set parentId and maintain subCategories
        updates = []
        for fa, en, slug, parent_slug in data:
            if parent_slug:
                child_id = slug_to_id.get(slug)
                parent_id = slug_to_id.get(parent_slug)
                if not child_id or not parent_id:
                    self.stdout.write(self.style.ERROR(f"Missing parent/child for slug='{slug}', parent='{parent_slug}'"))
                    continue

                updates.append(
                    UpdateOne(
                        {"_id": child_id},
                        {"$set": {"parentId": parent_id}}
                    )
                )
                # push child into parent's subCategories if not already there
                updates.append(
                    UpdateOne(
                        {"_id": parent_id},
                        {"$addToSet": {"subCategories": child_id}}
                    )
                )
            else:
                # ensure roots have no parentId (or explicitly set to None)
                cat_id = slug_to_id.get(slug)
                if cat_id:
                    updates.append(
                        UpdateOne({"_id": cat_id}, {"$unset": {"parentId": ""}})
                    )

        if dry:
            self.stdout.write(self.style.WARNING("[DRY-RUN] Would set parentId and subCategories relationships"))
        else:
            if updates:
                res2 = col.bulk_write(updates, ordered=False)
                self.stdout.write(self.style.SUCCESS("Parent/child relationships updated."))

        self.stdout.write(self.style.SUCCESS("✅ Category seeding complete."))
