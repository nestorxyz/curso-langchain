<p align="center">
  <img src="images/Group 2.png" width="761" height="400">
</p>

# Creación de un chatbot conversacional con memoria usando HuggingFace y OpenAI, Streamlit(UI) y ChromaDB como BD vectorial

## **Descripción**

Este proyecto toma archivos jsonl que tienen la documentación de Hugging Face de los repositorios:

- https://github.com/huggingface/transformers
- https://github.com/huggingface/accelerate
- https://github.com/huggingface/peft
- https://github.com/huggingface/blog

Y los usa como contexto para responder las preguntas del usuario a través de una UI hecha con Streamlit, el proyecto está hecho para ser ejecutado localmente ya que la BD vectorial no se guarda en la nube sino de manera local.

## **Configuración**

El funcionamiento del proyecto se puede manipular mediante el archivo **`config.yaml`**. Para utilizar el proyecto desde cero, sigue estos pasos:

1. **Extracción de textos**: Ejecute **`hashira/text_extractor.py`**. Este script exportará a la carpeta **`data`** un archivo jsonl con todos los archivos markdown de las documentaciones indicadas en la variable **`github`** en el archivo **`config.yaml`**. Estos archivos serán limpiados por **`text_extractor.py`** y estarán listos para ser divididos en Documentos de Langchain.
2. **Recreación de la base de datos de Chroma**: La función **`get_chroma_db`** recibe un parámetro llamado **`recreate_chroma_db`**, en la primera ejecución asignale **`True`** para que se cree la BD vectorial de manera local y se almacenará localmente con el nombre "chroma_docs".
3. **Interacción con los documentos**: Al ejecutar **`hashira/app.py`**, podrás chatear con todos los documentos obtenidos de Github.

![Untitled design](https://github.com/nestorxyz/curso-langchain/assets/72099481/71875eb7-9a5d-4735-928c-1dbcf59505b8)


## Instalación de dependencias con Poetry

Puede instalar las dependencias y crear un entorno virtual utilizando Poetry con el siguiente comando:

```shell
poetry install
```

Luego, puede ejecutar el proyecto con:

```shell
poetry run streamlit run hashira/app.py
```

## **Código base**
El código base del proyecto fue tomado del curso de Langchain de Platzi: https://github.com/platzi/curso-langchain

## **Blog explicando el código**
https://blog.nestormamani.com/creacion-de-un-chatbot-conversacional-con-memoria-usando-huggingface-y-openai-streamlitui-y-chromadb-como-bd-vectorial
