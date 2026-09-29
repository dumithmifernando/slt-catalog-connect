const BASE = "/api";

export async function fetchItems(category) {
  const url = category ? `${BASE}/items?category=${encodeURIComponent(category)}` : `${BASE}/items`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to load items");
  return res.json();
}

export async function fetchCategories() {
  const res = await fetch(`${BASE}/categories`);
  if (!res.ok) throw new Error("Failed to load categories");
  return res.json();
}
