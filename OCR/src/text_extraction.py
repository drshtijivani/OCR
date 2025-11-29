import re

def extract_target_line(ocr_results):
    """
   
     Format: Returns '18Digits_1_'.
    """
    
    # 1. Regex to find the 18-digit ID 
    # Structure: 18 digits + separator (1, l, I, i, |) + optional trailing separator
    # Fixed: [_\-\s] instead of [_-\s]
    id_pattern = re.compile(r'(\d{18})([_\-\s]*[1lIi|][_\-\s]*)')
    
    # 2. Context Keywords (Triggers)
    label_regex = re.compile(r'(?:order|po|waybill|awb)\s*[\w\W]{0,5}\s*id|\b(?:ftpl|ftfl|rvp)\b', re.IGNORECASE)

    best_match = None
    
    # --- STRATEGY 1: CONTEXT SEARCH (High Priority) ---
    n = len(ocr_results)
    for i in range(n):
        text = ocr_results[i][1]
        
        # Check if the line contains any of our Keywords
        if label_regex.search(text):
            
            # Scan the NEXT 4 lines
            for j in range(1, 5):
                if i + j >= n: break
                
                neighbor_text = ocr_results[i+j][1]
                
                # Clean noise but keep underscores and letters
                clean_neighbor = re.sub(r'[^\w_\|\-]', '', neighbor_text)
                
                # Check A: Perfect Match
                match = id_pattern.search(clean_neighbor)
                if match:
                    # Found match! Return only ID + _1_ (discard suffix)
                    return f"{match.group(1)}_1_", 1.0

                # Check B: Digits Only (Reconstruct)
                clean_digits = re.sub(r'\D', '', neighbor_text)
                if len(clean_digits) == 18:
                    
                    # Look for suffix start in the very next line
                    if i + j + 1 < n:
                        next_line = ocr_results[i+j+1][1]
                        clean_next = re.sub(r'[^\w_\|\-]', '', next_line)
                        
                        # If next line looks like the continuation
                        # FIXED: Escaped hyphen here: [_\-\s]
                        if re.match(r'^[_\-\s]*[1lIi|]', clean_next) or re.match(r'^\w+$', clean_next):
                             # Return just the ID part with the standard suffix start
                             return f"{clean_digits}_1_", 0.9
                    
                    # Default assumption if we found 18 digits under a keyword
                    return f"{clean_digits}_1_", 0.8

    # --- STRATEGY 2: GLOBAL SCAN (Fallback) ---
    for item in ocr_results:
        text = item[1]
        # Clean noise
        clean_text = re.sub(r'[^\w_\|\-]', '', text)
        
        match = id_pattern.search(clean_text)
        if match:
            # Return truncated version
            return f"{match.group(1)}_1_", item[2]

    return None, 0.0