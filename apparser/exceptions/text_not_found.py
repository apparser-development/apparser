class TextNotFoundException(Exception):
    """Represent a failure to find text with the required similarity."""

    def __init__(self, min_similarity: float):
        """Initialize a text lookup exception.

        :param min_similarity: Minimum accepted similarity value.
        :type min_similarity: float | int
        :raises TypeError: If ``min_similarity`` has an invalid type.
        :raises ValueError: If ``min_similarity`` is outside the inclusive range from 0 to 1.
        """
        if not isinstance(min_similarity, (float, int)):
            raise TypeError("min_similarity must be a number")

        if min_similarity < 0 or min_similarity > 1:
            raise ValueError("min_similarity must be between 0 and 1")

        super().__init__(f"No text with similarity greater than or equal to {min_similarity} was found.")
