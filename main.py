import tempfile
import os
from PIL import Image
import streamlit as st
from streamlit_cropper import st_cropper
import io
import random

# Constants
SUPPORTED_FORMATS = ["png", "jpg", "jpeg"]
DEFAULT_AVATAR_SIZE = 1768
FRAME_POSITION = (250, 250)
# Fun elements
EMOJI_DECORATIONS = "🌈 ⭐ 🌟 ✨ 💫 🎨 🎭 🎪 🎯 🎪 🎨 🎭 ⭐ 🌟 ✨ 💫"
CONGRATULATION_EMOJIS = ["🎉", "🎊", "🥳", "🌟", "⭐", "💫", "✨", "🦄", "🌈", "🍭"]
LOADING_EMOJIS = ["🎨", "🖼️", "🎭", "🎪", "🎯", "🎨", "🎭", "🦄", "🌈", "🍭"]


class AvatarMerger:
    def __init__(self):
        self.setup_page()
        self.initialize_session_state()

    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'cropped_image' not in st.session_state:
            st.session_state.cropped_image = None
        if 'merged_image' not in st.session_state:
            st.session_state.merged_image = None
        if 'active_tab' not in st.session_state:
            st.session_state.active_tab = 0
        if 'expander_state' not in st.session_state:
            st.session_state.expander_state = True
        if 'previous_upload_state' not in st.session_state:
            st.session_state.previous_upload_state = None

    def setup_page(self):
        """Configure the Streamlit page settings and layout"""
        st.set_page_config(
            page_title="✨🦂💖 Nov 91-94 Avatar Frame Merger 💝🦂✨",
            page_icon="🦂",
            layout="wide"
        )

        st.markdown("""
            <style>
                /* Colorful headers */
                h1 {
                    background: linear-gradient(45deg, #FF69B4, #4B0082, #0000FF, #00FF00);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    font-size: 3em !important;
                    text-align: center;
                    padding: 20px 0;
                }
                h3 {
                    color: #FF69B4;
                    text-align: center;
                }
                /* Fun buttons */
                .stButton>button {
                    width: 100%;
                    background: linear-gradient(45deg, #FF69B4, #9370DB);
                    color: white;
                    border: none;
                    border-radius: 20px;
                    padding: 10px 20px;
                    font-size: 1.2em;
                    transition: all 0.3s ease;
                }
                .stButton>button:hover {
                    transform: scale(1.05);
                    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                }
                /* Playful success message */
                .success-message {
                    padding: 1rem;
                    border-radius: 20px;
                    background: linear-gradient(45deg, #87CEEB, #98FB98);
                    color: #4B0082;
                    text-align: center;
                    font-size: 1.2em;
                    margin: 20px 0;
                    animation: bounce 1s infinite;
                }
                /* Fun frame preview */
                .frame-preview {
                    border: 3px solid #FF69B4;
                    padding: 20px;
                    border-radius: 20px;
                    margin: 20px 0;
                    background: linear-gradient(45deg, rgba(255,192,203,0.1), rgba(147,112,219,0.1));
                }
                /* Animated tabs */
                .stTabs [data-baseweb="tab"] {
                    padding: 10px 20px;
                    background: linear-gradient(45deg, #FFB6C1, #DDA0DD);
                    color: white;
                    border-radius: 15px;
                    margin: 0 5px;
                    transition: all 0.3s ease;
                }
                .stTabs [data-baseweb="tab"]:hover {
                    transform: translateY(-2px);
                }
                /* Fun file uploader */
                .uploadedFile {
                    background: linear-gradient(45deg, #E6E6FA, #F0F8FF);
                    border-radius: 15px;
                    padding: 10px;
                }
                /* Bouncing animation */
                @keyframes bounce {
                    0%, 100% { transform: translateY(0); }
                    50% { transform: translateY(-10px); }
                }
            </style>
        """, unsafe_allow_html=True)

    def get_random_emoji(self, emoji_list):
        return random.choice(emoji_list)

    def load_frame(self):
        """Load the frame image"""
        try:
            frame_path = os.path.join(os.path.dirname(__file__), "nov2024frame.png")
            return Image.open(frame_path)
        except Exception as e:
            st.error(f"Error loading frame: {str(e)}")
            return None

    def display_frame(self, frame_image):
        """Display the frame in a consistent location"""
        with st.container():
            st.markdown('<div class="frame-preview">', unsafe_allow_html=True)
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(frame_image, caption="Frame Template", use_column_width=True)
            with col2:
                st.markdown(f"""
                    ### 🎨 Khung gốc by Dung PMU {self.get_random_emoji(CONGRATULATION_EMOJIS)}
                    Khung này cực đẹp nhưng hơi kén hình. 
                    Chọn ảnh thật khéo và vùng ảnh đẹp nhất bạn nhá.

                    ✨ Tips ✨:
                    - 🎯 Chọn chủ thể trong hình vuông
                    - 🌟 Có thể phải thêm ít không gian xung quanh chủ thể
                    - 🎪 Kết quả sẽ luôn là avatar vuông nhá 
                """)
            st.markdown('</div>', unsafe_allow_html=True)

    def crop_image(self, image):
        """Crop the uploaded image and update preview"""
        width, height = image.size
        crop_size = min(width, height)

        # Calculate center crop coordinates
        left = (width - crop_size) / 2
        top = (height - crop_size) / 2
        right = (width + crop_size) / 2
        bottom = (height + crop_size) / 2

        st.markdown("### ✂️ Crop Your Image")
        st.markdown("Kéo các góc để chọn vùng ảnh. Vùng chọn sẽ luôn là hình vuông để hợp với khung gốc.")

        cropped_image = st_cropper(
            image,
            aspect_ratio=(1, 1),
            default_coords=(left, right, top, bottom),
            box_color='#FF0000',
            return_type='image'
        )

        if cropped_image:
            st.session_state.cropped_image = cropped_image
            # Automatically generate merged preview when crop changes
            if st.session_state.get('frame_image'):
                st.session_state.merged_image = self.merge_images(
                    cropped_image,
                    st.session_state.frame_image
                )

        return cropped_image

    def merge_images(self, avatar_image, frame_image):
        """Merge the avatar with the frame"""
        try:
            avatar = avatar_image.convert("RGBA")
            frame = frame_image.convert("RGBA")

            width, height = avatar.size
            if height == 0:
                st.error("Invalid image height. Please try a different image.")
                return None

            aspect_ratio = width / height
            new_width = DEFAULT_AVATAR_SIZE
            new_height = int(new_width / aspect_ratio)
            avatar = avatar.resize((new_width, new_height))

            new_avatar_image = Image.new("RGBA", frame.size)
            new_avatar_image.paste(avatar, FRAME_POSITION, mask=avatar)

            return Image.alpha_composite(new_avatar_image, frame)

        except Exception as e:
            st.error(f"Error merging images: {str(e)}")
            return None

    def download_result(self, merged_image):
        """Create download button with improved UI"""
        img_bytes = io.BytesIO()
        merged_image.save(img_bytes, format="PNG", optimize=True)

        if st.download_button(
                label="⬇️ Tải Avatar của bạn",
                data=img_bytes.getvalue(),
                file_name="custom_avatar.png",
                mime="image/png",
                key="download_button"
        ):
            st.markdown(
                '<div class="success-message">✅ Đã tải xong. Bạn kiểm tra phần Tải về trên trình duyệt.</div>',
                unsafe_allow_html=True
            )

    def run(self):
        """Main application logic"""
        st.title("✨🦂💖 Nov 91-94 Avatar Frame Merger 💝🦂✨")

        # Load and store frame image in session state
        if 'frame_image' not in st.session_state:
            st.session_state.frame_image = self.load_frame()

        # File uploader outside expander to track state
        upload_help = f"Supported formats: {', '.join(SUPPORTED_FORMATS)}"
        avatar_file = st.file_uploader(
            "Chọn ảnh của bạn",
            type=SUPPORTED_FORMATS,
            help=upload_help,
            key="uploader",
            label_visibility="collapsed"
        )

        # Check for new upload and update expander state
        if avatar_file != st.session_state.previous_upload_state:
            st.session_state.previous_upload_state = avatar_file
            st.session_state.expander_state = not bool(avatar_file)
            #st.experimental_rerun()

        # Input section in expander
        with st.expander("📤 Upload Your Image", expanded=st.session_state.expander_state):
            # Always display frame at the top
            if st.session_state.frame_image:
                self.display_frame(st.session_state.frame_image)

            # File upload section
            st.file_uploader(
                "Chọn ảnh của bạn",
                type=SUPPORTED_FORMATS,
                help=upload_help,
                key="uploader_in_expander",
                label_visibility="visible"
            )

        if avatar_file:
            try:
                image = Image.open(avatar_file)

                # Create tabs
                tabs = st.tabs([
                    "✂️ Crop",
                    "👀 Xem trước",
                    "🎉 Kết quả"
                ])

                # Set active tab to Crop when image is first uploaded
                if st.session_state.get('_uploaded_file') != avatar_file:
                    st.session_state.active_tab = 0
                    st.session_state._uploaded_file = avatar_file

                # Crop tab
                with tabs[0]:
                    cropped_avatar = self.crop_image(image)

                # Preview tab
                with tabs[1]:
                    if st.session_state.cropped_image is not None:
                        st.markdown("### 👀 Xem vùng ảnh đã chọn")
                        st.image(st.session_state.cropped_image, use_column_width=True)
                        if st.button("✨ Tuyệt! Cho tôi kết quả!", key="preview"):
                            st.session_state.active_tab = 2
                            #st.experimental_rerun()

                # Final result tab
                with tabs[2]:
                    if st.session_state.merged_image is not None:
                        st.markdown("### 🎉 Avatar của bạn đã sẵn sàng!")
                        # Create a container for the download button/message
                        download_container = st.empty()
                        st.info("Nếu chưa ưng quay lại sửa. Còn ưng thì chờ tí nút tải sẽ hiện lên ở đây nhá!!!")
                        st.image(st.session_state.merged_image, use_column_width=True)
                        # Create download button in the container
                        with download_container:
                            img_bytes = io.BytesIO()
                            st.session_state.merged_image.save(img_bytes, format="PNG", optimize=True)

                            if st.download_button(
                                    label="⬇️ Tải Avatar của bạn",
                                    data=img_bytes.getvalue(),
                                    file_name="custom_avatar.png",
                                    mime="image/png",
                                    key="download_button"
                            ):
                                st.markdown(
                                    '<div class="success-message">✅ Đã tải xong. Bạn kiểm tra phần Tải về trên trình duyệt.</div>',
                                    unsafe_allow_html=True
                                )
                    else:
                        st.info("Chọn vùng ảnh gốc để ghép vào khung!")

            except Exception as e:
                st.error(f"Lỗi xử lý ảnh: {str(e)}")
                st.info("Mời bạn chọn ảnh khác.")
                st.session_state.expander_state = True
        else:
            st.info("👆 Đầu tiên là tải ảnh lên!")
            st.session_state.expander_state = True


if __name__ == "__main__":
    app = AvatarMerger()
    app.run()