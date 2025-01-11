# Image Auto Edit

A simple and intuitive web application that allows users to upload images and enhance them using advanced HDR (High Dynamic Range) processing with denoising and smoothing. Built using **Streamlit**, this app provides side-by-side comparisons of original and enhanced images, offering a seamless experience for image improvement.

---

## Features

### 🎨 Image Enhancement
- Utilizes OpenCV's **HDR enhancement** for vibrant image processing.
- Smoothens and denoises the enhanced image for better quality output.
- Supports image formats: **JPG**, **JPEG**, and **PNG**.

### 🔒 Session Storage
- Uses Streamlit's session state to store the original and enhanced images.
- Allows users to clear uploaded and processed images easily from the sidebar.

### 🌐 Integrated Sidebar
- Displays a custom logo fetched dynamically from GitHub.
- Provides clear and actionable buttons for clearing images and managing memory efficiently.

### 🔄 Responsive Design
- Displays original and enhanced images side by side for easy comparison.
- Ensures an intuitive and visually appealing layout with columns.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/KirtanTankRed/image_auto_edit.git
   cd image_auto_edit
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

4. Open the application in your browser at:
   ```
   http://localhost:8501
   ```

---

## Usage

1. **Upload Image**: Drag and drop or select an image file in JPG, JPEG, or PNG format.
2. **Enhancement**: The app will process the image to enhance its visual quality using HDR and denoising techniques.
3. **Compare Images**: View the original and enhanced images side by side.
4. **Clear Images**: Use the sidebar's "Clear Images" button to remove images from session storage.

---

## Technologies Used

- **Python**: Programming language.
- **Streamlit**: Web application framework.
- **Pillow**: Image processing.
- **OpenCV**: Image enhancement and denoising.
- **Requests**: Fetching dynamic content from GitHub.

---

## Project Structure

```
image_auto_edit/
├── app.py                  # Main application file
├── requirements.txt        # Required dependencies
└── README.md               # Documentation (you are here!)
```

---

## Known Issues and Limitations

- 🛑 **Prototype**: This is a demo application and not suitable for production.
- ⚠️ **Limited Memory**: Ensure to clear session images to manage memory usage effectively.
- 🎨 **Limited Formats**: Only supports JPG, JPEG, and PNG image formats.

---

## Contributing

Contributions are welcome! If you have ideas to improve the app, feel free to open an issue or submit a pull request.

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request on GitHub.

---

## License

This project is not open-source. 
For permission to use, modify, or distribute this application, please contact the developer via email.

---

## Contact

For questions or feedback, please reach out to the developer:
- **Name**: Kirtan Tank
- **GitHub**: [KirtanTankRed](https://github.com/KirtanTankRed)
- **Email**: [kirtan.tank@redsoftware.in](mailto:kirtan.tank@redsoftware.in)

