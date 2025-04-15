# 🎨 AI Sketch Generator

Transform your descriptions into beautiful black and white sketches powered by Magic Hour API and Google's Gemini AI.

![AI Sketch Generator]![image](https://github.com/user-attachments/assets/081e6fd9-47a1-4a04-91b9-d4924338cf33)


## ✨ Overview

AI Sketch Generator is a web application that converts text descriptions into artistic sketches. The application utilizes Google's Gemini 2.0 Flash model to enhance user prompts and Magic Hour's AI to generate high-quality sketch artwork.

## 🚀 Features

- **🧠 AI-Enhanced Prompts**: Uses Gemini AI to improve your descriptions for better results
- **🖌️ Multiple Art Styles**: Choose from Sketch, Line Art, Minimalist, and Hand Drawn styles
- **⚙️ Real-Time Generation**: Watch as your sketch comes to life with progress tracking
- **💾 Easy Downloads**: Download your generated sketches with one click
- **📊 Resource Management**: Track your remaining frames (API credits)

## 🛠️ Installation

### Prerequisites

- Python 3.7+
- Pip package manager
- Magic Hour API account
- Google Gemini API key

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/username/ai-sketch-generator.git
   cd ai-sketch-generator
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   MAGIC_HOUR_API_KEY=your_magic_hour_api_key_here
   ```

   > **Note**: You need to obtain API keys from [Google AI Studio](https://makersuite.google.com/app/apikey) and [Magic Hour](https://magic.hour/account).

## 📋 Usage

1. Start the application:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to `http://localhost:8501`

3. Enter a detailed description of the sketch you want to create

4. Select your preferred art style from the dropdown menu

5. Click "Generate Sketch" and wait for the magic to happen!

6. Download your sketch when it's ready

## 💡 Example Prompts

- "A serene mountain landscape with a small cabin and pine trees"
- "Portrait of a young woman with flowing hair looking at the horizon"
- "A futuristic cityscape with flying vehicles and tall skyscrapers"
- "A still life composition with a vintage camera, books, and a cup of coffee"

## 🧩 Art Styles

- **Sketch**: Traditional sketch with natural lines and shading
- **Line Art**: Clean, defined lines with minimal shading
- **Minimalist**: Simplified forms with essential elements only
- **Hand Drawn**: Organic, authentic hand-drawn aesthetic

## 📁 Project Structure

```
ai-sketch-generator/
├── app.py                # Main application file
├── .env                  # Environment variables (not tracked by git)
├── requirements.txt      # Project dependencies
├── README.md             # This file
└── images/               # Screenshots and images
    └── screenshot.png    # Application screenshot
```

## 📦 Dependencies

- `streamlit`: Web application framework
- `magic_hour`: Magic Hour API client
- `google-generativeai`: Google's Generative AI API client
- `python-dotenv`: Environment variable management

## 📋 Requirements

```
streamlit==1.32.0
magic-hour==1.0.0
google-generativeai==0.7.0
python-dotenv==1.0.0
```

## ⚠️ Usage Limitations

- Each sketch generation consumes 5 frames from your Magic Hour account
- The application requires a minimum of 5 frames available to operate
- Consider upgrading your Magic Hour plan if you need more frames

## 👋 Connect With The Developer

- 👔 [LinkedIn](https://www.linkedin.com/in/vitthal-sawant-maharastra01/)
- 📸 [Instagram](https://www.instagram.com/vitthal_sawant__/)
- 💬 [WhatsApp](https://wa.me/+918308075485)


## 🙏 Acknowledgments

- Magic Hour API for sketch generation capabilities
- Google Generative AI for providing the Gemini API
- Streamlit for the web application framework

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
