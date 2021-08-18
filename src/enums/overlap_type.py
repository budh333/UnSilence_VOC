from enum import Enum

class OverlapType(Enum):
    BASEvsGT = 'BASE-vs-GT'
    BASEvsOCR = 'BASE-vs-OCR'
    BASEvsOG = 'BASE-vs-OG'
    GTvsOCR = 'GT-vs-RAW'

    @staticmethod
    def get_friendly_name(overlap_type) -> str:
        if overlap_type == OverlapType.BASEvsGT:
            return 'BASE vs. Ground-Truth'
        elif overlap_type == OverlapType.BASEvsOCR:
            return 'BASE vs. OCR'
        elif overlap_type == OverlapType.BASEvsOG:
            return 'BASE vs. Original (non-fine-tuned)'

        return None