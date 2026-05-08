
... 
... # --- МАТЕМАТИЧНІ МОДЕЛІ ---
... 
def membrana(Gv, Cv, Xob, Xp):
...     """
...     Розрахунок мембранного вузла.
...     Gv - вхідний потік, Cv - вхідна концентрація
...     Xob - коефіцієнт затримки (0.99 = 99%), Xp - вихід перміату (0.75 = 75%)
...     """
...     Gp = Gv * Xp
...     Gk = Gv - Gp
...     Cp = Cv * (1 - Xob)
...     Ck = (Gv * Cv - Gp * Cp) / Gk
...     return Gp, Cp, Gk, Ck
... 
... # --- НАЛАШТУВАННЯ ІНТЕРФЕЙСУ ---
... 
... st.set_page_config(page_title="RO Calculator Pro", layout="wide")
... st.title("🚰 Калькулятор систем зворотного осмосу")
... st.markdown("Модульний розрахунок ступенів очистки з перевіркою балансу.")
... 
... # --- ВХІДНІ ДАНІ (SIDEBAR) ---
... 
... st.sidebar.header("📍 Вихідна вода")
... Gi_total = st.sidebar.number_input("Загальний потік на вході (м3/год)", min_value=0.1, value=10.0, step=0.5)
... Ci_total = st.sidebar.number_input("Початкова мінералізація (мг/л)", min_value=0.0, value=500.0, step=10.0)
... 
... st.sidebar.divider()
... 
... # Налаштування 1-ї ступені
... st.sidebar.subheader("⚙️ Параметри 1-ї ступені")
... Xp1 = st.sidebar.slider("Вихід перміату 1 (Xp1)", 0.05, 0.95, 0.75, help="Частка чистої води від входу")
... Xob1 = st.sidebar.slider("Селективність 1 (Xob1)", 0.80, 0.999, 0.98)

# Опція додавання 2-ї ступені
st.sidebar.divider()
add_second_stage = st.sidebar.checkbox("➕ Додати другу ступінь", value=False)

if add_second_stage:
    st.sidebar.subheader("⚙️ Параметри 2-ї ступені")
    Xp2 = st.sidebar.slider("Вихід перміату 2 (Xp2)", 0.05, 0.95, 0.50)
    Xob2 = st.sidebar.slider("Селективність 2 (Xob2)", 0.80, 0.999, 0.97)

# --- РОЗРАХУНОК ---

# Розрахунок 1-ї ступені
Gp1, Cp1, Gk1, Ck1 = membrana(Gi_total, Ci_total, Xob1, Xp1)

# Розрахунок 2-ї ступені (якщо активовано)
if add_second_stage:
    # Друга ступінь зазвичай працює на концентраті першої
    Gp2, Cp2, Gk2, Ck2 = membrana(Gk1, Ck1, Xob2, Xp2)
    
    total_permeate_G = Gp1 + Gp2
    total_permeate_C = (Gp1 * Cp1 + Gp2 * Cp2) / total_permeate_G
    final_concentrate_G = Gk2
    final_concentrate_C = Ck2
else:
    total_permeate_G = Gp1
    total_permeate_C = Cp1
    final_concentrate_G = Gk1
    final_concentrate_C = Ck1

# --- ВИВЕДЕННЯ РЕЗУЛЬТАТІВ ---

col1, col2 = st.columns(2)

with col1:
    st.info("### Ступінь №1")
    st.metric("Перміат Gp1", f"{Gp1:.2f} м3/год")
    st.metric("Солоність Cp1", f"{Cp1:.2f} мг/л")
    st.write(f"**Концентрат Gk1:** {Gk1:.2f} м3/год")
    st.write(f"**Солоність Ck1:** {Ck1:.2f} мг/л")

with col2:
    if add_second_stage:
        st.success("### Ступінь №2")
        st.metric("Перміат Gp2", f"{Gp2:.2f} м3/год")
        st.metric("Солоність Cp2", f"{Cp2:.2f} мг/л")
        st.write(f"**Фінальний концентрат Gk2:** {Gk2:.2f} м3/год")
        st.write(f"**Фінальна солоність Ck2:** {Ck2:.2f} мг/л")
    else:
        st.write("### Ступінь №2")
        st.write("Не активовано. Використовується лише одноступенева схема.")

st.divider()

# --- МАТЕРІАЛЬНИЙ БАЛАНС ---

st.subheader("⚖️ Перевірка матеріального балансу")

# Розрахунок нев'язки
in_mass_water = Gi_total
out_mass_water = total_permeate_G + final_concentrate_G
error_water = abs(in_mass_water - out_mass_water)

in_mass_salt = Gi_total * Ci_total
out_mass_salt = (total_permeate_G * total_permeate_C) + (final_concentrate_G * final_concentrate_C)
error_salt = abs(in_mass_salt - out_mass_salt)

b1, b2, b3 = st.columns(3)

with b1:
    st.write("**Потік води (м3/год)**")
    st.write(f"Вхід: {in_mass_water:.4f}")
    st.write(f"Вихід: {out_mass_water:.4f}")
    st.write(f"Нев'язка: `{error_water:.6f}`")

with b2:
    st.write("**Маса солі (г/год)**")
    st.write(f"Вхід: {in_mass_salt:.2f}")
    st.write(f"Вихід: {out_mass_salt:.2f}")
    st.write(f"Нев'язка: `{error_salt:.6f}`")

with b3:
    if error_water < 1e-7 and error_salt < 1e-4:
        st.success("✅ Баланс зійшовся!")
    else:
        st.error("❌ Помилка балансу!")

# ФІНАЛЬНИЙ ПІДСУМОК
st.divider()
st.subheader("📊 Загальний підсумок системи")
sum1, sum2, sum3 = st.columns(3)
sum1.metric("Загальний перміат", f"{total_permeate_G:.2f} м3/год")
sum2.metric("Сер. мінералізація", f"{total_permeate_C:.2f} мг/л")
