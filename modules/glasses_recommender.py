class GlassesRecommender:
    """Recommend glasses frames based on face shape."""

    RECOMMENDATIONS = {
        'oval': {
            'frames': ['Cat-Eye', 'Rectangular', 'Round', 'Clubmaster'],
            'reason': 'Oval faces are balanced and can wear almost any frame style. These styles complement your proportions.'
        },
        'round': {
            'frames': ['Rectangular', 'Square', 'Geometric', 'Wayfarer'],
            'reason': 'Rectangular frames add definition and balance round features. Angular styles elongate your face.'
        },
        'square': {
            'frames': ['Round', 'Oval', 'Clubmaster', 'Cat-Eye'],
            'reason': 'Softer, curved frames balance strong angular features. These styles complement your defined jawline.'
        },
        'heart': {
            'frames': ['Bottom-Heavy', 'Round', 'Oval', 'Aviator'],
            'reason': 'Bottom-heavy frames balance a wider forehead. Curved styles bring proportion to your face shape.'
        },
        'oblong': {
            'frames': ['Wayfarer', 'Clubmaster', 'Browline', 'Round'],
            'reason': 'Horizontal or oversized frames add width and balance your elongated features.'
        },
        'unknown': {
            'frames': ['Oval', 'Round', 'Rectangular', 'Cat-Eye'],
            'reason': 'Classic frames that work with most face shapes.'
        }
    }

    def recommend(self, face_shape: str) -> dict:
        """
        Get glasses recommendations for a face shape.

        Args:
            face_shape: str (oval, round, square, heart, oblong, unknown)

        Returns:
            dict: {
                'recommendations': list of frame styles,
                'reason': explanation,
                'descriptions': dict with details for each frame style
            }
        """
        shape_key = face_shape.lower()
        if shape_key not in self.RECOMMENDATIONS:
            shape_key = 'unknown'

        rec = self.RECOMMENDATIONS[shape_key]

        descriptions = self._get_frame_descriptions()

        return {
            'recommendations': rec['frames'],
            'reason': rec['reason'],
            'descriptions': {frame: descriptions.get(frame, 'Classic frame style')
                           for frame in rec['frames']}
        }

    def _get_frame_descriptions(self):
        """Get detailed descriptions for each frame type."""
        return {
            'Cat-Eye': 'Retro style with upswept outer corners. Creates a lift and draws attention upward.',
            'Rectangular': 'Clean, geometric shape. Adds structure and definition to softer faces.',
            'Round': 'Circular lenses. Softens angular features and adds a vintage touch.',
            'Clubmaster': 'Bold browline with smaller round bottom. Balanced classic style.',
            'Square': 'Sharp geometric shape. Adds definition and modern appeal.',
            'Geometric': 'Unique angular shapes. Makes a bold style statement.',
            'Wayfarer': 'Trapezoidal shape. Timeless style that works with many face shapes.',
            'Oval': 'Curved, symmetrical shape. Universally flattering and versatile.',
            'Bottom-Heavy': 'Wider at the bottom. Balances wider foreheads.',
            'Browline': 'Prominent top with curved brow. Emphasizes the upper face.',
            'Aviator': 'Teardrop shape. Classic and sophisticated.'
        }
