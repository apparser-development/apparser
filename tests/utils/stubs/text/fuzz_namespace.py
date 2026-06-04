class FuzzNamespace:
    @staticmethod
    def token_sort_ratio(first: str, second: str) -> int:
        return 100 if first == second else 0
