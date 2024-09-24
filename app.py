import streamlit as st
from pytubefix import YouTube

# Título de la aplicación
st.title("YouTube Downloader")

# Entrada para la URL del video
video_url = st.text_input("Introduce la URL del video de YouTube:")

# Selección del formato de descarga
formato = st.selectbox("Selecciona el formato de descarga:", ["MP4 (Video)", "MP3 (Audio)"])

# Verificar si hay una URL de video
if video_url:
    try:
        # Crear objeto YouTube
        yt = YouTube(video_url)
        st.write(f"Título del video: {yt.title}")

        # Si el formato es MP4, mostrar las opciones de calidad disponibles
        if formato == "MP4 (Video)":
            # Filtrar los streams de video disponibles
            streams = yt.streams.filter(progressive=True, file_extension='mp4')

            # Mostrar las resoluciones disponibles para que el usuario elija
            opciones_calidad = [stream.resolution for stream in streams]
            calidad_seleccionada = st.selectbox("Selecciona la calidad del video:", opciones_calidad)

        elif formato == "MP3 (Audio)":
            st.write("Solo se descargará el audio del video.")

        # Botón para iniciar la descarga
        if st.button("Descargar"):
            if formato == "MP4 (Video)" and calidad_seleccionada:
                # Descargar el video en la calidad seleccionada
                stream = streams.filter(res=calidad_seleccionada).first()
                if stream:
                    st.write(f"Descargando {yt.title} en {calidad_seleccionada}...")
                    stream.download()
                    st.success(f"Descarga completada: {yt.title} en {calidad_seleccionada}")
                else:
                    st.error("No se encontró el stream en la calidad seleccionada.")

            elif formato == "MP3 (Audio)":
                # Descargar solo audio
                stream = yt.streams.filter(only_audio=True).first()
                if stream:
                    st.write(f"Descargando audio de {yt.title}...")
                    stream.download(filename=f"{yt.title}.mp3")
                    st.success(f"Descarga de audio completada: {yt.title}")
                else:
                    st.error("No se pudo descargar el audio.")

    except Exception as e:
        st.error(f"Error al descargar el video: {e}")
