import pytesseract
from PIL import Image
import re
from io import BytesIO

class PassportOCRService:
    """Passport OCR and MRZ extraction"""
    
    # Tesseract path (Windows)
    TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    def __init__(self):
        pytesseract.pytesseract.pytesseract_cmd = self.TESSERACT_PATH
    
    def extract_from_image(self, image_path):
        """Extract passport data from image"""
        try:
            image = Image.open(image_path)
            
            # Preprocess image
            image = self._preprocess_image(image)
            
            # Extract text
            raw_text = pytesseract.image_to_string(image, lang='eng')
            
            # Extract MRZ (Machine Readable Zone)
            mrz_data = self._extract_mrz(raw_text)
            
            # Parse MRZ
            parsed_data = self._parse_mrz(mrz_data) if mrz_data else {}
            
            # Extract OCR data
            ocr_data = self._extract_ocr_fields(raw_text)
            
            # Merge results
            result = {**ocr_data, **parsed_data}
            result['mrz_data'] = mrz_data
            result['raw_text'] = raw_text
            
            return result
            
        except Exception as e:
            return {'error': str(e)}
    
    def _preprocess_image(self, image):
        """Preprocess image for better OCR"""
        from PIL import ImageEnhance
        
        # Convert to grayscale
        if image.mode != 'L':
            image = image.convert('L')
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(2)
        
        return image
    
    def _extract_mrz(self, text):
        """Extract Machine Readable Zone from text"""
        lines = text.split('\n')
        mrz_lines = []
        
        for line in lines:
            # MRZ lines are typically 44 characters and contain specific format
            if len(line.strip()) >= 44:
                # Check if line contains MRZ pattern
                if re.search(r'^[A-Z0-9<]{44}', line.strip()):
                    mrz_lines.append(line.strip())
        
        return '\n'.join(mrz_lines) if mrz_lines else None
    
    def _parse_mrz(self, mrz_data):
        """Parse MRZ to extract structured data"""
        result = {
            'mrz_valid': False,
        }
        
        if not mrz_data:
            return result
        
        try:
            lines = mrz_data.strip().split('\n')
            
            if len(lines) >= 2:
                line1 = lines[0]
                line2 = lines[1]
                
                # Extract from MRZ
                # Format: P<CTRYNAME<<SURNAME<<<<<<<<GIVENNAME
                # Line 2: PASSPORTNUMBER NATIONALITY DOB SEX EXPIRY ...
                
                # Passport number (line2, positions 0-8)
                passport_number = line2[0:9].replace('<', '').strip()
                
                # Nationality (line2, positions 10-12)
                nationality = line2[10:13].replace('<', '').strip()
                
                # Date of birth (line2, positions 13-18) - YYMMDD
                dob_str = line2[13:19]
                if dob_str and dob_str != '<<<<<<':
                    try:
                        from datetime import datetime
                        year = 1900 + int(dob_str[0:2]) if int(dob_str[0:2]) > 50 else 2000 + int(dob_str[0:2])
                        date_of_birth = f"{year}-{dob_str[2:4]}-{dob_str[4:6]}"
                    except:
                        date_of_birth = None
                else:
                    date_of_birth = None
                
                # Gender (line2, position 20)
                gender = 'M' if line2[20] == 'M' else 'F' if line2[20] == 'F' else None
                
                # Expiry date (line2, positions 21-26) - YYMMDD
                exp_str = line2[21:27]
                if exp_str and exp_str != '<<<<<<':
                    try:
                        year = 1900 + int(exp_str[0:2]) if int(exp_str[0:2]) > 50 else 2000 + int(exp_str[0:2])
                        expiry_date = f"{year}-{exp_str[2:4]}-{exp_str[4:6]}"
                    except:
                        expiry_date = None
                else:
                    expiry_date = None
                
                # Extract name from line 1
                name_part = line1[5:].replace('<', ' ').strip()
                parts = name_part.split()
                
                result = {
                    'mrz_valid': True,
                    'passport_number': passport_number if passport_number else None,
                    'passport_number_confidence': 0.95 if passport_number else 0,
                    'nationality': nationality if nationality else None,
                    'date_of_birth': date_of_birth,
                    'date_of_birth_confidence': 0.9 if date_of_birth else 0,
                    'gender': gender,
                    'expiry_date': expiry_date,
                    'expiry_date_confidence': 0.9 if expiry_date else 0,
                    'surname': parts[0] if len(parts) > 0 else None,
                    'given_name': ' '.join(parts[1:]) if len(parts) > 1 else None,
                }
        
        except Exception as e:
            result['mrz_valid'] = False
        
        return result
    
    def _extract_ocr_fields(self, text):
        """Extract fields from OCR text"""
        result = {}
        
        # Look for passport number patterns
        passport_match = re.search(r'(?:Passport\s*(?:No|Number)?[\s:]*)?([A-Z]{1,2}\d{6,9})', text, re.IGNORECASE)
        if passport_match:
            result['passport_number'] = passport_match.group(1)
            result['passport_number_confidence'] = 0.7
        
        # Look for dates (DD/MM/YYYY or similar)
        date_pattern = r'(\d{1,2}[/-]\d{1,2}[/-]\d{4})'
        dates = re.findall(date_pattern, text)
        
        return result
    
    def detect_duplicates(self, passport_number, candidate_id=None):
        """Check for duplicate passports"""
        from smart_career.apps.candidates.models import Candidate
        
        duplicates = Candidate.objects.filter(
            passport_number=passport_number
        ).exclude(id=candidate_id)
        
        return duplicates.exists(), duplicates