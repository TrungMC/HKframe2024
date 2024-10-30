import tempfile
import os
import tempfile
import requests
from PIL import Image, PngImagePlugin
import streamlit as st
from streamlit_cropper import st_cropper
import io
# Frame: 1958x1958
# Visible:1500x1500
# Position:
def crop_image1(image):
    aspect_dict = {
        "1:1": (1, 1),
        "16:9": (16, 9),
        "4:3": (4, 3),
        "2:3": (2, 3),
        "Free": None
    }
    st.markdown("### 📏 Chọn vùng ảnh đẹp nhất bạn nhá!")
    cropped_image = st_cropper(image, aspect_ratio=(1,1),)
    # cropped_image = image
    return cropped_image
def crop_image(image):
    #aspect_dict = { "1:1": (1, 1), "16:9": (16, 9), "4:3": (4, 3), "2:3": (2, 3), "Free": None }
    st.markdown("Chọn vùng ảnh đẹp nhất bạn nhá!")
    # Get image dimensions
    width, height = image.size
    # Calculate the largest 1:1 ratio in the center
    crop_size = min(width, height)
    left = (width - crop_size) / 2
    top = (height - crop_size) / 2
    right = (width + crop_size) / 2
    bottom = (height + crop_size) / 2
    # Set the default coordinates for the cropper
    cropped_image = st_cropper(
        image, aspect_ratio=(1, 1),
        default_coords=(left,right,top, bottom),
        box_color='#FF0000',
        return_type='image'
    )
    return cropped_image

def merge_images(avatar_image, frame_image):
    # Open the avatar and frame images using PIL
    try:
        avatar = avatar_image.convert("RGBA")

        frame = frame_image.convert("RGBA")

        width, height = avatar.size
        if height==0:
            st.error("Lỗi xử lý Avatar. Hệ thống chỉ hỗ trợ các định dạng ảnh jpg")
            return None

        aspect_ratio = width / height
        new_width = 1768
        new_height = int(new_width / aspect_ratio)
        avatar = avatar.resize((new_width, new_height))

        # Create a new blank image with transparent background
        new_avatar_image = Image.new("RGBA", frame.size)
        # Calculate the position to place the avatar in the middle of the frame
        position = (250,250) #((frame.width - avatar.width) // 2, (frame.height - avatar.height) // 2)
        # Paste the resized avatar onto the blank frame image at the calculated position
        new_avatar_image.paste(avatar, position, mask=avatar)

        # Combine the avatar and frame images
        merged_image = Image.alpha_composite(new_avatar_image, frame)

        return merged_image
    except Exception as e:
        st.error(f"Error merging images: {str(e)}")
        return None


def frame_image():
    frame_image_path = os.path.join(os.path.dirname(__file__), "nov2024frame.png")
    frame_image_content = Image.open(frame_image_path)
    return frame_image_content


def download_result(merged_image):
    img_bytes = io.BytesIO()
    merged_image.save(img_bytes, format="PNG")

    # Create a download button for the image
    if st.download_button(
            label="Download Avatar",
            data=img_bytes.getvalue(),
            file_name="nov9194_avatar_4u.png",
            mime="image/png",
            key="download_button"
    ):
        # Add a message after the download
           st.markdown(
            '<div class="success-message">✅ Tải tệp tin thành công. Avatar của bạn được lưu trong thư mục Download của trình duyệt!</div>',
            unsafe_allow_html=True
        )


def app():
    # st.title("Nov 91-94 Avatar Merger-v2024")

    st.set_page_config(page_title="Nov 91-94 Frame Merger-one in a year", page_icon=":shark:")
    st.markdown("<h1 style='color: purple;'>🎨 Nov 91-94 Avatar Merger-v2024</h1>", unsafe_allow_html=True)
    st.subheader("💖💝!!!")
    with st.expander("🖼️ Frame gốc by Dung PMU"):
        # Load the frame image from the local file
        frame_image_content = frame_image()
        if frame_image_content:
            st.image(frame_image_content, caption="From PMU with love!")

    # File uploader for the avatar image
    avatar_expander=st.expander("### 📤Ảnh avatar của bạn",expanded=True)
    avatar_image = avatar_expander.file_uploader(
        "Tải ảnh lên",
        type=["png", "jpg", "jpeg"],
        help="Định dạng hỗ trợ: png, jpg, jpeg"
    )

    if avatar_image is not None:
        try:
            avatar_expander.empty()
            # Read the image file
            image = Image.open(avatar_image)

            # Allow user to select a rectangular area for cropping
            cropped_avatar = crop_image(image)
            # Allow user to select a rectangular area for the avatar
            # cropped_avatar = crop_image(avatar_image.convert('RGBA'))

            if cropped_avatar and frame_image_content:
                merged_image = merge_images(cropped_avatar, frame_image_content)

                # Save the merged image to a temporary file
                #temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                #merged_image.save(temp_file.name)
                if merged_image:

                    # Display the merged image
                    st.markdown("Phew, xong rồi. Avatar của bạn đây!")
                    st.image(merged_image)

                    # Download link for the merged image
                    download_result(merged_image)
                else:
                    st.markdown("Chán quá. Lỗi gì rồi. Bạn đổi ảnh khác xem. Định dạng jpeg nhá!")
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
            st.info("Please try uploading a different image.")

def get_download_link(file_path, link_text):
    href = f'<a href="{file_path}" download="{link_text}">{link_text}</a>'
    return href


if __name__ == "__main__":
    app()
