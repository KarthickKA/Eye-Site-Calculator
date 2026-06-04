import numpy as np
from PIL import Image, ImageDraw
import streamlit as st


class ColorBlindnessTest:
    """Ishihara color blindness test."""

    def __init__(self):
        self.plates = [
            {'name': 'Plate 1 (Control)', 'answer': '12', 'description': 'Everyone should see 12'},
            {'name': 'Plate 2', 'answer': '8', 'description': 'Normal: 8, Red-blind: 3, Green-blind: 5'},
            {'name': 'Plate 3', 'answer': '29', 'description': 'Normal: 29, Red-blind: 70, Green-blind: 70'},
            {'name': 'Plate 4', 'answer': '5', 'description': 'Normal: 5, Red-blind: 2, Green-blind: 2'},
            {'name': 'Plate 5', 'answer': '3', 'description': 'Normal: 3, Red-blind: 5, Green-blind: 5'},
            {'name': 'Plate 6', 'answer': '15', 'description': 'Normal: 15, Blue-blind: cannot see'},
        ]

    def create_ishihara_plate(self, plate_index):
        """Create a synthetic Ishihara-style color blindness test plate."""
        img = Image.new('RGB', (600, 600), color=(200, 200, 200))
        draw = ImageDraw.Draw(img, 'RGBA')

        if plate_index == 0:
            colors_normal = [(255, 0, 0), (0, 180, 0)]
            self._draw_number(draw, '12', colors_normal)

        elif plate_index == 1:
            colors_normal = [(255, 0, 0), (255, 100, 0), (0, 150, 0)]
            self._draw_number(draw, '8', colors_normal)

        elif plate_index == 2:
            colors_normal = [(255, 0, 0), (255, 100, 0), (0, 150, 0)]
            self._draw_number(draw, '29', colors_normal)

        elif plate_index == 3:
            colors_normal = [(255, 0, 0), (255, 100, 0), (100, 100, 0)]
            self._draw_number(draw, '5', colors_normal)

        elif plate_index == 4:
            colors_normal = [(255, 0, 0), (255, 100, 0), (100, 100, 0)]
            self._draw_number(draw, '3', colors_normal)

        elif plate_index == 5:
            colors_blue = [(0, 0, 255), (0, 100, 200), (100, 100, 150)]
            self._draw_number(draw, '15', colors_blue)

        return np.array(img)

    def _draw_number(self, draw, number, colors):
        """Draw a number on the plate using colored circles."""
        x_start = 150
        y_start = 200

        for i, digit in enumerate(number):
            x_offset = i * 150
            x = x_start + x_offset
            y = y_start

            if digit == '1':
                self._draw_digit_1(draw, x, y, colors)
            elif digit == '2':
                self._draw_digit_2(draw, x, y, colors)
            elif digit == '3':
                self._draw_digit_3(draw, x, y, colors)
            elif digit == '5':
                self._draw_digit_5(draw, x, y, colors)
            elif digit == '8':
                self._draw_digit_8(draw, x, y, colors)
            elif digit == '9':
                self._draw_digit_9(draw, x, y, colors)

    def _draw_digit_1(self, draw, x, y, colors):
        """Draw digit 1 using circles."""
        for i in range(5):
            draw.ellipse(
                [x + 20, y + i * 30, x + 50, y + 30 + i * 30],
                fill=colors[i % len(colors)]
            )

    def _draw_digit_2(self, draw, x, y, colors):
        """Draw digit 2 using circles."""
        positions = [
            (x, y), (x + 30, y), (x + 60, y),
            (x + 60, y + 30), (x + 30, y + 30),
            (x, y + 30), (x, y + 60), (x + 30, y + 60), (x + 60, y + 60)
        ]
        for i, (px, py) in enumerate(positions):
            draw.ellipse(
                [px, py, px + 20, py + 20],
                fill=colors[i % len(colors)]
            )

    def _draw_digit_3(self, draw, x, y, colors):
        """Draw digit 3 using circles."""
        positions = [
            (x, y), (x + 30, y), (x + 60, y),
            (x + 60, y + 30), (x + 30, y + 30),
            (x + 60, y + 60), (x + 30, y + 60), (x, y + 60)
        ]
        for i, (px, py) in enumerate(positions):
            draw.ellipse(
                [px, py, px + 20, py + 20],
                fill=colors[i % len(colors)]
            )

    def _draw_digit_5(self, draw, x, y, colors):
        """Draw digit 5 using circles."""
        positions = [
            (x, y), (x + 30, y), (x + 60, y),
            (x, y + 30), (x + 30, y + 30),
            (x + 60, y + 60), (x + 30, y + 60), (x, y + 60)
        ]
        for i, (px, py) in enumerate(positions):
            draw.ellipse(
                [px, py, px + 20, py + 20],
                fill=colors[i % len(colors)]
            )

    def _draw_digit_8(self, draw, x, y, colors):
        """Draw digit 8 using circles."""
        for row in range(3):
            for col in range(3):
                px = x + col * 25
                py = y + row * 25
                draw.ellipse(
                    [px, py, px + 20, py + 20],
                    fill=colors[(row + col) % len(colors)]
                )

    def _draw_digit_9(self, draw, x, y, colors):
        """Draw digit 9 using circles."""
        positions = [
            (x, y), (x + 30, y), (x + 60, y),
            (x, y + 30), (x + 30, y + 30), (x + 60, y + 30),
            (x + 60, y + 60), (x + 30, y + 60)
        ]
        for i, (px, py) in enumerate(positions):
            draw.ellipse(
                [px, py, px + 20, py + 20],
                fill=colors[i % len(colors)]
            )

    def run_test(self):
        """Run interactive color blindness test."""
        st.write("### Color Blindness Test (Ishihara Plates)")
        st.write("Look at each plate and enter what number you see.")

        if 'cb_current_plate' not in st.session_state:
            st.session_state.cb_current_plate = 0
            st.session_state.cb_answers = []

        if st.session_state.cb_current_plate < len(self.plates):
            plate_info = self.plates[st.session_state.cb_current_plate]
            plate_img = self.create_ishihara_plate(st.session_state.cb_current_plate)

            st.write(f"#### {plate_info['name']}")
            st.image(plate_img, use_column_width=True)

            user_answer = st.text_input(
                "What number do you see?",
                key=f"plate_{st.session_state.cb_current_plate}"
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Next Plate"):
                    if user_answer:
                        st.session_state.cb_answers.append({
                            'plate': st.session_state.cb_current_plate,
                            'correct': plate_info['answer'],
                            'user_answer': user_answer
                        })
                        st.session_state.cb_current_plate += 1
                        st.rerun()

            with col2:
                if st.button("Skip"):
                    st.session_state.cb_answers.append({
                        'plate': st.session_state.cb_current_plate,
                        'correct': plate_info['answer'],
                        'user_answer': 'skipped'
                    })
                    st.session_state.cb_current_plate += 1
                    st.rerun()

        else:
            st.write("## Test Results")
            correct_count = sum(
                1 for ans in st.session_state.cb_answers
                if ans['user_answer'] == ans['correct']
            )
            total = len(st.session_state.cb_answers)

            color_vision = self._determine_color_vision(st.session_state.cb_answers)

            st.metric("Score", f"{correct_count}/{total}", delta=None)
            st.info(f"**Color Vision Type:** {color_vision}")

            if st.button("Restart Test"):
                st.session_state.cb_current_plate = 0
                st.session_state.cb_answers = []
                st.rerun()

            return {'color_vision_type': color_vision, 'score': f"{correct_count}/{total}"}

    def _determine_color_vision(self, answers):
        """Determine color vision type from answers."""
        if not answers:
            return "Incomplete test"

        correct = sum(1 for a in answers if a['user_answer'] == a['correct'])
        total = len(answers)

        if correct == total:
            return "Normal Color Vision (Trichromat)"
        elif correct >= total * 0.7:
            return "Mild Color Vision Deficiency"
        else:
            return "Significant Color Vision Deficiency (Red-Green or Blue-Yellow)"
