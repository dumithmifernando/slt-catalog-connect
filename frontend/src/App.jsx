import { useEffect, useState } from "react";
import { fetchItems, fetchCategories } from "./api";
import ItemCard from "./components/ItemCard";

export default function App() {
  const [items, setItems] = useState([]);
  const [categories, setCategories] = useState([]);
  const [activeCategory, setActiveCategory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchCategories().then(setCategories).catch(() => {});
  }, []);

  useEffect(() => {
    setLoading(true);
    setError(null);
    fetchItems(activeCategory)
      .then(setItems)
      .catch(() => setError("Couldn't load the catalog. Is the backend running?"))
      .finally(() => setLoading(false));
  }, [activeCategory]);

  return (
    <div className="page">
      <header className="header">
        <span className="brand">SLT Catalog</span>
        <p className="tagline">Pick a plan, package, or device — order it straight on WhatsApp.</p>
      </header>

      <nav className="filters">
        <button className={activeCategory === null ? "filter active" : "filter"} onClick={() => setActiveCategory(null)}>
          All
        </button>
        {categories.map((cat) => (
          <button
            key={cat}
            className={activeCategory === cat ? "filter active" : "filter"}
            onClick={() => setActiveCategory(cat)}
          >
            {cat}
          </button>
        ))}
      </nav>

      <main>
        {loading && <p className="status">Loading…</p>}
        {error && <p className="status status-error">{error}</p>}
        {!loading && !error && items.length === 0 && <p className="status">No items yet.</p>}

        <div className="grid">
          {items.map((item) => (
            <ItemCard key={item.id} item={item} />
          ))}
        </div>
      </main>
    </div>
  );
}
