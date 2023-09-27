import os 
import vecs
from PIL import Image
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client
from streamlit_supabase_auth import login_form, logout_button
from sentence_transformers import SentenceTransformer

def create_collection(images_arr, conn):
    with vecs.create_client(conn) as vx:
    # create a new collection with an associated adapter
      st.toast('Creating collection...')
      images = vx.get_or_create_collection(name="image_vectors", dimension=512)

      # Load CLIP model
      model = SentenceTransformer('clip-ViT-B-32')
      
      vectors = []
      for image in images_arr:
          vectors.append((
              image["name"],        # the vector's identifier
              model.encode(Image.open(image["name"])),          # the vector. list or np.array
              {"type": image['name'].split(".")[1]}   # associated  metadata            )
          ))

      # add records to the *images* collection
      images.upsert(
          vectors
      )
      st.toast("Uploaded images to collection")

      # index the collection for fast search performance
      images.create_index()
      st.toast("Index created")

def upload_files_button(files, client, conn):
    st.session_state.clicked_upload = True
    if files != []:
        st.toast("Uploading images...")
        images = []
        for file in files:
            images.append({"name": file.name})
            with open(file.name, "wb") as f:
                f.write(file.getbuffer())

            with open(file.name, "rb") as f:
                client.storage.from_('images').upload(
                    path=file.name,
                    file=f,
                    file_options={
                    "content-type": file.type,
                    "x-upsert": "true",
                    },
            )
        create_collection(images, conn)
        st.toast('Done')  

def result_search_button(text_search, conn, image_url):
    if text_search != "":
      with vecs.create_client(conn) as vx:
        images = vx.get_collection(name="image_vectors")

        # Load CLIP model
        model = SentenceTransformer('clip-ViT-B-32')
        # Encode text query

        # query_string = "a man with a laptop"
        text_emb = model.encode(text_search)

        # query the collection filtering metadata for "type" = "jpg" or "png"
        results = images.query(
            data=text_emb,              # required
            limit=3,                            # number of records to return
            filters={"$or": [
                        {"type": {"$eq": "jpg"}},
                        {"type": {"$eq": "png"}},
                    ]},   # metadata filters
            # measure="cosine_distance",  # distance measure
            # include_value = True
            # probes = 1,
        )

        groups = []
        for i in range(0,len(results),5):
            group_names = [file for file in results[i:i+5]]
            groups.append(group_names)

        for group in groups:
            col = st.columns(5)
            for i, image_file in enumerate(group):
                col[i].image(image_url + image_file)
        
        no_search = False


def main():

    # Load environment variables.
    load_dotenv()
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("PASSWORD")
    db_host = os.getenv("HOST")
    db_port = os.getenv("PORT")
    db_name = os.getenv("DB_NAME")

    # Initialize connection.
    # print(user, password, host, db_port, db_name)
    db_connection = "postgresql://" + db_user + ":" + db_password + "@" + db_host + ":" + db_port + "/" + db_name
    # db_connection = "postgresql://postgres:" + password + "@db.mnsfnlvrzlybpibcvvit.supabase.co:5432/postgres"


    supabase_client = create_client(
    supabase_key=supabase_key, supabase_url=supabase_url
    )

    session = login_form(
        url=supabase_url,
        apiKey=supabase_key,
        # providers=["apple", "facebook", "github", "google"],
    )

    # Variables
    no_search = True
    url = "https://mnsfnlvrzlybpibcvvit.supabase.co/storage/v1/object/public/images/"
    
    if 'clicked_upload' not in st.session_state:
        st.session_state.clicked_upload = False

    if session: 
        st.experimental_set_query_params(page=["success"])
        with st.sidebar:
            st.write(f"Welcome {session['user']['email']}")
            
            logout_button()

            # Add file uploader
            st.info("Please note that the uploaded images will be public and will be displayed in the grid. 👉")
            uploaded_files = st.file_uploader("images", type=['png', 'jpg'] , accept_multiple_files=True, label_visibility= 'hidden')

            st.button("Upload", on_click=upload_files_button, args=[uploaded_files, supabase_client, db_connection])

            if st.session_state.clicked_upload and (uploaded_files == []):
                st.warning("No files uploaded, please upload a file")

            # uploaded_files = []
            
        # App title
        st.header(":mag: :blue[Image Search Engine with] :green[Supabase]")
        st.subheader("You can upload your own image or search for a specific one")

        # Search box
        text_search = st.text_input(label= "Search image", label_visibility= 'hidden', placeholder="Search a specific image", value="")

        if st.button("Search"):
            no_search = False
            result_search_button(text_search, db_connection, url)

        if no_search:
            groups = []
            
            all_files = supabase_client.storage.from_('images').list('', {'sortBy': {'column':'created_at', 'order': 'asc'}})
            if all_files != []:
                for i in range(1,len(all_files),5):
                    group_names = [file["name"] for file in all_files[i:i+5]]
                    groups.append(group_names)

                # print(groups)
                for group in groups:
                    # print(group)
                    col = st.columns(5)
                    for i, image_file in enumerate(group):
                        col[i].image(url + image_file)
    
    

if __name__ == '__main__':
  main()
