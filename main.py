
import streamlit as st
import time
import random
import html
st.set_page_config(page_title="Typing Speed Test")
st.title("Typing Speed Test")
st.write("Type the sentence below as quickly and accurately as possible!")
sentences = [
    "A person's catalog cannot change a person's perspective",
    "Making code is very hard",
    "Self-esteem doesn't pay",
    "Practice makes perfect",
    "Be better at typing"
]
if "sentence" not in st.session_state:
    st.session_state.sentence = random.choice(sentences)
    st.session_state.start = None
    st.session_state.finish = None
    st.session_state.typing = ""
def new_sentence():
    st.session_state.sentence = random.choice(sentences)
    st.session_state.start = None
    st.session_state.finish = None
    st.session_state.typing = ""
def check_typing():
    if st.session_state.typing and st.session_state.start is None:
        st.session_state.start = time.time()
    if st.session_state.typing == st.session_state.sentence:
        if st.session_state.finish is None:
            st.session_state.finish = time.time()
typed = st.text_input("Type here:", key="typing", on_change=check_typing)
highlighted = ""
for i, letter in enumerate(st.session_state.sentence):
    if i < len(typed):
        color = "green" if typed[i] == letter else "red"
    else:
        color = "gray"
    highlighted += f'<span style="color:{color}">{html.escape(letter)}</span>'
st.markdown(f'<div style="font-size:24px;line-height:2;letter-spacing:1px">{highlighted}</div>', unsafe_allow_html=True)
@st.fragment(run_every=1)
def show_results():
    typed = st.session_state.typing
    if st.session_state.start is None:
        seconds = 0
    elif st.session_state.finish is not None:
        seconds = st.session_state.finish - st.session_state.start
    else:
        seconds = time.time() - st.session_state.start
    correct = sum(a == b for a, b in zip(typed, st.session_state.sentence))
    accuracy = correct / len(typed) * 100 if typed else 0
    wpm = (correct / 5) / (seconds / 60) if seconds > 0 else 0
    col1, col2, col3 = st.columns(3)
    col1.metric("Time", f"{seconds:.1f}s")
    col2.metric("WPM", f"{wpm:.1f}")
    col3.metric("Accuracy", f"{accuracy:.0f}%")
    if st.session_state.finish is not None:
        st.success("Excellent! You have finished your sentence!")
show_results()
st.button("New Sentence", on_click=new_sentence)
