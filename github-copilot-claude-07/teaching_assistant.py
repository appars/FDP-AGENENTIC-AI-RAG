import streamlit as st
from transformers import pipeline
import torch
import PyPDF2
import io

# ── Config ────────────────────────────────────────────────────────────────────

HF_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
MAX_NEW_TOKENS = 512
SYLLABUS_CHARS = 1200   # keep prompt short for 2048-token context window

CONTENT_TYPES = {
    "Explanation": "Explain this topic clearly with simple examples for undergraduate students.",
    "MCQs":        "Generate 5 multiple-choice questions with 4 options each. Mark the correct answer.",
    "Assignment":  "Create 3 assignment questions (mix of short and long answer) on this topic.",
    "References":  "List 5 useful academic references (books or URLs) for this topic.",
}

# ── Model (cached so it loads only once) ─────────────────────────────────────

@st.cache_resource(show_spinner="Loading TinyLlama — first run downloads ~600 MB...")
def load_model():
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    return pipeline(
        "text-generation",
        model=HF_MODEL,
        torch_dtype=dtype,
        device_map="auto",
    )

# ── Helpers ───────────────────────────────────────────────────────────────────

def extract_pdf_text(uploaded_file) -> str:
    reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def llm(pipe, system: str, user: str) -> str:
    messages = [
        {"role": "system", "content": system},
        {"role": "user",   "content": user},
    ]
    prompt = pipe.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    outputs = pipe(
        prompt,
        max_new_tokens=MAX_NEW_TOKENS,
        do_sample=True,
        temperature=0.7,
        top_p=0.95,
        pad_token_id=pipe.tokenizer.eos_token_id,
    )
    # Strip the input prompt from the output
    return outputs[0]["generated_text"][len(prompt):].strip()


def extract_topics(syllabus_text: str, pipe) -> list[str]:
    system = "You are a helpful assistant that extracts topics from a course syllabus."
    user = (
        "List the main topics from this syllabus, one per line, no numbering, no extra text.\n\n"
        f"{syllabus_text[:SYLLABUS_CHARS]}"
    )
    raw = llm(pipe, system, user)
    return [line.strip() for line in raw.splitlines() if line.strip()]


def generate_response(topic: str, content_type: str, syllabus_text: str, pipe) -> str:
    system = (
        "You are an AI Teaching Assistant helping professors prepare course material.\n"
        f"Syllabus context: {syllabus_text[:SYLLABUS_CHARS]}"
    )
    user = f"Topic: {topic}\nTask: {CONTENT_TYPES[content_type]}"
    return llm(pipe, system, user)


def chat_reply(user_message: str, topic: str, syllabus_text: str,
               history: list, pipe) -> str:
    system = (
        "You are an AI Teaching Assistant. Answer the professor's question concisely.\n"
        f"Current topic: {topic}\n"
        f"Syllabus context: {syllabus_text[:SYLLABUS_CHARS]}"
    )
    history_text = "\n".join(
        f"{'Professor' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
        for m in history[-4:]
    )
    user = f"{history_text}\nProfessor: {user_message}" if history_text else user_message
    return llm(pipe, system, user)

# ── UI ────────────────────────────────────────────────────────────────────────

def main():
    st.set_page_config(page_title="AI Teaching Assistant", page_icon="🎓", layout="wide")
    st.title("🎓 AI Teaching Assistant")
    st.caption("Powered by TinyLlama-1.1B-Chat (local) — for professors")

    # Load model at startup (cached after first load)
    pipe = load_model()

    # ── Session state ──────────────────────────────────────────────────────────
    for key, default in [("messages", []), ("topics", []), ("syllabus_text", "")]:
        if key not in st.session_state:
            st.session_state[key] = default

    # ── Sidebar ────────────────────────────────────────────────────────────────
    with st.sidebar:
        st.header("⚙️ Setup")
        st.success(f"Model loaded: `{HF_MODEL}` ✓")

        st.divider()

        uploaded = st.file_uploader("📄 Upload Syllabus PDF", type="pdf")
        if uploaded:
            with st.spinner("Reading PDF..."):
                st.session_state.syllabus_text = extract_pdf_text(uploaded)
            with st.spinner("Extracting topics..."):
                st.session_state.topics = extract_topics(
                    st.session_state.syllabus_text, pipe
                )
            st.success(f"{len(st.session_state.topics)} topics found ✓")

        selected_topic = "General"
        if st.session_state.topics:
            st.divider()
            st.header("📚 Topic")
            selected_topic = st.selectbox("Select a topic", st.session_state.topics)

            st.header("🛠️ Generate")
            for label in CONTENT_TYPES:
                if st.button(label, use_container_width=True):
                    with st.spinner(f"Generating {label}..."):
                        reply = generate_response(
                            selected_topic,
                            label,
                            st.session_state.syllabus_text,
                            pipe,
                        )
                    st.session_state.messages.append(
                        {"role": "assistant", "content": f"**{label} — {selected_topic}**\n\n{reply}"}
                    )
                    st.rerun()

            st.divider()
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

    # ── Chat area ──────────────────────────────────────────────────────────────
    if not st.session_state.syllabus_text:
        st.info("Upload a syllabus PDF from the sidebar to begin.")
        return

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input(f"Ask about {selected_topic}..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = chat_reply(
                    prompt,
                    selected_topic,
                    st.session_state.syllabus_text,
                    st.session_state.messages,
                    pipe,
                )
            st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
