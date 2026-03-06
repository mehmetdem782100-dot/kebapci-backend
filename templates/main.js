// Müşteri tarafı
let cart = [];

function fetchProducts() {
  fetch('/api/products')
    .then(res => res.json())
    .then(data => {
      let list = document.getElementById('product-list');
      list.innerHTML = '';
      data.forEach(p => {
        let div = document.createElement('div');
        div.innerHTML = `<b>${p.title}</b> - ${p.price} TL - Stok: ${p.stock} 
        <button onclick="addToCart('${p.code}',1)">Sepete Ekle</button>`;
        list.appendChild(div);
      });
    });
}

function addToCart(code, qty) {
  let found = cart.find(c=>c.code===code);
  if(found) found.qty+=qty; else cart.push({code, qty});
  renderCart();
}

function renderCart() {
  let div = document.getElementById('cart');
  div.innerHTML = cart.map(c=>`${c.code} x ${c.qty}`).join('<br>');
}

document.getElementById('order-btn').onclick = function(){
  let name = prompt("İsim girin:");
  let phone = prompt("Telefon girin:");
  let address = prompt("Adres girin:");
  if(!name || !phone || !address){ alert("Alanlar boş bırakılamaz"); return; }
  fetch('/api/orders',{
    method:'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({name,phone,address,items:cart})
  }).then(r=>r.json()).then(res=>{
    if(res.ok){ alert("Siparişiniz alındı! Sipariş ID: "+res.order_id); cart=[]; renderCart(); }
    else alert("Hata: "+JSON.stringify(res));
  });
}

fetchProducts();

// Admin JS (fetch, display orders/products) — örnek
