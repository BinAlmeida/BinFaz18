import io
import uuid
from datetime import datetime, timezone

import streamlit as st
from PIL import Image, ImageOps
from supabase import create_client, Client

from style import aplicar_estilo, banner, rodape

st.set_page_config(
    page_title="Bin faz 18!",
    page_icon="🎀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

aplicar_estilo()

def get_config():
    try:
        return st.secrets["supabase"]
    except Exception:
        return None

def connect_supabase() -> Client:
    cfg = get_config()
    if not cfg:
        st.error("O Supabase ainda não está configurado. Veja o arquivo README.md.")
        st.stop()
    url = str(cfg.get("url", ""))
    key = str(cfg.get("service_role_key", ""))
    if "SEU-PROJETO" in url or "COLE_AQUI" in key or not url or not key:
        st.error("O arquivo .streamlit/secrets.toml ainda está com os valores de exemplo. "
                 "Preencha a URL do projeto e a chave secreta do Supabase e reinicie o app.")
        st.stop()
    try:
        return create_client(url, key)
    except Exception as exc:
        st.error(f"Não foi possível conectar ao Supabase: {exc}")
        st.stop()

def prepare_image(uploaded_file):
    """Corrige a orientação e limita imagens muito grandes antes do upload."""
    image = Image.open(uploaded_file)
    image = ImageOps.exif_transpose(image).convert("RGB")
    image.thumbnail((2000, 2000))
    output = io.BytesIO()
    image.save(output, format="JPEG", quality=88, optimize=True)
    return output.getvalue()

def image_public_url(supabase, path):
    cfg = get_config()
    bucket = cfg.get("bucket", "birthday-photos")
    result = supabase.storage.from_(bucket).get_public_url(path)
    if isinstance(result, str):
        return result
    return result.get("publicUrl") or result.get("publicURL") or str(result)

cfg = get_config()
event_title = (cfg.get("event_title", "Memórias da Festa") if cfg else "Memórias da Festa")
event_date = (cfg.get("event_date", "") if cfg else "")

banner()
st.markdown(
    "<p style='text-align:center; font-size:1.1rem'>✿ Um lugar para reunir os momentos mais especiais da festa ✿<br>"
    "Tire uma foto, compartilhe com a gente e ajude a guardar essa memória! ♥</p>",
    unsafe_allow_html=True,
)

if event_date:
    st.caption(f"🎉 Data da festa: {event_date}")

supabase = connect_supabase()
cfg = get_config()
bucket = cfg.get("bucket", "birthday-photos")
admin_code = str(cfg.get("admin_code", ""))

tab_upload, tab_gallery, tab_admin = st.tabs(["Enviar fotos", "Galeria", "Administração"])

with tab_upload:
    st.subheader("Compartilhe suas fotos")
    st.write("Escolha uma ou mais imagens. Para facilitar os envios, prefira fotos JPG, PNG ou WEBP.")
    uploads = st.file_uploader(
        "Selecione as fotos",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True,
        help="Limite recomendado: até 10 MB por foto.",
    )
    nickname = st.text_input("Seu nome ou apelido (opcional)", max_chars=40)
    note = st.text_input("Legenda (opcional)", max_chars=180)
    st.caption("Ao enviar, você confirma que tem permissão para compartilhar as imagens escolhidas.")

    if st.button("Enviar fotos", type="primary", use_container_width=True):
        if not uploads:
            st.warning("Escolha pelo menos uma foto antes de enviar.")
        else:
            progress = st.progress(0)
            successes, errors = 0, []
            for index, uploaded in enumerate(uploads):
                try:
                    if uploaded.size > 10 * 1024 * 1024:
                        raise ValueError("A imagem excede 10 MB.")
                    content = prepare_image(uploaded)
                    filename = f"{uuid.uuid4().hex}.jpg"
                    path = f"{datetime.now(timezone.utc).strftime('%Y/%m')}/{filename}"
                    supabase.storage.from_(bucket).upload(
                        path,
                        content,
                        file_options={"content-type": "image/jpeg", "upsert": "false"},
                    )
                    row = {
                        "storage_path": path,
                        "nickname": nickname.strip() or "Convidado",
                        "caption": note.strip(),
                        "created_at": datetime.now(timezone.utc).isoformat(),
                    }
                    supabase.table("photos").insert(row).execute()
                    successes += 1
                except Exception as exc:
                    errors.append(f"{uploaded.name}: {exc}")
                progress.progress((index + 1) / len(uploads))
            if successes:
                st.success(f"{successes} foto(s) enviada(s)! Obrigada por compartilhar")
            if errors:
                st.error("Alguns arquivos não foram enviados:\n\n" + "\n".join(errors))
            if successes:
                st.cache_data.clear()

with tab_gallery:
    st.subheader("Mural de memórias")
    col_a, col_b = st.columns([3, 1])
    with col_a:
        search_name = st.text_input("Filtrar por nome ou legenda", placeholder="Digite para buscar...")
    with col_b:
        if st.button("Atualizar galeria", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    try:
        response = supabase.table("photos").select("*").order("created_at", desc=True).limit(500).execute()
        photos = response.data or []
        if search_name:
            term = search_name.casefold()
            photos = [p for p in photos if term in str(p.get("nickname", "")).casefold()
                      or term in str(p.get("caption", "")).casefold()]
        if not photos:
            st.info("Ainda não há fotos por aqui. Seja a primeira pessoa a compartilhar uma!")
        else:
            st.caption(f"{len(photos)} foto(s) exibida(s) — mostrando até 500 publicações mais recentes.")
            columns = st.columns(3, gap="medium")
            for i, photo in enumerate(photos):
                with columns[i % 3]:
                    try:
                        url = image_public_url(supabase, photo["storage_path"])
                        st.image(url, use_container_width=True)
                        st.markdown(f"**{photo.get('nickname') or 'Convidado'}**")
                        if photo.get("caption"):
                            st.write(photo["caption"])
                        st.caption(photo.get("created_at", "")[:16].replace("T", " "))
                    except Exception:
                        st.warning("Esta imagem não pôde ser carregada.")
    except Exception as exc:
        st.error(f"Não foi possível carregar a galeria: {exc}")
        st.info("Confira se executou o SQL de configuração do README.")

with tab_admin:
    st.subheader("Área da aniversariante")
    admin_input = st.text_input("Código de administração", type="password")
    if admin_input and admin_code and admin_input == admin_code:
        st.success("Acesso administrativo liberado.")
        try:
            response = supabase.table("photos").select("*").order("created_at", desc=True).limit(500).execute()
            photos = response.data or []
            if not photos:
                st.info("Ainda não existem fotos.")
            for photo in photos:
                left, right = st.columns([4, 1])
                with left:
                    st.write(f"**{photo.get('nickname') or 'Convidado'}** — {photo.get('caption') or 'Sem legenda'}")
                    st.caption(photo.get("storage_path", ""))
                with right:
                    if st.button("Excluir", key=f"delete_{photo['id']}", type="secondary"):
                        try:
                            supabase.storage.from_(bucket).remove([photo["storage_path"]])
                            supabase.table("photos").delete().eq("id", photo["id"]).execute()
                            st.success("Foto excluída.")
                            st.rerun()
                        except Exception as exc:
                            st.error(f"Não foi possível excluir: {exc}")
        except Exception as exc:
            st.error(f"Erro ao carregar administração: {exc}")
    elif admin_input:
        st.error("Código de administração incorreto.")

rodape()
