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

# API keys setup
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
MAGIC_HOUR_API_KEY = os.getenv('MAGIC_HOUR_API_KEY')

# Check API keys and stop execution if they're missing
if not GOOGLE_API_KEY or not MAGIC_HOUR_API_KEY:
    st.error("Missing API keys. Please check your .env file.")
    st.stop()

# Configure APIs
genai.configure(api_key=GOOGLE_API_KEY)
client = Client(token=MAGIC_HOUR_API_KEY)

# Default parameters for the Gemini model
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 1024,
}

# Initialize the Gemini model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config
)

# Function to enhance the user prompt
def enhance_prompt(user_prompt):
    try:
        enhancement_prompt = f"""
        Enhance this image description to make it more detailed and artistic.
        Focus on visual elements, style, and artistic details. 
        Original prompt: {user_prompt}
        
        Enhanced prompt should include:
        - Main subject and composition
        - Artistic style and mood
        - Key visual elements and details
        - Lighting and atmosphere
        
        Return only the enhanced prompt without any explanations or additional text.
        """
        response = model.generate_content(enhancement_prompt)
        return response.text.strip() if response.text else user_prompt
    except Exception as e:
        st.warning(f"Could not enhance prompt: {str(e)}. Using original prompt.")
        return user_prompt

# Streamlit app setup
st.title("AI Sketch Generator")
st.write("Transform your descriptions into beautiful sketches!")

# Input section for sketch description
user_prompt = st.text_area(
    "Enter your sketch description:",
    "",
    help="Describe what you want to sketch. Be as detailed as possible!"
)

# Style options
style_options = {
    "Sketch": "sketch",
    "Line Art": "line_art",
    "Minimalist": "minimalist",
    "Hand Drawn": "hand_drawn"
}
selected_style = st.selectbox("Choose your art style:", options=list(style_options.keys()))

# Orientation options
orientation_options = {
    "Landscape": "landscape",
    "Portrait": "portrait",
    "Square": "square"
}
selected_orientation = st.selectbox("Choose orientation:", options=list(orientation_options.keys()))

# Generate sketch based on prompt
if st.button("Generate Sketch"):
    if user_prompt.strip():
        try:
            with st.spinner("Enhancing your prompt with AI..."):
                # Enhance the prompt
                enhanced_prompt = enhance_prompt(user_prompt)
                st.info("Enhanced prompt: " + enhanced_prompt)
                
                with st.spinner("Creating your artistic sketch..."):
                    try:
                        # Creating sketch generation request
                        create_res = client.v1.ai_image_generator.create(
                            image_count=1,
                            orientation=orientation_options[selected_orientation],
                            style={
                                "prompt": f"black and white sketch: {enhanced_prompt}"
                            }
                        )
                        
                        st.info(f"Queued image with ID: {create_res.id} | Frames used: {create_res.frame_cost}")
                        
                        # Poll for completion
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        while True:
                            res = client.v1.image_projects.get(id=create_res.id)
                            
                            if res.status == "complete":
                                progress_bar.progress(100)
                                if res.downloads and len(res.downloads) > 0:
                                    # Download the image to a temporary file
                                    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
                                        with urllib.request.urlopen(res.downloads[0].url) as response:
                                            temp_file.write(response.read())
                                        temp_file_path = temp_file.name
                                    
                                    # Display the image
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
                                st.error("❌ Sketch generation failed")
                                break
                            else:
                                status_text.text(f"Status: {res.status}")
                                progress_bar.progress(50)
                                time.sleep(1)
                    except Exception as e:
                        if "frames" in str(e).lower():
                            st.error("""
                            ⚠️ Insufficient frames to generate sketch!
                            Each sketch generation costs frames.
                            Please visit https://magic.hour/account to:
                            1. Check your current frame balance
                            2. Upgrade your plan for more frames
                            3. Contact support for assistance
                            """)
                        else:
                            st.error(f"Error during sketch generation: {str(e)}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a description for your sketch.")