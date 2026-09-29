export default function ItemCard({ item }) {
  return (
    <a className="card" href={item.whatsapp_url} target="_blank" rel="noopener noreferrer">
      <div className="card-media">
        {item.image_url ? (
          <img src={item.image_url} alt={item.name} />
        ) : (
          <div className="card-media-fallback">{item.category}</div>
        )}
      </div>
      <div className="card-body">
        <span className="card-category">{item.category}</span>
        <h3 className="card-name">{item.name}</h3>
        {item.description && <p className="card-desc">{item.description}</p>}
        <div className="card-footer">
          {item.price != null && <span className="card-price">Rs. {item.price.toLocaleString()}</span>}
          <span className="card-cta">Order on WhatsApp</span>
        </div>
      </div>
    </a>
  );
}
