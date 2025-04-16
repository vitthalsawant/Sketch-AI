import os
import streamlit as st
from magic_hour import Client
import time
from dotenv import load_dotenv
import google.generativeai as genai
import urllib.request
import tempfile

# Load environment variables
load_dotenv()

# Configure API keys
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
MAGIC_HOUR_API_KEY = os.getenv('MAGIC_HOUR_API_KEY')

# Validate API keys
if not GOOGLE_API_KEY or not MAGIC_HOUR_API_KEY:
    st.error("Missing API keys. Please check your .env file or environment settings.")
    st.stop()

# Configure Generative AI API
genai.configure(api_key=GOOGLE_API_KEY)

# Set default parameters for Generative AI
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 1024,
}

# Initialize Generative AI model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config
)

# Initialize Magic Hour Client
client = Client(token=MAGIC_HOUR_API_KEY)

# Enhance the user prompt using Generative AI
def enhance_prompt(user_prompt):
    try:
        enhancement_prompt = f"""
        Enhance this image description to make it more detailed and artistic.
        Original prompt: {user_prompt}
        Return only the enhanced prompt without explanations or additional text.
        """
        response = model.generate_content(enhancement_prompt)
        return response.text.strip() if response.text else user_prompt
    except Exception as e:
        st.warning(f"Could not enhance prompt: {str(e)}. Using original prompt.")
        return user_prompt

# Streamlit App Interface
st.title("AI Sketch Generator")
st.write("Transform your descriptions into artistic sketches!")

# Input for sketch description
user_prompt = st.text_area(
    "Enter your sketch description:",
    help="Be as detailed as possible!"
)

# Style options
style_options = {
    "Sketch": "sketch",
    "Line Art": "line_art",
    "Minimalist": "minimalist",
    "Hand Drawn": "hand_drawn"
}
selected_style = st.selectbox("Choose art style:", options=list(style_options.keys()))

# Orientation options
orientation_options = {
    "Landscape": "landscape",
    "Portrait": "portrait",
    "Square": "square"
}
selected_orientation = st.selectbox("Choose orientation:", options=list(orientation_options.keys()))

# Generate Sketch Button Logic
if st.button("Generate Sketch"):
    if user_prompt.strip():
        try:
            # Enhance prompt
            with st.spinner("Enhancing your prompt with AI..."):
                enhanced_prompt = enhance_prompt(user_prompt)
                st.info("Enhanced prompt: " + enhanced_prompt)

            # Request sketch generation
            with st.spinner("Creating your sketch..."):
                try:
                    create_res = client.v1.ai_image_generator.create(
                        prompt=f"black and white sketch: {enhanced_prompt}",
                        orientation=orientation_options[selected_orientation],
                        style=style_options[selected_style]
                    )
                    st.info(f"Queued image with ID: {create_res.id} | Frames used: {create_res.frame_cost}")

                    # Poll for project completion
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    while True:
                        res = client.v1.image_projects.get(id=create_res.id)

                        if res.status == "complete":
                            progress_bar.progress(100)
                            if res.downloads and len(res.downloads) > 0:
                                # Download image to a temporary file
                                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
                                    with urllib.request.urlopen(res.downloads[0].url) as response:
                                        temp_file.write(response.read())
                                    temp_file_path = temp_file.name

                                # Display generated sketch
                                st.image(temp_file_path, caption="Your Generated Sketch")
                                st.success("✨ Sketch created successfully!")
                                
                                # Add download button
                                with open(temp_file_path, "rb") as file:
                                    st.download_button(
                                        label="Download Sketch",
                                        data=file,
                                        file_name="generated_sketch.png",
                                        mime="image/png"
                                    )
                            break
                        elif res.status == "error":
                            progress_bar.empty()
                            st.error("❌ Sketch generation failed. Please try again.")
                            break
                        else:
                            status_text.text(f"Status: {res.status}")
                            progress_bar.progress(50)
                            time.sleep(1)
                except Exception as e:
                    if "frames" in str(e).lower():
                        st.error("""
                        ⚠️ Insufficient frames to generate sketch!
                        Please visit https://magic.hour/account to:
                        1. Check frame balance
                        2. Upgrade plan for more frames
                        3. Contact support if needed
                        """)
                    else:
                        st.error(f"Error during sketch generation: {str(e)}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a description for your sketch.")