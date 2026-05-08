import streamlit as st

def membrana(Gv, Cv, Xob, Xp):
    Gp = Gv * Xp
    Gk = Gv - Gp
    Cp = Cv * (1 - Xob)
    if Gk > 0.0001:
        Ck = (Gv * Cv - Gp * Cp) / Gk
    else:
        Ck = Cv
    return Gp, Cp, Gk, Ck

st.set_page_config(page_title="RO System", layout="wide")
st.title("Розрахунок ступенів зворотного осмосу")

Gi_total = st.sidebar.number_input("Потік води (м3/год)", value=10.0)
Ci_total = st.sidebar.number_input("Мінералізація (мг/л)", value=500.0)

st.sidebar.subheader("Ступінь 1")
Xp1 = st.sidebar.slider("Вихід перміату 1", 0.1, 0.95, 0.75)
Xob1 = st.sidebar.slider("Селективність 1", 0.9, 0.999, 0.98)

add_second = st.sidebar.checkbox("Додати Ступінь 2")

if add_second:
    st.sidebar.subheader("Ступінь 2")
    Xp2 = st.sidebar.slider("Вихід перміату 2", 0.1, 0.95, 0.5)
    Xob2 = st.sidebar.slider("Селективність 2", 0.9, 0.999, 0.97)

Gp1, Cp1, Gk1, Ck1 = membrana(Gi_total, Ci_total, Xob1, Xp1)

if add_second:
    Gp2, Cp2, Gk2, Ck2 = membrana(Gk1, Ck1, Xob2, Xp2)
    total_G_p = Gp1 + Gp2
    total_C_p = (Gp1 * Cp1 + Gp2 * Cp2) / total_G_p
    total_G_c = Gk2
    total_C_c = Ck2
else:
    total_G_p = Gp1
    total_C_p = Cp1
    total_G_c = Gk1
    total_C_c = Ck1

col1, col2 = st.columns(2)
with col1:
    st.info("### Ступінь 1")
    st.write(f"Перміат: {Gp1:.2f} м3/год")
    st.write(f"Солоність: {Cp1:.2f} мг/л")
    st.write(f"Концентрат: {Gk1:.2f} м3/год")

with col2:
    if add_second:
        st.success("### Ступінь 2")
        st.write(f"Перміат: {Gp2:.2f} м3/год")
        st.write(f"Солоність: {Cp2:.2f} мг/л")
        st.write(f"Концентрат: {Gk2:.2f} м3/год")

st.divider()
st.subheader("Баланс")
in_s = Gi_total * Ci_total
out_s = (total_G_p * total_C_p) + (total_G_c * total_C_c)
st.write(f"Похибка потоку: {abs(Gi_total - (total_G_p + total_G_c)):.6f}")
st.write(f"Похибка солей: {abs(in_s - out_s):.6f}")
