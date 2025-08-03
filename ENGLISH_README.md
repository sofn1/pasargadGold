
# Admin, Writer, and Customer Dashboards – API Documentation (English)

This documentation includes all developed endpoints across the three dashboards.

---

## 🔐 Authentication
All endpoints require token-based authentication (`IsAuthenticated`).

---

## 🧑‍💼 Admin Dashboard

### 1. `GET /api/admin/dashboard/summary/`
- **Description:** Get site-wide statistics.
- **Response:** Total users, sellers, writers, etc.

### 2. `GET /api/admin/dashboard/sellers/`
- **Description:** List all sellers with product/order count.

### 3. `GET /api/admin/dashboard/writers/`
- **Description:** List all writers and their permissions.

### 4. `GET/PATCH /api/admin/dashboard/comments/flagged/`
- **Description:** List and update flagged comments.

### 5. `GET /api/admin/dashboard/alerts/low-stock/`
- **Description:** List products with stock ≤ 5.

### 6. `GET /api/admin/dashboard/payments/failed/`
- **Description:** Get latest failed payments.

### 7. `POST /api/admin/dashboard/sellers/create/`
- **Description:** Create a new seller.

### 8. `PUT/DELETE /api/admin/dashboard/sellers/<id>/`
- **Description:** Update/delete a seller.

### 9. `PATCH /api/admin/dashboard/writers/<writer_id>/permissions/`
- **Description:** Update writer's permissions.

### 10. `GET/POST/PATCH/DELETE /api/admin/dashboard/admins/manage/`
- **Description:** Manage admin accounts and superadmin roles.

### 11. `POST /api/admin/dashboard/admins/invite/`
- **Description:** Invite new admin via email token.

### 12. `POST /api/admin/dashboard/admins/activate/`
- **Description:** Activate admin using token.

### 13. `PATCH /api/admin/dashboard/admins/suspend/`
- **Description:** Suspend admin temporarily.

### 14. `GET /api/admin/dashboard/logs/`
- **Description:** Filter admin logs by date/admin.

### 15. `GET /api/admin/dashboard/logs/export/`
- **Description:** Export logs to Excel.

### 16. `GET /api/admin/dashboard/growth/`
- **Description:** Admin registration summary.

### 17. `POST /api/admin/dashboard/impersonate/`
- **Description:** Impersonate another admin.

---

## ✍️ Writer Dashboard

### 1. `GET /api/writer/dashboard/summary/`
- **Description:** View content stats (blogs/news).

### 2. `POST /api/writer/dashboard/seo/`
- **Description:** Get SEO + AI readability analysis.

### 3. `GET /api/writer/dashboard/trends/`
- **Description:** Time-series of content publishing.

### 4. `GET /api/writer/dashboard/top/`
- **Description:** Get top blogs/news by views.

### 5. `GET /api/writer/dashboard/export/`
- **Description:** Export writer content to Excel.

### 6. `GET/POST /api/writer/blogs/`
- **Description:** List/Create blogs.

### 7. `GET/PUT/DELETE /api/writer/blogs/<id>/`
- **Description:** Retrieve, update or delete blog.

### 8. `GET/POST /api/writer/news/`
- **Description:** List/Create news articles.

### 9. `GET/PUT/DELETE /api/writer/news/<id>/`
- **Description:** Retrieve, update or delete news.

### 10. `GET /api/writer/blogs/<blog_id>/comments/`
- **Description:** List comments on a blog.

### 11. `GET /api/writer/news/<news_id>/comments/`
- **Description:** List comments on a news post.

### 12. `POST /api/writer/comments/<comment_id>/reply/`
- **Description:** Reply to a comment.

---

## 👤 Customer Dashboard

### 1. `GET /api/customer/dashboard/notifications/`
- **Description:** List customer notifications.

### 2. `PATCH /api/customer/dashboard/notifications/<id>/mark-read/`
- **Description:** Mark a notification as read.

### 3. `GET /api/customer/dashboard/tickets/`
- **Description:** List customer support tickets.

### 4. `POST /api/customer/dashboard/tickets/`
- **Description:** Create a new ticket.

### 5. `GET /api/customer/dashboard/tickets/<id>/`
- **Description:** View ticket details + replies.

### 6. `POST /api/customer/dashboard/tickets/<id>/reply/`
- **Description:** Reply to a ticket.

---

All endpoints support pagination and error handling using standard DRF responses.


---

## 📁 Apps Documentation Continued

### 🔐 accounts

- `/api/accounts/register/` – Register a new user.
- `/api/accounts/login/` – Log in with phone number and password.
- `/api/accounts/profile/` – View and update profile (Authenticated).
- `/api/accounts/change-password/` – Change password.
- `/api/accounts/send-code/` – Send verification code for login/reset.
- `/api/accounts/verify-code/` – Verify received code.

### 📝 blogs

- `/api/blogs/` – Public list of blogs.
- `/api/blogs/<id>/` – Blog detail view.
- `/api/blogs/<id>/like/` – Like a blog (Authenticated).
- `/api/blogs/writer/` – Create or list blogs for the writer.
- `/api/blogs/writer/<id>/` – Update/delete blog by writer.

### 💬 comments

- `/api/comments/` – Post new comment (Authenticated).
- `/api/comments/<id>/like/` – Like or unlike comment.
- `/api/comments/<content_type>/<object_id>/` – Get comments for object.

### 🧾 logs

- `/api/admin/dashboard/logs/` – View admin logs with filters (date/admin).
- `/api/admin/dashboard/logs/export/` – Export logs to Excel.
- `/api/admin/dashboard/logs/summary/` – Activity summary for charting.

### 🗞️ news

- `/api/news/` – Public list of news.
- `/api/news/<id>/` – News detail view.
- `/api/news/writer/` – Create or list news for writer.
- `/api/news/writer/<id>/` – Update/delete news by writer.

### 🛒 orders

- `/api/orders/` – List or create order (Authenticated).
- `/api/orders/<id>/` – Retrieve/update/delete specific order.

### 💳 payments

- `/api/payments/failures/` – List recent failed payments (Admin only).

### 🛍️ products

- `/api/products/` – List available products.
- `/api/products/<id>/` – Retrieve/update/delete product.
- `/api/products/seller/` – Create/list seller's products.
- `/api/products/low-stock/` – Low-stock alert for admin.

### ⚙️ core settings & global routes

- `core/settings.py` – Project-wide settings, integrations, middleware.
- `core/urls.py` – Root API router including all apps.
