import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Prasanna Chowdary - Restaurant Bill Generator",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(255, 99, 71, 0.15), transparent 25%),
        radial-gradient(circle at 90% 20%, rgba(255, 193, 7, 0.16), transparent 25%),
        linear-gradient(135deg, #fff7ed 0%, #fff 48%, #fef3c7 100%);
}

.main-title {
    text-align: center;
    font-size: 44px;
    font-weight: 800;
    margin-top: 10px;
    margin-bottom: 4px;
    background: linear-gradient(90deg, #ff4b2b, #ff8c00, #e91e63);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: titleGlow 2.5s ease-in-out infinite alternate;
}

.subtitle {
    text-align: center;
    color: #666;
    font-size: 17px;
    margin-bottom: 25px;
}

@keyframes titleGlow {
    from { transform: translateY(0px); }
    to { transform: translateY(-4px); }
}

.hero {
    background: linear-gradient(135deg, #ff512f, #f09819);
    color: white;
    padding: 22px;
    border-radius: 22px;
    text-align: center;
    box-shadow: 0 12px 30px rgba(240, 152, 25, 0.28);
    animation: floatCard 3s ease-in-out infinite;
    margin-bottom: 25px;
}

.hero h2 {
    margin: 0;
    font-size: 27px;
}

.hero p {
    margin: 7px 0 0;
    opacity: 0.95;
}

@keyframes floatCard {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
}

.section-card {
    background: rgba(255,255,255,0.82);
    border: 1px solid rgba(255, 152, 0, 0.18);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.07);
    margin-bottom: 18px;
}

.bill-card {
    background: white;
    border-radius: 22px;
    padding: 26px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.10);
    border-top: 7px solid #ff6b35;
}

.grand-total {
    background: linear-gradient(90deg, #ff512f, #dd2476);
    color: white;
    padding: 18px;
    border-radius: 16px;
    text-align: center;
    font-size: 29px;
    font-weight: 800;
    margin-top: 15px;
    box-shadow: 0 8px 22px rgba(221,36,118,0.25);
}

.item-pill {
    background: #fff7ed;
    border-left: 5px solid #ff7a00;
    border-radius: 10px;
    padding: 10px 14px;
    margin: 7px 0;
}

.footer {
    text-align: center;
    color: #777;
    padding: 20px 0 5px;
    font-size: 14px;
}

div.stButton > button {
    border-radius: 12px;
    border: none;
    font-weight: 700;
    padding: 10px 18px;
    transition: 0.25s;
}

div.stButton > button:hover {
    transform: scale(1.03);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fff1e6, #fff8f0);
}

@media (max-width: 768px) {
    .main-title { font-size: 31px; }
    .subtitle { font-size: 14px; }
}
</style>
""", unsafe_allow_html=True)

# -------------------- DATA --------------------
MENU = {
    "🍕 Margherita Pizza": 250,
    "🍔 Classic Burger": 180,
    "🍟 French Fries": 100,
    "🍝 White Sauce Pasta": 220,
    "🌮 Veg Tacos": 160,
    "🥪 Club Sandwich": 150,
    "🍗 Crispy Chicken": 280,
    "🍚 Veg Fried Rice": 170,
    "🥤 Cold Drink": 60,
    "🍨 Ice Cream": 90
}

# -------------------- HEADER --------------------
st.markdown(
    '<div class="main-title">Prasanna Chowdary - Restaurant Bill Generator</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Create a beautiful restaurant bill in a few simple steps 🍽️</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="hero">
    <h2>🍔 Welcome to Prasanna's Food Corner! 🍕</h2>
    <p>Select your favorite food, choose quantities, apply tax or discount, and generate your final bill.</p>
</div>
""", unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.header("⚙️ Bill Settings")

    customer_name = st.text_input("👤 Customer Name", value="Guest")
    table_number = st.text_input("🪑 Table Number", value="T-01")

    st.divider()

    tax_rate = st.number_input(
        "🧾 Tax (%)",
        min_value=0.0,
        max_value=50.0,
        value=5.0,
        step=0.5
    )

    discount_rate = st.number_input(
        "🏷️ Discount (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=1.0
    )

    st.divider()
    st.info("💡 Tip: Add your items first, then generate the bill.")

# -------------------- ITEM SELECTION --------------------
st.markdown("### 🍽️ Select Food Items")

selected_items = []

cols = st.columns(2)

for index, (item, price) in enumerate(MENU.items()):
    with cols[index % 2]:
        with st.container(border=True):
            selected = st.checkbox(f"{item} — ₹{price}", key=f"select_{index}")

            if selected:
                quantity = st.number_input(
                    "Quantity",
                    min_value=1,
                    max_value=20,
                    value=1,
                    step=1,
                    key=f"qty_{index}"
                )

                item_total = price * quantity
                selected_items.append({
                    "item": item,
                    "price": price,
                    "quantity": quantity,
                    "total": item_total
                })

# -------------------- CALCULATION --------------------
subtotal = sum(item["total"] for item in selected_items)
discount_amount = subtotal * discount_rate / 100
after_discount = subtotal - discount_amount
tax_amount = after_discount * tax_rate / 100
grand_total = after_discount + tax_amount

st.markdown("### 📊 Bill Calculation")

c1, c2, c3, c4 = st.columns(4)

c1.metric("🍴 Items", len(selected_items))
c2.metric("💰 Subtotal", f"₹{subtotal:,.2f}")
c3.metric("🏷️ Discount", f"₹{discount_amount:,.2f}")
c4.metric("🧾 Tax", f"₹{tax_amount:,.2f}")

# -------------------- BILL --------------------
st.markdown("### 🧾 Final Bill")

if selected_items:
    bill_rows = ""
    for item in selected_items:
        bill_rows += f"""
        <div class="item-pill">
            <b>{item['item']}</b><br>
            ₹{item['price']:,.2f} × {item['quantity']} = <b>₹{item['total']:,.2f}</b>
        </div>
        """

    now = datetime.now().strftime("%d-%m-%Y %I:%M %p")

    st.markdown(f"""
    <div class="bill-card">
        <h2 style="text-align:center;">🍽️ PRASANNA'S FOOD CORNER</h2>
        <p style="text-align:center;color:#777;">Restaurant Bill</p>
        <hr>
        <p><b>Customer:</b> {customer_name}</p>
        <p><b>Table:</b> {table_number}</p>
        <p><b>Date & Time:</b> {now}</p>
        <hr>
        {bill_rows}
        <hr>
        <p style="text-align:right;"><b>Subtotal:</b> ₹{subtotal:,.2f}</p>
        <p style="text-align:right;"><b>Discount ({discount_rate:.1f}%):</b> -₹{discount_amount:,.2f}</p>
        <p style="text-align:right;"><b>Tax ({tax_rate:.1f}%):</b> +₹{tax_amount:,.2f}</p>
        <div class="grand-total">GRAND TOTAL: ₹{grand_total:,.2f}</div>
        <p style="text-align:center;margin-top:18px;">✨ Thank you for dining with us! ✨</p>
    </div>
    """, unsafe_allow_html=True)

    st.balloons()

    st.download_button(
        "📥 Download Bill Summary",
        data=(
            f"PRASANNA'S FOOD CORNER\n"
            f"Restaurant Bill\n\n"
            f"Customer: {customer_name}\n"
            f"Table: {table_number}\n"
            f"Date & Time: {now}\n\n"
            + "\n".join(
                f"{i['item']} | ₹{i['price']:.2f} x {i['quantity']} = ₹{i['total']:.2f}"
                for i in selected_items
            )
            + f"\n\nSubtotal: ₹{subtotal:.2f}"
              f"\nDiscount: ₹{discount_amount:.2f}"
              f"\nTax: ₹{tax_amount:.2f}"
              f"\nGrand Total: ₹{grand_total:.2f}\n"
        ),
        file_name="prasanna_chowdary_restaurant_bill.txt",
        mime="text/plain"
    )

else:
    st.info("👆 Please select at least one food item to generate your bill.")

st.markdown("""
<div class="footer">
    🚀 Built with Python + Streamlit | Prasanna Chowdary | Beginner-Friendly Project
</div>
""", unsafe_allow_html=True)
