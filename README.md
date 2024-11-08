# PDF to Audiobook Converter

This is a web application that converts PDF files into audio files, creating a personalized audiobook experience. Users can upload a PDF, choose a text-to-speech (TTS) engine (offline or online), and generate an audio version of the document. This application supports both offline (using `pyttsx3`) and online (using Google TTS - `gTTS`) TTS engines with multiple language options.

## Features

- **PDF Upload**: Upload a PDF document to convert into an audio file.
- **TTS Engine Choice**: Choose between offline (pyttsx3) and online (Google TTS - gTTS) TTS engines.
- **Voice and Language Selection**: Customize the narration by choosing different voices or language codes.
- **Responsive UI**: Designed with Bootstrap for a modern and user-friendly interface.

## Technologies Used

- **Python** (for backend processing of PDF and TTS conversion)
- **Flask** (for handling requests and routing)
- **pyttsx3** (offline TTS engine)
- **gTTS** (Google TTS for online voice generation)
- **Bootstrap** (for front-end styling)

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/pdf-to-audiobook.git
   cd pdf-to-audiobook
   ```

2. **Install Dependencies**
   Install the required Python packages using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   Start the Flask server:
   ```bash
   python app.py
   ```

4. **Access the Application**
   Open your browser and go to:
   ```
   http://127.0.0.1:5001
   ```

## Usage

1. **Upload a PDF**: Click on the file input to select and upload a PDF document.
2. **Choose TTS Engine**: Select either `pyttsx3` (offline) or `gTTS` (online) from the dropdown menu.
3. **Set Voice/Language Options**:
   - If you selected `pyttsx3`, choose a voice from the dropdown.
   - If you selected `gTTS`, use the search-enabled dropdown to select a language.
4. **Generate Audiobook**: Click the "Generate Audiobook" button to create your audio file.

## Language Codes for Google TTS

If using Google TTS (`gTTS`), you can choose from a variety of language codes:
- **en** - English
- **tr** - Turkish
- **fr** - French
- **de** - German
- **es** - Spanish

> Note: For more supported languages, see the [gTTS documentation](https://gtts.readthedocs.io/).

## Project Structure

```
pdf-to-audiobook/
├── app.py                    # Main application file
├── templates/
│   └── index.html            # Front-end HTML (Bootstrap-based)
├── static/
│   └── style.css             # Custom styles (if any)
└── README.md                 # Project documentation
```

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your message"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-branch
   ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Bootstrap](https://getbootstrap.com/) for responsive UI components.
- [pyttsx3](https://pypi.org/project/pyttsx3/) for offline TTS support.
- [gTTS](https://gtts.readthedocs.io/) for Google TTS support.

---

Thank you for using the PDF to Audiobook Converter!
```

This README file provides all necessary details for setting up, running, and contributing to the project. Make sure to replace placeholder links and paths (e.g., GitHub repository link, your username) with actual information.
