from typing import Dict, Any, Optional
import xml.etree.ElementTree as ET
from datetime import datetime
import uuid

class LegalProcessor:
    def __init__(self):
        self.namespaces = {
            'akn': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0',
            'ukl': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0/ukl'
        }
        
    def create_akoma_ntoso(self, document_data: Dict[str, Any]) -> str:
        """
        Create an Akoma Ntoso XML document from processed document data.
        
        Args:
            document_data (Dict[str, Any]): Processed document data
            
        Returns:
            str: Akoma Ntoso XML string
        """
        # Create root element
        root = ET.Element('akn:akomaNtoso', self.namespaces)
        
        # Add document metadata
        meta = self._create_metadata(document_data)
        root.append(meta)
        
        # Add document body
        body = self._create_body(document_data)
        root.append(body)
        
        # Convert to string with proper formatting
        return ET.tostring(root, encoding='unicode', method='xml')
    
    def _create_metadata(self, data: Dict[str, Any]) -> ET.Element:
        """Create metadata section of the document."""
        meta = ET.Element('akn:meta')
        
        # Add identification
        identification = ET.SubElement(meta, 'akn:identification')
        FRBRWork = ET.SubElement(identification, 'akn:FRBRWork')
        
        # Add FRBRWork elements
        ET.SubElement(FRBRWork, 'akn:FRBRthis').text = f"#{uuid.uuid4()}"
        ET.SubElement(FRBRWork, 'akn:FRBRuri').text = data.get('file_info', {}).get('path', '')
        ET.SubElement(FRBRWork, 'akn:FRBRdate').text = datetime.now().isoformat()
        
        # Add classification
        classification = ET.SubElement(meta, 'akn:classification')
        for category, confidence in data.get('classification', {}).get('all_categories', {}).items():
            cat = ET.SubElement(classification, 'akn:keyword')
            cat.text = category
            cat.set('confidence', str(confidence))
        
        return meta
    
    def _create_body(self, data: Dict[str, Any]) -> ET.Element:
        """Create main body section of the document."""
        body = ET.Element('akn:mainBody')
        
        # Add main content
        main_content = ET.SubElement(body, 'akn:mainContent')
        
        # Process content into sections
        content = data.get('content', '')
        sections = self._split_into_sections(content)
        
        for section in sections:
            section_elem = ET.SubElement(main_content, 'akn:section')
            section_elem.text = section
        
        return body
    
    def _split_into_sections(self, content: str) -> list:
        """Split content into logical sections."""
        # Simple section splitting based on newlines and common section markers
        sections = []
        current_section = []
        
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                if current_section:
                    sections.append('\n'.join(current_section))
                    current_section = []
            else:
                current_section.append(line)
        
        if current_section:
            sections.append('\n'.join(current_section))
        
        return sections
    
    def extract_legal_metadata(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract legal-specific metadata from document data.
        
        Args:
            document_data (Dict[str, Any]): Processed document data
            
        Returns:
            Dict[str, Any]: Legal metadata
        """
        legal_metadata = {
            'document_type': self._determine_legal_document_type(document_data),
            'jurisdiction': self._extract_jurisdiction(document_data),
            'date': self._extract_date(document_data),
            'parties': self._extract_parties(document_data),
            'references': self._extract_references(document_data)
        }
        
        return legal_metadata
    
    def _determine_legal_document_type(self, data: Dict[str, Any]) -> str:
        """Determine the type of legal document."""
        # Use classification results to determine document type
        classification = data.get('classification', {})
        if classification.get('primary_category') == 'legal':
            # Look for specific legal document indicators
            content = data.get('content', '').lower()
            if 'contract' in content:
                return 'contract'
            elif 'agreement' in content:
                return 'agreement'
            elif 'act' in content or 'statute' in content:
                return 'legislation'
            elif 'judgment' in content or 'ruling' in content:
                return 'judicial_decision'
        return 'unknown'
    
    def _extract_jurisdiction(self, data: Dict[str, Any]) -> Optional[str]:
        """Extract jurisdiction information."""
        # Look for jurisdiction in entities
        entities = data.get('metadata', {}).get('entities', {})
        locations = entities.get('locations', [])
        
        # Common jurisdiction indicators
        jurisdiction_indicators = ['jurisdiction', 'governed by', 'laws of']
        content = data.get('content', '').lower()
        
        for indicator in jurisdiction_indicators:
            if indicator in content:
                # Extract the jurisdiction text
                start_idx = content.find(indicator)
                end_idx = content.find('\n', start_idx)
                if end_idx == -1:
                    end_idx = len(content)
                jurisdiction = content[start_idx:end_idx].strip()
                return jurisdiction
        
        return locations[0] if locations else None
    
    def _extract_date(self, data: Dict[str, Any]) -> Optional[str]:
        """Extract document date."""
        dates = data.get('metadata', {}).get('entities', {}).get('dates', [])
        return dates[0] if dates else None
    
    def _extract_parties(self, data: Dict[str, Any]) -> list:
        """Extract parties involved in the document."""
        return data.get('metadata', {}).get('entities', {}).get('persons', [])
    
    def _extract_references(self, data: Dict[str, Any]) -> list:
        """Extract legal references."""
        # Look for common legal reference patterns
        content = data.get('content', '')
        references = []
        
        # Common reference patterns
        patterns = [
            r'\b\d+\s+U\.S\.C\.\s+\d+\b',  # US Code references
            r'\b\d+\s+Stat\.\s+\d+\b',      # Statute references
            r'\b\d+\s+F\.\s+\d+\b',         # Federal references
            r'\b\d+\s+U\.K\.\s+\d+\b',      # UK references
        ]
        
        import re
        for pattern in patterns:
            matches = re.findall(pattern, content)
            references.extend(matches)
        
        return list(set(references))  # Remove duplicates 