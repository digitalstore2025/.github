# Marketplace Bundle (Next.js App Router)

## 0️⃣ المتطلبات
- Node.js 18+
- حساب Stripe
- Git (اختياري)
- Vercel (للنشر)

---

## 1️⃣ إنشاء المشروع (Next.js – App Router)
```bash
npx create-next-app@latest marketplace
cd marketplace
npm run dev
```

اختر:
- App Router: ✅
- TypeScript: ❌
- Tailwind: ❌
- ESLint: ✅

---

## 2️⃣ تثبيت الاعتمادات
```bash
npm install stripe
```

---

## 3️⃣ متغيرات البيئة
**.env.local**
```bash
STRIPE_SECRET_KEY=sk_live_xxxxxxxxx
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_xxxxxxxxx
```

---

## 4️⃣ هيكل المشروع النهائي
```
app/
├─ layout.jsx
├─ page.jsx
├─ globals.css
├─ success/page.jsx
├─ cart/page.jsx
├─ login/page.jsx
├─ api/checkout/route.js
├─ components/
│  ├─ ProductGrid.jsx
│  ├─ ProductCard.jsx
│  ├─ BottomNav.jsx
├─ hooks/
│  ├─ useCart.js
│  ├─ useFavorites.js
├─ context/
│  └─ AuthContext.jsx
├─ lib/
│  └─ products.js
└─ manifest.json
```

---

## 5️⃣ الأكواد (انسخ كما هي)

### app/layout.jsx
```jsx
import { AuthProvider } from "./context/AuthContext";
import "./globals.css";

export const metadata = {
  title: "Marketplace",
  description: "عرض إطلاق – دفع آمن – تسليم فوري"
};

export default function RootLayout({ children }) {
  return (
    <html lang="ar">
      <body>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
```

---

### app/page.jsx
```jsx
import { getProducts } from "./lib/products";
import ProductGrid from "./components/ProductGrid";
import BottomNav from "./components/BottomNav";

export default async function Home() {
  const products = await getProducts();

  return (
    <main className="app">
      <h1>عرض إطلاق</h1>
      <ProductGrid products={products} />
      <BottomNav />
    </main>
  );
}
```

---

### app/lib/products.js
```js
export async function getProducts() {
  const res = await fetch("https://fakestoreapi.com/products", {
    cache: "no-store"
  });
  return res.json();
}
```

---

### components/ProductGrid.jsx
```jsx
import ProductCard from "./ProductCard";

export default function ProductGrid({ products }) {
  return (
    <div className="grid">
      {products.map(p => (
        <ProductCard key={p.id} product={p} />
      ))}
    </div>
  );
}
```

---

### components/ProductCard.jsx
```jsx
"use client";
import { useCart } from "../hooks/useCart";

export default function ProductCard({ product }) {
  const { add } = useCart();

  return (
    <article className="card">
      <img src={product.image} alt={product.title} />
      <h4>{product.title.slice(0, 20)}…</h4>
      <strong>{product.price} $</strong>
      <button onClick={() => add(product)}>
        أضف للسلة
      </button>
    </article>
  );
}
```

---

### hooks/useCart.js
```js
import { useState, useEffect } from "react";

export function useCart() {
  const [cart, setCart] = useState(
    JSON.parse(localStorage.getItem("cart") || "[]")
  );

  useEffect(() => {
    localStorage.setItem("cart", JSON.stringify(cart));
  }, [cart]);

  const add = (product) => {
    setCart(c => {
      const f = c.find(i => i.id === product.id);
      if (f) {
        return c.map(i =>
          i.id === product.id ? { ...i, qty: i.qty + 1 } : i
        );
      }
      return [...c, { ...product, qty: 1 }];
    });
  };

  const total = cart.reduce((s, i) => s + i.price * i.qty, 0);

  return { cart, add, total };
}
```

---

### app/cart/page.jsx
```jsx
"use client";
import { useCart } from "../../hooks/useCart";

export default function CartPage() {
  const { cart, total } = useCart();

  if (!cart.length) return <p>السلة فارغة</p>;

  const checkout = async () => {
    const res = await fetch("/api/checkout", {
      method: "POST",
      body: JSON.stringify({ items: cart })
    });
    const { url } = await res.json();
    window.location.href = url;
  };

  return (
    <main>
      <h2>سلة الشراء</h2>
      {cart.map(i => (
        <div key={i.id}>
          {i.title} × {i.qty}
        </div>
      ))}
      <strong>الإجمالي: {total}</strong>
      <button onClick={checkout}>الدفع</button>
    </main>
  );
}
```

---

### app/api/checkout/route.js
```js
import Stripe from "stripe";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

export async function POST(req) {
  const { items } = await req.json();

  const session = await stripe.checkout.sessions.create({
    payment_method_types: ["card"],
    line_items: items.map(i => ({
      price_data: {
        currency: "usd",
        product_data: { name: i.title },
        unit_amount: Math.round(i.price * 100)
      },
      quantity: i.qty
    })),
    mode: "payment",
    success_url: `${req.headers.get("origin")}/success`,
    cancel_url: `${req.headers.get("origin")}/cart`
  });

  return Response.json({ url: session.url });
}
```

---

### app/success/page.jsx
```jsx
export default function Success() {
  return (
    <main>
      <h1>تم الدفع بنجاح</h1>
      <p>سيصلك تأكيد على البريد</p>
    </main>
  );
}
```

---

### context/AuthContext.jsx
```jsx
"use client";
import { createContext, useContext, useState } from "react";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  const login = email => {
    setUser({ email });
    localStorage.setItem("user", email);
  };

  return (
    <AuthContext.Provider value={{ user, login }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
```

---

### components/BottomNav.jsx
```jsx
"use client";
import Link from "next/link";

export default function BottomNav() {
  return (
    <nav className="bottom">
      <Link href="/">🏠</Link>
      <Link href="/cart">🛒</Link>
      <Link href="/login">👤</Link>
    </nav>
  );
}
```

---

### app/manifest.json
```json
{
  "name": "Marketplace",
  "short_name": "Shop",
  "start_url": "/",
  "display": "standalone",
  "theme_color": "#22c55e",
  "background_color": "#ffffff"
}
```

---

## 6️⃣ التشغيل
```bash
npm run dev
```

---

## 7️⃣ النشر (Vercel)
```bash
git init
git add .
git commit -m "Marketplace ready"
```

- ارفع على GitHub
- اربط بـ Vercel
- أضف متغيرات البيئة
- Deploy

---

✅ النتيجة
- متجر يعمل
- دفع حقيقي
- سلة
- مستخدم
- PWA
- جاهز للبيع الآن
