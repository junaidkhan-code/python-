import shutil
from datetime import datetime
from pathlib import Path

import streamlit as st

# ───────────────────────── Page config ─────────────────────────
st.set_page_config(page_title="File Manager", page_icon="🗂️", layout="wide")

# ───────────────────────── Palette ─────────────────────────
# bg #0E1124 | card #171B36 | border #2A2F57 | text #E6E8F5 | muted #9AA0C7
# violet #7C6CFF | teal #2DD4BF | rose #FB7185 | amber #FBBF24
CSS = """
<style>
#MainMenu, footer {visibility: hidden;}
.block-container {padding-top: 2rem; max-width: 1150px;}

.hero {
    background: linear-gradient(120deg, #7C6CFF 0%, #4F8CFF 55%, #2DD4BF 100%);
    padding: 1.6rem 2rem; border-radius: 18px; margin-bottom: 1.5rem;
    box-shadow: 0 10px 30px rgba(124,108,255,.25);
}
.hero h1 {color:#fff; margin:0; font-size:2rem;}
.hero p  {color:rgba(255,255,255,.85); margin:.3rem 0 0 0;}

.stat {
    background:#171B36; border:1px solid #2A2F57; border-radius:16px;
    padding:1.1rem 1.3rem; border-left:5px solid var(--c);
}
.stat .lbl {color:#9AA0C7; font-size:.8rem; letter-spacing:.08em; text-transform:uppercase;}
.stat .val {color:#E6E8F5; font-size:2rem; font-weight:700; line-height:1.2;}

.item {
    display:flex; justify-content:space-between; align-items:center;
    background:#171B36; border:1px solid #2A2F57; border-radius:12px;
    padding:.65rem 1rem; margin-bottom:.5rem;
}
.item:hover {border-color:#7C6CFF;}
.item .name {color:#E6E8F5; font-weight:600;}
.item .meta {color:#9AA0C7; font-size:.8rem;}

section[data-testid="stSidebar"] {background:#12152C; border-right:1px solid #2A2F57;}
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(90deg,#7C6CFF,#4F8CFF); color:#fff; border:none;
    border-radius:10px; padding:.55rem 1.3rem; font-weight:600; transition:.2s;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-1px); box-shadow:0 6px 18px rgba(124,108,255,.4); color:#fff;
}
.danger .stButton > button {background: linear-gradient(90deg,#FB7185,#F43F5E);}
.stTextInput input, .stTextArea textarea, div[data-baseweb="select"] > div {
    background:#0E1124 !important; border:1px solid #2A2F57 !important; border-radius:10px !important;
}
.stTabs [data-baseweb="tab-list"] {gap:.4rem;}
.stTabs [data-baseweb="tab"] {background:#171B36; border-radius:10px 10px 0 0; padding:.5rem 1.1rem;}
.stTabs [aria-selected="true"] {background:#2A2F57; color:#2DD4BF;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ───────────────────────── Helpers ─────────────────────────
ROOT = Path("workspace")
ROOT.mkdir(exist_ok=True)
ROOT = ROOT.resolve()


def safe(path) -> Path:
    """Resolve a path and make sure it stays inside the workspace."""
    p = (ROOT / path).resolve()
    if p != ROOT and not p.is_relative_to(ROOT):
        raise ValueError("Path is outside the workspace.")
    return p


def rel(p: Path) -> str:
    return "/" if p == ROOT else p.relative_to(ROOT).as_posix()


def folders():
    return sorted([p for p in ROOT.rglob("*") if p.is_dir()])


def files():
    return sorted([p for p in ROOT.rglob("*") if p.is_file()])


def human(n: int) -> str:
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.0f} {u}" if u == "B" else f"{n:.1f} {u}"
        n /= 1024
    return f"{n:.1f} TB"


def flash(msg, kind="success"):
    st.session_state["flash"] = (msg, kind)


def show_flash():
    if "flash" in st.session_state:
        msg, kind = st.session_state.pop("flash")
        {"success": st.success, "error": st.error, "warning": st.warning}[kind](msg)


def stat(label, value, color):
    st.markdown(
        f'<div class="stat" style="--c:{color}"><div class="lbl">{label}</div>'
        f'<div class="val">{value}</div></div>',
        unsafe_allow_html=True,
    )


def item_row(icon, p: Path):
    info = p.stat()
    meta = human(info.st_size) if p.is_file() else "folder"
    when = datetime.fromtimestamp(info.st_mtime).strftime("%d %b %Y, %H:%M")
    st.markdown(
        f'<div class="item"><span class="name">{icon} {rel(p)}</span>'
        f'<span class="meta">{meta} · {when}</span></div>',
        unsafe_allow_html=True,
    )


def done(msg):
    flash(msg)
    st.rerun()


# ───────────────────────── Sidebar ─────────────────────────
with st.sidebar:
    st.markdown("## 🗂️ File Manager")
    st.caption("Everything lives inside the `workspace/` folder.")
    page = st.radio("Navigate", ["🏠 Dashboard", "📁 Folders", "📄 Files"], label_visibility="collapsed")
    st.divider()
    st.caption("Palette: violet · blue · teal on midnight")

st.markdown(
    '<div class="hero"><h1>File Manager</h1>'
    "<p>Create, read, update and delete folders & files — beautifully.</p></div>",
    unsafe_allow_html=True,
)
show_flash()

all_folders, all_files = folders(), files()
folder_options = [ROOT] + all_folders

# ───────────────────────── Dashboard ─────────────────────────
if page == "🏠 Dashboard":
    total = sum(f.stat().st_size for f in all_files)
    c1, c2, c3 = st.columns(3)
    with c1: stat("Folders", len(all_folders), "#7C6CFF")
    with c2: stat("Files", len(all_files), "#2DD4BF")
    with c3: stat("Total size", human(total), "#FBBF24")

    st.markdown("### 🕑 Recently modified")
    recent = sorted(all_files + all_folders, key=lambda p: p.stat().st_mtime, reverse=True)[:8]
    if recent:
        for p in recent:
            item_row("📁" if p.is_dir() else "📄", p)
    else:
        st.info("Nothing here yet — create a folder or file to get started.")

# ───────────────────────── Folders ─────────────────────────
elif page == "📁 Folders":
    t1, t2, t3, t4 = st.tabs(["➕ Create", "📂 Browse", "✏️ Rename", "🗑️ Delete"])

    with t1:
        parent = st.selectbox("Create inside", folder_options, format_func=rel, key="f_parent")
        name = st.text_input("Folder name", key="f_new")
        if st.button("Create folder"):
            try:
                if not name.strip():
                    st.error("Please enter a folder name.")
                else:
                    p = safe(parent / name.strip())
                    if p.exists():
                        st.error("That folder already exists — try another name.")
                    else:
                        p.mkdir(parents=True)
                        done(f"Folder '{rel(p)}' created successfully!")
            except ValueError as e:
                st.error(str(e))

    with t2:
        if all_folders:
            for p in all_folders:
                item_row("📁", p)
        else:
            st.info("No folders yet.")

    with t3:
        if all_folders:
            old = st.selectbox("Folder to rename", all_folders, format_func=rel, key="f_old")
            new = st.text_input("New name", key="f_newname")
            if st.button("Rename folder"):
                try:
                    target = safe(old.parent / new.strip())
                    if not new.strip():
                        st.error("Enter a new name.")
                    elif target.exists():
                        st.error("A folder with that name already exists.")
                    else:
                        old.rename(target)
                        done("Updated successfully!")
                except ValueError as e:
                    st.error(str(e))
        else:
            st.info("No folders to rename.")

    with t4:
        if all_folders:
            target = st.selectbox("Folder to delete", all_folders, format_func=rel, key="f_del")
            has_content = any(target.iterdir())
            force = False
            if has_content:
                st.warning("This folder is not empty.")
                force = st.checkbox("Delete it and everything inside")
            confirm = st.checkbox("I understand this can't be undone", key="f_confirm")
            st.markdown('<div class="danger">', unsafe_allow_html=True)
            if st.button("Delete folder"):
                if not confirm:
                    st.error("Please tick the confirmation box.")
                elif has_content and not force:
                    st.error("Folder isn't empty — tick the delete-everything box.")
                else:
                    shutil.rmtree(target) if has_content else target.rmdir()
                    done("Folder deleted successfully!")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No folders to delete.")

# ───────────────────────── Files ─────────────────────────
else:
    t1, t2, t3, t4 = st.tabs(["➕ Create", "👁️ Read", "✏️ Update", "🗑️ Delete"])

    with t1:
        parent = st.selectbox("Save inside", folder_options, format_func=rel, key="file_parent")
        name = st.text_input("File name with extension", placeholder="notes.txt", key="file_new")
        content = st.text_area("Content", height=180, key="file_content")
        if st.button("Create file"):
            try:
                if not name.strip():
                    st.error("Please enter a file name.")
                else:
                    p = safe(parent / name.strip())
                    if p.exists():
                        st.error("File already exists — pick another name.")
                    else:
                        p.write_text(content, encoding="utf-8")
                        done(f"File '{rel(p)}' created successfully!")
            except ValueError as e:
                st.error(str(e))

    with t2:
        if all_files:
            f = st.selectbox("Choose a file", all_files, format_func=rel, key="read_sel")
            try:
                text = f.read_text(encoding="utf-8")
                st.caption(f"{human(f.stat().st_size)} · {len(text.splitlines())} lines")
                st.code(text or "(empty file)", language=f.suffix.lstrip(".") or None)
                st.download_button("⬇️ Download", text, file_name=f.name)
            except UnicodeDecodeError:
                st.warning("This looks like a binary file and can't be previewed.")
        else:
            st.info("No files yet.")

    with t3:
        if all_files:
            f = st.selectbox("File to update", all_files, format_func=rel, key="upd_sel")
            mode = st.radio("Action", ["Rename", "Overwrite content", "Append content"], horizontal=True)

            if mode == "Rename":
                new = st.text_input("New name with extension", key="upd_name")
                if st.button("Rename file"):
                    try:
                        target = safe(f.parent / new.strip())
                        if not new.strip():
                            st.error("Enter a new name.")
                        elif target.exists():
                            st.error("A file with that name already exists.")
                        else:
                            f.rename(target)
                            done("File name changed successfully!")
                    except ValueError as e:
                        st.error(str(e))
            else:
                try:
                    current = f.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    current = None
                if current is None:
                    st.warning("Binary file — can't edit as text.")
                elif mode == "Overwrite content":
                    data = st.text_area("New content", value=current, height=200, key="upd_over")
                    if st.button("Save changes"):
                        f.write_text(data, encoding="utf-8")
                        done("Overwritten successfully!")
                else:
                    data = st.text_area("Text to append", height=140, key="upd_app")
                    if st.button("Append"):
                        with open(f, "a", encoding="utf-8") as fh:
                            fh.write(data)
                        done("Appended successfully!")
        else:
            st.info("No files to update.")

    with t4:
        if all_files:
            f = st.selectbox("File to delete", all_files, format_func=rel, key="del_sel")
            confirm = st.checkbox("I understand this can't be undone", key="file_confirm")
            st.markdown('<div class="danger">', unsafe_allow_html=True)
            if st.button("Delete file"):
                if confirm:
                    f.unlink()
                    done("File deleted successfully!")
                else:
                    st.error("Please tick the confirmation box.")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No files to delete.")