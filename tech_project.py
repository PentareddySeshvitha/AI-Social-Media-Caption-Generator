import streamlit as st
import ollama
import base64


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Social Media Caption Generator",
    page_icon="✨",
    layout="centered"
)


# ============================================================
# TITLE
# ============================================================

st.title("✨ AI Social Media Caption Generator")

st.write(
    "Generate creative social media captions using "
    "Ollama AI and Streamlit."
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Caption Settings")

platform = st.sidebar.selectbox(
    "Select Platform",
    [
        "Instagram",
        "LinkedIn",
        "Twitter/X",
        "Facebook"
    ]
)

tone = st.sidebar.selectbox(
    "Select Tone",
    [
        "Creative",
        "Professional",
        "Funny",
        "Friendly",
        "Inspirational",
        "Casual"
    ]
)

length = st.sidebar.selectbox(
    "Caption Length",
    [
        "Short",
        "Medium",
        "Long"
    ]
)

hashtags = st.sidebar.checkbox(
    "Include Hashtags",
    value=True
)


# ============================================================
# TABS
# ============================================================

text_tab, image_tab = st.tabs(
    [
        "📝 Text Caption",
        "🖼️ Image Caption"
    ]
)


# ============================================================
# TEXT CAPTION GENERATOR
# ============================================================

with text_tab:

    st.header("📝 Generate Caption from Text")

    topic = st.text_area(
        "Describe your post",
        placeholder=(
            "Example: College friends enjoying "
            "a beautiful sunset at the beach..."
        ),
        height=120
    )

    if st.button(
        "✨ Generate Caption",
        use_container_width=True
    ):

        if topic.strip() == "":

            st.warning(
                "⚠️ Please enter a description."
            )

        else:

            # Hashtag instruction
            if hashtags:
                hashtag_text = (
                    "Include 3 to 5 relevant hashtags."
                )
            else:
                hashtag_text = (
                    "Do not include hashtags."
                )

            # AI Prompt
            prompt = f"""
You are an AI Social Media Caption Generator.

Create a social media caption using the
following information.

Post description:
{topic}

Platform:
{platform}

Tone:
{tone}

Length:
{length}

Hashtag requirement:
{hashtag_text}

Rules:
- Create an original caption.
- Make it creative and engaging.
- Match the selected platform.
- Match the selected tone.
- Do not explain the answer.
- Return only the final caption.
"""

            try:

                with st.spinner(
                    "🤖 Generating caption..."
                ):

                    response = ollama.chat(
                        model="llama3.2",
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )

                caption = response["message"]["content"]

                st.success(
                    "✅ Caption generated successfully!"
                )

                st.subheader("Generated Caption")

                st.text_area(
                    "Your Caption",
                    caption,
                    height=180
                )

                st.download_button(
                    "📥 Download Caption",
                    caption,
                    file_name="caption.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            except Exception as e:

                st.error(
                    "❌ Could not connect to Ollama."
                )

                st.info(
                    "Make sure Ollama is installed and "
                    "llama3.2:3b is downloaded."
                )

                st.code(str(e))


# ============================================================
# IMAGE CAPTION GENERATOR
# ============================================================

with image_tab:

    st.header("🖼️ Generate Caption from Image")

    st.write(
        "Upload an image and LLaVA will analyze it "
        "and generate a caption."
    )

    uploaded_image = st.file_uploader(
        "Upload Image",
        type=[
            "jpg",
            "jpeg",
            "png"
        ]
    )

    if uploaded_image is not None:

        st.image(
            uploaded_image,
            caption="Uploaded Image",
            use_container_width=True
        )

        if st.button(
            "🖼️ Generate Image Caption",
            use_container_width=True
        ):

            if hashtags:
                hashtag_text = (
                    "Include 3 to 5 relevant hashtags."
                )
            else:
                hashtag_text = (
                    "Do not include hashtags."
                )

            # Read image
            image_bytes = uploaded_image.read()

            # Convert image to Base64
            image_base64 = base64.b64encode(
                image_bytes
            ).decode("utf-8")

            # AI Prompt
            prompt = f"""
Analyze the uploaded image and create a
social media caption.

Platform:
{platform}

Tone:
{tone}

{hashtag_text}

Rules:
- Understand the main subject of the image.
- Create a creative and engaging caption.
- Do not invent details that cannot be seen.
- Make it suitable for the selected platform.
- Return only the final caption.
"""

            try:

                with st.spinner(
                    "👁️ AI is analyzing the image..."
                ):

                    response = ollama.chat(
                        model="llava",
                        messages=[
                            {
                                "role": "user",
                                "content": prompt,
                                "images": [
                                    image_base64
                                ]
                            }
                        ]
                    )

                caption = response["message"]["content"]

                st.success(
                    "✅ Image caption generated!"
                )

                st.subheader("Generated Caption")

                st.text_area(
                    "Your Caption",
                    caption,
                    height=180
                )

                st.download_button(
                    "📥 Download Caption",
                    caption,
                    file_name="image_caption.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            except Exception as e:

                st.error(
                    "❌ Could not analyze the image."
                )

                st.info(
                    "Make sure Ollama is installed and "
                    "the llava model is downloaded."
                )

                st.code(str(e))


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI Social Media Caption Generator | "
    "Python + Streamlit + Ollama + Llama 3.2 + LLaVA"
)

