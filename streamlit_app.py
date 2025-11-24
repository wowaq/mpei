import streamlit as st


def lab1():
    from raw_labs import lab1 as raw

    st.title("Лабораторная работа №5")
    k = st.slider("Числа", 1, 6)
    st.write(raw.k(k))


def lab2():
    st.title("Second lab")


def random_emoji():
    import random

    list = "📊 ✅ 🔎 📈 ✔️ 🛠️ 📚 🌐 🧠".split()
    return random.choice(list)


pg = st.navigation(
    [
        st.Page(lab1, title="Лабораторная работа №5", icon=random_emoji()),
        st.Page(lab2, title="Лабораторная работа №6", icon=random_emoji()),
    ]
)
pg.run()
