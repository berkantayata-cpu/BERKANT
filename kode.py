import os
import streamlit as st
import yt_dlp

# Sayfa Yapılandırması
st.set_page_config(
    page_title="BerkantAYT Media Suite",
    page_icon="🎵",
    layout="centered"
)

# Koyu Tema ve Spotify Tarzı Stil
st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: white;
    }
    h1, h2, h3, p, label, span {
        color: white !important;
    }
    .stButton>button {
        background-color: #1db954;
        color: black;
        font-weight: bold;
        border-radius: 20px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #1aa34a;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🟢 BerkantAYT Media Suite")
st.caption("Telefon ve Mobil Web İçin Özel Medya İndirici")

# Arama Bölümü
query = st.text_input("🔍 Şarkı, Sanatçı veya YouTube Linki Girin:", placeholder="Örn: Gamsız Hayat veya https://...")

if st.button("Aramayı Başlat"):
    if query:
        with st.spinner("Medyalar taranıyor..."):
            ydl_opts = {'extract_flat': 'in_playlist', 'skip_download': True, 'quiet': True}
            try:
                res = yt_dlp.YoutubeDL(ydl_opts).extract_info(f"ytsearch10:{query}", download=False)
                st.session_state['results'] = res.get('entries', [])
            except Exception as e:
                st.error(f"Arama hatası: {e}")

# Sonuçları Gösterme ve Telefona İndirme
if 'results' in st.session_state and st.session_state['results']:
    st.subheader("Arama Sonuçları")
    for idx, item in enumerate(st.session_state['results']):
        v_id = item.get('id')
        v_title = item.get('title', 'Bilinmeyen Başlık')
        v_url = item.get('url') or f"https://www.youtube.com/watch?v={v_id}"

        st.markdown(f"**{v_title}**")
        
        # İndirme işlemi
        if st.button(f"⬇️ {v_title[:30]}... İndir", key=f"btn_{idx}"):
            with st.spinner("Dosya hazırlanıyor..."):
                file_path = f"download_{v_id}.mp3"
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': f'download_{v_id}.%(ext)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'quiet': True
                }
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([v_url])
                    
                    # Buluttan Doğrudan Telefona İndirme Butonu
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as f:
                            st.download_button(
                                label="📥 Telefona Kaydet (MP3)",
                                data=f,
                                file_name=f"{v_title}.mp3",
                                mime="audio/mpeg"
                            )
                        os.remove(file_path)
                except Exception as ex:
                    st.error(f"İndirme hazırlığı hatası: {ex}")
        st.markdown("---")