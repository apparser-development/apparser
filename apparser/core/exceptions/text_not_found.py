class TextNotFoundException(Exception):
    def __init__(self, min_similarity: float):
        if not isinstance(min_similarity, float):
            raise TypeError("min_similarity must be float")

        if min_similarity < 0 or min_similarity > 1:
            raise ValueError("min_similarity must be between 0 and 1")

        super().__init__(f"No text with similarity greater than or equal to {min_similarity} was found.")