import os
import streamlit as st
from magic_hour import Client
import time
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    st.error("API key not found. Please check your .env file.")
    st.stop()
genai.configure(api_key=GOOGLE_API_KEY)

# Configure Magic Hour Client
MAGIC_HOUR_API_KEY = os.getenv('MAGIC_HOUR_API_KEY')
if not MAGIC_HOUR_API_KEY:
    st.error("Magic Hour API key not found. Please check your .env file.")
    st.stop()

client = Client(token=MAGIC_HOUR_API_KEY)

# Set default parameters for the model
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

def enhance_prompt(user_prompt):
    try:
        enhancement_prompt = f"""Enhance this image description to make it more detailed and artistic. 
        Focus on visual elements, style, and artistic details. Keep it concise but descriptive.
        Original prompt: {user_prompt}
        
        Enhanced prompt should include:
        1. Main subject and composition
        2. Artistic style and mood
        3. Key visual elements and details
        4. Lighting and atmosphere
        
        Return only the enhanced prompt without any explanations or additional text."""
        
        response = model.generate_content(enhancement_prompt)
        return response.text.strip() if response.text else user_prompt
    except Exception as e:
        st.warning(f"Could not enhance prompt: {str(e)}. Using original prompt.")
        return user_prompt

# Initialize the Streamlit app
st.title("AI Sketch Generator")
st.write("Transform your descriptions into beautiful sketches!")

# Input section for sketch description
user_prompt = st.text_area("Enter your sketch description:", "", 
                          help="Describe what you want to sketch. Be as detailed as possible!")

# Style options
style_options = {
    "Sketch": "sketch",
    "Line Art": "line_art",
    "Minimalist": "minimalist",
    "Hand Drawn": "hand_drawn"
}
selected_style = st.selectbox("Choose your art style:", options=list(style_options.keys()))

# Generate sketch based on prompt
if st.button("Generate Sketch"):
    if user_prompt.strip():
        try:
            with st.spinner("Enhancing your prompt with AI..."):
                # Enhance the prompt using Gemini
                enhanced_prompt = enhance_prompt(user_prompt)
                st.info("Enhanced prompt: " + enhanced_prompt)
                
                with st.spinner("Creating your artistic sketch..."):
                    try:
                        # Create sketch generation request with enhanced prompt
                        params = {
                            "prompt": f"black and white sketch, minimal lines, artistic drawing style: {enhanced_prompt}",
                            "style": style_options[selected_style],
                            "artistic_style": "sketch",
                            "color_scheme": "monochrome"
                        }
                        create_res = client.v1.ai_image_generator.create(**params)

                        # Poll for completion
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        while True:
                            res = client.v1.image_projects.get(id=create_res.id)
                            
                            if res.status == "complete":
                                progress_bar.progress(100)
                                if res.downloads and len(res.downloads) > 0:
                                    st.image(res.downloads[0].url, caption="Your Generated Sketch")
                                    st.success("✨ Sketch created successfully!")
                                    
                                    # Add download button
                                    st.markdown(f"[Download Sketch]({res.downloads[0].url})")
                                break
                            elif res.status == "error":
                                progress_bar.empty()
                                st.error("❌ Sketch generation failed")
                                break
                            else:
                                # Update progress indication
                                status_text.text(f"Status: {res.status}")
                                progress_bar.progress(50)
                                time.sleep(1)
                    except Exception as e:
                        if "frames" in str(e).lower():
                            st.error("""
                            ⚠️ Insufficient frames to generate sketch!
                            
                            Each sketch generation costs 5 frames.
                            Please visit https://magic.hour/account to:
                            1. Check your current frame balance
                            2. Upgrade your plan to get more frames
                            3. Contact support for assistance
                            """)
                        else:
                            raise e

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a description for your sketch.")