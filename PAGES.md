git add .
git commit -m 'serna modifications'
git push


# 🎯 Frontend-Visible Pages (Dynamic Base URL)

Use these endpoints in your browser or frontend testing tool.

## Set your base server address first:

```bash
export BASE_URL=http://localhost:8000
```

### `login`
- **App**: `accounts`
- **Test**: `$BASE_URL/login`

### `register/customer`
- **App**: `accounts`
- **Test**: `$BASE_URL/register/customer`

### `register/seller`
- **App**: `accounts`
- **Test**: `$BASE_URL/register/seller`

### `register/writer`
- **App**: `accounts`
- **Test**: `$BASE_URL/register/writer`

### `admin-dashboard/admin-logs`
- **App**: `admin_dashboard`
- **Test**: `$BASE_URL/frontend/admin-logs`

### `admin-dashboard/admins/create`
- **App**: `admin_dashboard`
- **Test**: `$BASE_URL/frontend/admins/create`

### `admin-dashboard/failed-payments`
- **App**: `admin_dashboard`
- **Test**: `$BASE_URL/frontend/failed-payments`

### `admin-dashboard/flagged-comments`
- **App**: `admin_dashboard`
- **Test**: `$BASE_URL/frontend/flagged-comments`

### `admin-dashboard/growth`
- **App**: `admin_dashboard`
- **Test**: `$BASE_URL/frontend/growth`

### `admin-dashboard/impersonate`
- **App**: `admin_dashboard`
- **Test**: `$BASE_URL/frontend/impersonate`

### `admin-dashboard/low-stock`
- **App**: `admin_dashboard`
- **Test**: `$BASE_URL/frontend/low-stock`

### `admin-dashboard/manage-admins`
- **App**: `admin_dashboard`
- **Test**: `$BASE_URL/frontend/manage-admins`

### `admin-dashboard/sellers`
- **App**: `admin_dashboard`
- **Test**: `$BASE_URL/frontend/sellers`

### `admin-dashboard/sellers/<int:id>/update`
- **App**: `admin_dashboard`
- **Test**: `$BASE_URL/frontend/sellers/<int:id>/update`

### `admin-dashboard/sellers/create`
- **App**: `admin_dashboard`
- **Test**: `$BASE_URL/frontend/sellers/create`

### `admin-dashboard/summary`
- **App**: `admin_dashboard`
- **Test**: `$BASE_URL/frontend/summary`

### `admin-dashboard/writers`
- **App**: `admin_dashboard`
- **Test**: `$BASE_URL/frontend/writers`

### `api/blogs`
- **App**: `core`
- **Test**: `$BASE_URL/api/blogs`

### `api/news`
- **App**: `core`
- **Test**: `$BASE_URL/api/news`

### `api/products`
- **App**: `core`
- **Test**: `$BASE_URL/api/products`

### `admin/tickets/<int:ticket_id>/reply`
- **App**: `customer_dashboard`
- **Test**: `$BASE_URL/admin/tickets/<int:ticket_id>/reply`

### `cart`
- **App**: `customer_dashboard`
- **Test**: `$BASE_URL/cart`

### `frontend/addresses`
- **App**: `customer_dashboard`
- **Test**: `$BASE_URL/frontend/addresses`

### `frontend/cart`
- **App**: `customer_dashboard`
- **Test**: `$BASE_URL/frontend/cart`

### `frontend/invoice/<int:order_id>`
- **App**: `customer_dashboard`
- **Test**: `$BASE_URL/frontend/invoice/<int:order_id>`

### `frontend/notifications`
- **App**: `customer_dashboard`
- **Test**: `$BASE_URL/frontend/notifications`

### `frontend/orders`
- **App**: `customer_dashboard`
- **Test**: `$BASE_URL/frontend/orders`

### `frontend/profile`
- **App**: `customer_dashboard`
- **Test**: `$BASE_URL/frontend/profile`

### `frontend/recommended`
- **App**: `customer_dashboard`
- **Test**: `$BASE_URL/frontend/recommended`

### `frontend/support-tickets`
- **App**: `customer_dashboard`
- **Test**: `$BASE_URL/frontend/support-tickets`

### `frontend/wishlist`
- **App**: `customer_dashboard`
- **Test**: `$BASE_URL/frontend/wishlist`

### `notifications`
- **App**: `customer_dashboard`
- **Test**: `$BASE_URL/notifications`

### `notifications/<int:pk>/read`
- **App**: `customer_dashboard`
- **Test**: `$BASE_URL/notifications/<int:pk>/read`

### `notifications/unread`
- **App**: `customer_dashboard`
- **Test**: `$BASE_URL/notifications/unread`

### `profile`
- **App**: `customer_dashboard`
- **Test**: `$BASE_URL/profile`

### `support`
- **App**: `customer_dashboard`
- **Test**: `$BASE_URL/support`

### `support-tickets`
- **App**: `customer_dashboard`
- **Test**: `$BASE_URL/support-tickets`

### `support-tickets/replies`
- **App**: `customer_dashboard`
- **Test**: `$BASE_URL/support-tickets/replies`

### `tickets`
- **App**: `customer_dashboard`
- **Test**: `$BASE_URL/tickets`

### `tickets/<int:ticket_id>/reply`
- **App**: `customer_dashboard`
- **Test**: `$BASE_URL/tickets/<int:ticket_id>/reply`

### `add-to-cart/<int:id>`
- **App**: `frontend`
- **Test**: `$BASE_URL/add-to-cart/<int:id>`

### `blogs`
- **App**: `frontend`
- **Test**: `$BASE_URL/blogs`

### `blogs/<int:id>`
- **App**: `frontend`
- **Test**: `$BASE_URL/blogs/<int:id>`

### `cart`
- **App**: `frontend`
- **Test**: `$BASE_URL/cart`

### `checkout`
- **App**: `frontend`
- **Test**: `$BASE_URL/checkout`

### `login`
- **App**: `frontend`
- **Test**: `$BASE_URL/login`

### `news`
- **App**: `frontend`
- **Test**: `$BASE_URL/news`

### `news/<int:id>`
- **App**: `frontend`
- **Test**: `$BASE_URL/news/<int:id>`

### `notifications`
- **App**: `frontend`
- **Test**: `$BASE_URL/notifications`

### `product/<int:id>`
- **App**: `frontend`
- **Test**: `$BASE_URL/product/<int:id>`

### `products`
- **App**: `frontend`
- **Test**: `$BASE_URL/products`

### `profile`
- **App**: `frontend`
- **Test**: `$BASE_URL/profile`

### `register`
- **App**: `frontend`
- **Test**: `$BASE_URL/register`

### `cart`
- **App**: `orders`
- **Test**: `$BASE_URL/cart`

### `cart/<int:pk>`
- **App**: `orders`
- **Test**: `$BASE_URL/cart/<int:pk>`

### `low-stock-products`
- **App**: `seller_dashboard`
- **Test**: `$BASE_URL/low-stock-products`

### `products/low-stock`
- **App**: `seller_dashboard`
- **Test**: `$BASE_URL/products/low-stock`

### `products/top`
- **App**: `seller_dashboard`
- **Test**: `$BASE_URL/products/top`

### `top-products`
- **App**: `seller_dashboard`
- **Test**: `$BASE_URL/top-products`

### `blogs`
- **App**: `writer_dashboard`
- **Test**: `$BASE_URL/blogs`

### `blogs/<int:blog_id>/comments`
- **App**: `writer_dashboard`
- **Test**: `$BASE_URL/blogs/<int:blog_id>/comments`

### `blogs/<int:pk>`
- **App**: `writer_dashboard`
- **Test**: `$BASE_URL/blogs/<int:pk>`

### `blogs/create`
- **App**: `writer_dashboard`
- **Test**: `$BASE_URL/blogs/create`

### `frontend/blogs`
- **App**: `writer_dashboard`
- **Test**: `$BASE_URL/frontend/blogs`

### `frontend/blogs/<int:pk>/delete`
- **App**: `writer_dashboard`
- **Test**: `$BASE_URL/frontend/blogs/<int:pk>/delete`

### `frontend/blogs/<int:pk>/edit`
- **App**: `writer_dashboard`
- **Test**: `$BASE_URL/frontend/blogs/<int:pk>/edit`

### `frontend/blogs/create`
- **App**: `writer_dashboard`
- **Test**: `$BASE_URL/frontend/blogs/create`

### `frontend/news`
- **App**: `writer_dashboard`
- **Test**: `$BASE_URL/frontend/news`

### `frontend/news/<int:pk>/delete`
- **App**: `writer_dashboard`
- **Test**: `$BASE_URL/frontend/news/<int:pk>/delete`

### `frontend/news/<int:pk>/edit`
- **App**: `writer_dashboard`
- **Test**: `$BASE_URL/frontend/news/<int:pk>/edit`

### `frontend/news/create`
- **App**: `writer_dashboard`
- **Test**: `$BASE_URL/frontend/news/create`

### `news`
- **App**: `writer_dashboard`
- **Test**: `$BASE_URL/news`

### `news/<int:news_id>/comments`
- **App**: `writer_dashboard`
- **Test**: `$BASE_URL/news/<int:news_id>/comments`

### `news/<int:pk>`
- **App**: `writer_dashboard`
- **Test**: `$BASE_URL/news/<int:pk>`

### `news/create`
- **App**: `writer_dashboard`
- **Test**: `$BASE_URL/news/create`

