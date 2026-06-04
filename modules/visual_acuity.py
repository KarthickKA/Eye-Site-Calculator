import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import streamlit as st


class VisualAcuityTest:
    """Snellen chart visual acuity test."""

    def __init__(self):
        self.snellen_lines = [
            ('20/200', 200, 'E'),
            ('20/100', 100, 'F P T O Z'),
            ('20/70', 70, 'D E F C Z D E F C Z'),
            ('20/50', 50, 'D E F P T O Z C D E F'),
            ('20/40', 40, 'E D F C Z P T O D E F C Z D E F P'),
            ('20/30', 30, 'D E F C P T O Z D E F C Z D E F P T O'),
            ('20/20', 20, 'F D E C Z P T O D E F C Z D E F P T O Z'),
        ]

    def create_snellen_chart(self, line_index):
        """Create a Snellen chart image for a specific line."""
        acuity, font_size, letters = self.snellen_lines[line_index]

        img = Image.new('RGB', (800, 600), color='white')
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.load_default()
        except Exception:
            font = ImageFont.load_default()

        y_position = 250
        text_display = letters
        bbox = draw.textbbox((0, 0), text_display, font=font)
        text_width = bbox[2] - bbox[0]
        x_position = (800 - text_width) // 2

        draw.text((x_position, y_position), text_display, fill='black', font=font)

        draw.text((50, 50), f"Visual Acuity: {acuity}", fill='gray', font=font)
        draw.text(
            (50, 550),
            "Can you clearly read the letters above?",
            fill='gray',
            font=font
        )

        return np.array(img)

    def run_test(self):
        """Run interactive Snellen chart test."""
        st.write("### Visual Acuity Test (Snellen Chart)")
        st.write("You will be shown lines with decreasing letter sizes.")
        st.write("Tell us the last line you can clearly read.")

        if 'acuity_line' not in st.session_state:
            st.session_state.acuity_line = 0
        if 'test_complete' not in st.session_state:
            st.session_state.test_complete = False

        if st.session_state.test_complete:
            result = self.snellen_lines[st.session_state.acuity_line][0]
            st.success(f"Your visual acuity: **{result}**")
            if st.button("Restart Test"):
                st.session_state.acuity_line = 0
                st.session_state.test_complete = False
                st.rerun()
        else:
            if st.session_state.acuity_line < len(self.snellen_lines):
                chart = self.create_snellen_chart(st.session_state.acuity_line)
                st.image(chart, use_column_width=True)

                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button("I can read this"):
                        if st.session_state.acuity_line < len(self.snellen_lines) - 1:
                            st.session_state.acuity_line += 1
                            st.rerun()
                        else:
                            st.session_state.test_complete = True
                            st.rerun()

                with col2:
                    if st.button("Too small"):
                        st.session_state.test_complete = True
                        st.rerun()

                with col3:
                    if st.button("Reset"):
                        st.session_state.acuity_line = 0
                        st.rerun()

        return {
            'acuity_score': self.snellen_lines[st.session_state.acuity_line][0]
            if st.session_state.test_complete else 'Not completed'
        }
