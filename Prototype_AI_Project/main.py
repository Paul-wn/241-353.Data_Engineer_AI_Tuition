import streamlit as st
import cv2
import numpy as np
import requests
from PIL import Image
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO

# Set page config
st.set_page_config(
    page_title="Streamlit Mini Prototype",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"  # or "collapsed"
)

# Custom CSS for liquid blue theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap');
    
    /* Main theme colors */
    :root {
        --blue-primary: #3b82f6;
        --blue-secondary: #2563eb;
        --blue-accent: #1d4ed8;
        --blue-light: #dbeafe;
        --blue-dark: #1e40af;
        --glass-bg: rgba(255, 255, 255, 0.1);
        --glass-border: rgba(255, 255, 255, 0.2);
    }
    
    /* Background gradient */
    .stApp {
        background: linear-gradient(135deg, 
            #bfdbfe 0%, 
            #93c5fd 25%, 
            #60a5fa 50%, 
            #3b82f6 75%, 
            #2563eb 100%);
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        min-height: 100vh;
    }
    
    /* Glassmorphism containers */
    .main .block-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 24px;
        padding: 2rem;
        margin-top: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        animation: slideIn 0.6s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, 
            rgba(255, 255, 255, 0.15) 0%, 
            rgba(255, 255, 255, 0.05) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Headers */
    h1 {
        color: white;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        background: linear-gradient(45deg, #ffffff, #eff6ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    h2, h3 {
        color: white;
        font-weight: 600;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, var(--blue-primary), var(--blue-secondary));
        color: white;
        border: none;
        border-radius: 16px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-family: 'SF Pro Display', sans-serif;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
        background: linear-gradient(45deg, var(--blue-secondary), var(--blue-accent));
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Sliders */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, var(--blue-light), var(--blue-primary));
        border-radius: 8px;
    }
    
    .stSlider > div > div > div > div {
        background: white;
        border: 2px solid var(--blue-primary);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* Select boxes and inputs */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        color: white;
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        color: white;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.7);
    }
    
    /* File uploader */
    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 2px dashed rgba(255, 255, 255, 0.3);
        border-radius: 16px;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: var(--blue-primary);
        background: rgba(255, 255, 255, 0.15);
    }
    
    /* Metrics */
    .metric-container {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 0.5rem;
    }
    
    /* Sidebar labels */
    .css-1d391kg label {
        color: white !important;
        font-weight: 500;
    }
    
    /* Download button special styling */
    .stDownloadButton > button {
        background: linear-gradient(45deg, #1e40af, #1e3a8a);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-family: 'SF Pro Display', sans-serif;
        box-shadow: 0 4px 16px rgba(30, 64, 175, 0.3);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(30, 64, 175, 0.4);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: var(--blue-primary) !important;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: rgba(59, 130, 246, 0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 12px;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 12px;
    }
    
    /* Text colors */
    .stMarkdown p, .stText {
        color: white;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    /* Image containers */
    .stImage {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        transition: all 0.3s ease;
    }
    
    .stImage:hover {
        transform: scale(1.02);
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.2);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom floating effects */
    .floating {
        animation: floating 3s ease-in-out infinite;
    }
    
    @keyframes floating {
        0% { transform: translate(0, 0px); }
        50% { transform: translate(0, -10px); }
        100% { transform: translate(0, -0px); }
    }
</style>
""", unsafe_allow_html=True)

def load_image_from_url(url):
    """Load image from URL"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        return np.array(image)
    except Exception as e:
        st.error(f"Error loading image from URL: {str(e)}")
        return None

def apply_edge_detection(image, threshold1, threshold2):
    """Apply Canny edge detection"""
    if len(image.shape) == 3:
        # Convert RGB to BGR for OpenCV, then to grayscale
        bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    edges = cv2.Canny(gray, threshold1, threshold2)
    return edges

def apply_blur(image, kernel_size):
    """Apply Gaussian blur"""
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

def apply_brightness_contrast(image, brightness, contrast):
    """Adjust brightness and contrast"""
    # Convert to float to avoid overflow
    adjusted = np.clip(contrast * image + brightness, 0, 255)
    return adjusted.astype(np.uint8)

def apply_grayscale(image):
    """Convert to grayscale"""
    if len(image.shape) == 3:
        # Convert RGB to BGR for OpenCV, then to grayscale
        bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        return gray
    return image

def calculate_histogram(image):
    """Calculate color histogram"""
    if len(image.shape) == 3:
        # Color image - calculate histogram for each channel
        colors = ['red', 'green', 'blue']
        hist_data = []
        for i, color in enumerate(colors):
            hist = cv2.calcHist([image], [i], None, [256], [0, 256])
            hist_data.append((hist.flatten(), color))
        return hist_data
    else:
        # Grayscale image
        hist = cv2.calcHist([image], [0], None, [256], [0, 256])
        return [(hist.flatten(), 'gray')]

def main():
    st.title("💙 Image Processor")
    st.markdown('<p style="color: rgba(255,255,255,0.8); font-size: 1.2rem; margin-top: -1rem;">Transform your images with smooth, ocean-inspired processing</p>', unsafe_allow_html=True)
    
    # Add sidebar toggle info
    with st.expander("ℹ️ How to Toggle Sidebar", expanded=False):
        st.markdown("""
        **Toggle Sidebar Methods:**
        - 🖱️ **Click** the `<` or `>` arrow button (top-left of sidebar)
        - ⌨️ **Keyboard**: Press `Ctrl + Shift + A` (Windows/Linux) or `Cmd + Shift + A` (Mac)
        - 📱 **Mobile**: Swipe or tap the hamburger menu
        """)
    
    st.markdown("---")
    
    # Sidebar for controls
    st.sidebar.markdown("## 🎛️ Control Panel")
    
    # Image input section
    st.sidebar.markdown("### 📁 Image Source")
    input_method = st.sidebar.radio("Choose input method:", ["Upload Image", "Image URL"], horizontal=True)
    
    image = None
    
    if input_method == "Upload Image":
        uploaded_file = st.sidebar.file_uploader(
            "Choose an image file", 
            type=['png', 'jpg', 'jpeg', 'bmp', 'tiff']
        )
        if uploaded_file is not None:
            image = np.array(Image.open(uploaded_file))
    else:
        image_url = st.sidebar.text_input("Enter image URL:")
        if image_url:
            with st.spinner("Loading image from URL..."):
                image = load_image_from_url(image_url)
    
    if image is not None:
        # Image processing controls
        st.sidebar.markdown("### 🔧 Processing Studio")
        
        processing_type = st.sidebar.selectbox(
            "Select transformation:",
            ["Original", "Grayscale", "Edge Detection", "Blur", "Brightness/Contrast"],
            help="Choose how you want to transform your image"
        )
        
        processed_image = image.copy()
        
        if processing_type == "Grayscale":
            processed_image = apply_grayscale(image)
            
        elif processing_type == "Edge Detection":
            st.sidebar.markdown("**🔍 Edge Detection Settings**")
            threshold1 = st.sidebar.slider("Lower Threshold", 0, 255, 50, help="Lower edge detection threshold")
            threshold2 = st.sidebar.slider("Upper Threshold", 0, 255, 150, help="Upper edge detection threshold")
            processed_image = apply_edge_detection(image, threshold1, threshold2)
            
        elif processing_type == "Blur":
            st.sidebar.markdown("**🌫️ Blur Settings**")
            kernel_size = st.sidebar.slider("Blur Intensity", 1, 51, 15, step=2, help="Higher values create more blur")
            processed_image = apply_blur(image, kernel_size)
            
        elif processing_type == "Brightness/Contrast":
            st.sidebar.markdown("**☀️ Light & Contrast**")
            brightness = st.sidebar.slider("Brightness", -100, 100, 0, help="Adjust image brightness")
            contrast = st.sidebar.slider("Contrast", 0.1, 3.0, 1.0, 0.1, help="Adjust image contrast")
            processed_image = apply_brightness_contrast(image, brightness, contrast)
        
        # Main content area
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📷 Original Image")
            st.image(image, use_container_width=True)
            st.write(f"Shape: {image.shape}")
            if len(image.shape) == 3:
                st.write(f"Channels: {image.shape[2]}")
        
        with col2:
            st.subheader(f"✨ Processed Image ({processing_type})")
            # Handle grayscale images for display
            st.image(processed_image, use_container_width=True)
            st.write(f"Shape: {processed_image.shape}")
        
        # Histogram section
        st.markdown("---")
        st.subheader("📊 Image Histogram")
        
        # Choose which image to analyze
        analyze_option = st.radio(
            "Analyze histogram for:",
            ["Original Image", "Processed Image"],
            horizontal=True
        )
        
        target_image = image if analyze_option == "Original Image" else processed_image
        hist_data = calculate_histogram(target_image)
        
        # Create plotly histogram with grass theme
        fig = go.Figure()
        
        for hist, color in hist_data:
            fig.add_trace(go.Scatter(
                x=list(range(256)),
                y=hist,
                mode='lines',
                name=f'{color.title()} Channel',
                line=dict(color=color if color != 'gray' else '#3b82f6', width=3),
                fill='tonexty' if color == hist_data[0][1] else None,
                fillcolor=f'rgba(59, 130, 246, 0.3)' if color != 'gray' else 'rgba(37, 99, 235, 0.3)'
            ))
        
        fig.update_layout(
            title=f"📊 Color Distribution - {analyze_option}",
            xaxis_title="Pixel Intensity",
            yaxis_title="Frequency",
            hovermode='x unified',
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='SF Pro Display'),
            title_font=dict(size=20, color='white'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
            legend=dict(
                bgcolor='rgba(255,255,255,0.1)',
                bordercolor='rgba(255,255,255,0.2)',
                borderwidth=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Image statistics with custom styling
        st.markdown("---")
        st.subheader("📈 Image Analytics")
        
        col1, col2, col3 = st.columns(3)
        
        if len(target_image.shape) == 3:
            # Color image statistics
            with col1:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric("Mean Pixel Value", f"{np.mean(target_image):.2f}")
                st.metric("🔴 Red Channel", f"{np.mean(target_image[:,:,0]):.2f}")
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric("Standard Deviation", f"{np.std(target_image):.2f}")
                st.metric("🟢 Green Channel", f"{np.mean(target_image[:,:,1]):.2f}")
                st.markdown('</div>', unsafe_allow_html=True)
            with col3:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric("Min/Max Values", f"{np.min(target_image)}/{np.max(target_image)}")
                st.metric("🔵 Blue Channel", f"{np.mean(target_image[:,:,2]):.2f}")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Grayscale image statistics
            with col1:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric("Mean Pixel Value", f"{np.mean(target_image):.2f}")
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric("Standard Deviation", f"{np.std(target_image):.2f}")
                st.markdown('</div>', unsafe_allow_html=True)
            with col3:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric("Min/Max Values", f"{np.min(target_image)}/{np.max(target_image)}")
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Download processed image
        st.markdown("---")
        st.markdown('<div class="floating">', unsafe_allow_html=True)
        if st.button("💾 Export Processed Image"):
            # Convert to PIL Image for saving
            if len(processed_image.shape) == 2:
                pil_image = Image.fromarray(processed_image, mode='L')
            else:
                pil_image = Image.fromarray(processed_image)
            
            # Save to bytes
            img_buffer = BytesIO()
            pil_image.save(img_buffer, format='PNG')
            
            st.download_button(
                label="⬇️ Download PNG",
                data=img_buffer.getvalue(),
                file_name=f"liquid_blue_{processing_type.lower().replace('/', '_')}.png",
                mime="image/png"
            )
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # Welcome message with enhanced styling
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h2 style="font-size: 2rem; margin-bottom: 1rem;">💙 Welcome to Image Processor Studio  </h2>
            <p style="font-size: 1.2rem; color: rgba(255,255,255,0.8); margin-bottom: 2rem;">
                Experience the future of image processing 
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🚀 **Quick Start Guide:**
            1. **📸 Upload** your image or paste a URL
            2. **🎨 Choose** your processing style
            3. **⚡ Adjust** parameters in real-time
            4. **📊 Analyze** pixel distributions
            5. **💾 Export** your masterpiece
            
            ### ✨ **Processing Arsenal:**
            - **🔳 Grayscale**: Elegant monochrome conversion
            - **🔍 Edge Detection**: Reveal hidden structures
            - **🌫️ Blur**: Smooth artistic effects
            - **☀️ Light Control**: Perfect brightness & contrast
            """)
        
        with col2:
            st.markdown("""
            ### 🎯 **Sample URLs to Try:**
            ```
            Nature Scene:
            https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800
            
            Urban Architecture:
            https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800
            
            Portrait Photography:
            https://images.unsplash.com/photo-1494790108755-2616b612b77c?w=800
            ```
            
            ### 💡 **Pro Tips:**
            - Use **Edge Detection** for architectural photos
            - Try **Blur** for dreamy landscapes  
            - **Brightness/Contrast** for portrait enhancement
            - Check the **histogram** for exposure analysis
            """)
            
        st.markdown('<div class="floating" style="text-align: center; margin-top: 2rem; font-size: 1.1rem; color: rgba(255,255,255,0.7);">Start by uploading an image or entering a URL in the sidebar ➡️</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()