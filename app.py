Код додатка (app.py)
Ви можете скопіювати цей код у файл app.py і запустити його за допомогою команди streamlit run app.py
.
import streamlit as st

# Визначення функцій на основі джерел [2-4]
def zmishyvach(Gr, Ck, Ci, Gv):
    """Змішувач: розраховує потік Gi та концентрацію Cv [2]"""
    Gi = Gv - Gr
    Cv = (Gr * Ck + Gi * Ci) / Gv
    return Gi, Cv

def rozdiluvach(Gk, Xr):
    """Розділювач: розраховує концентрати Gr та Gs [3]"""
    Gr = Gk * Xr
    Gs = Gk - Gr
    return Gr, Gs

def membrana(Gv, Cv, Xob, Xp):
    """Мембрана: розраховує параметри перміату та концентрату [3]"""
    Gp = Gv * Xp
    Gk = Gv - Gp
    Cp = Cv * (1 - Xob)
    Ck = (Gv * Cv - Gp * Cp) / Gk
    return Gp, Cp, Gk, Ck

def zmish2(Gr1, Ck1, Gr2, Ck2):
    """Змішувач для 2-ї ступені [4]"""
    Gr = Gr1 + Gr2
    Ck = (Gr1 * Ck1 + Gr2 * Ck2) / Gr
    return Gr, Ck

# Інтерфейс користувача Streamlit [5, 6]
st.title("Калькулятор систем зворотного осмосу (RO-2022)")
st.markdown("Цей додаток дозволяє виконувати розрахунки вузлів системи ЗОУ на основі математичних моделей.")

# Бічна панель для введення даних
st.sidebar.header("Вихідні дані")

# Введення даних для змішувача
st.sidebar.subheader("Параметри змішувача")
Gr_input = st.sidebar.number_input("Потік концентрату (Gr)", value=10.0)
Ck_input = st.sidebar.number_input("Концентрація концентрату (Ck)", value=2.0)
Ci_input = st.sidebar.number_input("Початкова концентрація (Ci)", value=0.5)
Gv_input = st.sidebar.number_input("Загальний потік (Gv)", value=100.0)

# Введення даних для мембрани
st.sidebar.subheader("Параметри мембрани")
Xob_input = st.sidebar.number_input("Коефіцієнт затримки (Xob)", value=0.99)
Xp_input = st.sidebar.number_input("Вихід перміату (Xp)", value=0.75)

# Розрахунок при натисканні кнопки
if st.button("Виконати розрахунок"):
    # 1. Розрахунок змішувача
    Gi, Cv = zmishyvach(Gr_input, Ck_input, Ci_input, Gv_input)
    
    # 2. Розрахунок мембрани
    Gp, Cp, Gk, Ck_new = membrana(Gv_input, Cv, Xob_input, Xp_input)
    
    # Відображення результатів
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Результати змішувача")
        st.write(f"**Вхідний потік (Gi):** {Gi:.2f}")
        st.write(f"**Концентрація на вході в мембрану (Cv):** {Cv:.4f}")
        
    with col2:
        st.subheader("Результати мембрани")
        st.write(f"**Потік перміату (Gp):** {Gp:.2f}")
        st.write(f"**Концентрація перміату (Cp):** {Cp:.4f}")
        st.write(f"**Потік концентрату (Gk):** {Gk:.2f}")
        st.write(f"**Концентрація концентрату (Ck):** {Ck_new:.4f}")

    # Перевірка матеріального балансу [7, 8]
    st.divider()
    st.subheader("Перевірка матеріального балансу")
    balance_mass = Gv_input - (Gp + Gk)
    st.write(f"Похибка балансу по потоку: {balance_mass:.6f}")
