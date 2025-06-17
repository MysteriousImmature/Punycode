#!/usr/bin/env python3
"""
Punycode Email Variations Generator

This script generates various punycode variations of an email address
by substituting characters with visually similar Unicode characters.
"""

def generate_punycode_variations(email):
    """
    Generate punycode variations of an email address
    """
    # Split email into username and domain
    username, domain = email.split('@')
    
    # Character substitution mappings for homograph attacks
    # These are visually similar characters from different Unicode blocks
    char_substitutions = {
        'a': ['а', 'à', 'á', 'â', 'ã', 'ä', 'å', 'ā', 'ă', 'ą'],  # Cyrillic а, Latin variants
        'e': ['е', 'è', 'é', 'ê', 'ë', 'ē', 'ĕ', 'ė', 'ę', 'ě'],  # Cyrillic е, Latin variants
        'i': ['і', 'ì', 'í', 'î', 'ï', 'ī', 'ĭ', 'į', 'ı'],        # Cyrillic і, Latin variants
        'o': ['о', 'ò', 'ó', 'ô', 'õ', 'ö', 'ø', 'ō', 'ŏ', 'ő'],  # Cyrillic о, Latin variants
        'u': ['υ', 'ù', 'ú', 'û', 'ü', 'ū', 'ŭ', 'ů', 'ű', 'ų'],  # Greek υ, Latin variants
        'p': ['р', 'þ'],                                            # Cyrillic р
        'c': ['с', 'ç', 'ć', 'ĉ', 'ċ', 'č'],                      # Cyrillic с, Latin variants
        'g': ['ɡ', 'ğ', 'ĝ', 'ġ', 'ģ'],                          # Latin variants
        'm': ['м', 'ɱ'],                                            # Cyrillic м
        'n': ['ո', 'ñ', 'ń', 'ň', 'ņ'],                           # Armenian ո, Latin variants
        'l': ['ӏ', 'ł', 'ĺ', 'ļ', 'ľ', 'ŀ'],                     # Cyrillic ӏ, Latin variants
        's': ['ѕ', 'ś', 'ŝ', 'ş', 'š'],                           # Cyrillic ѕ, Latin variants
        't': ['т', 'ţ', 'ť', 'ŧ'],                                 # Cyrillic т, Latin variants
        'r': ['г', 'ŕ', 'ŗ', 'ř'],                                 # Cyrillic г, Latin variants
        'h': ['һ', 'ĥ', 'ħ'],                                      # Cyrillic һ, Latin variants
        'x': ['х', 'χ'],                                            # Cyrillic х, Greek χ
        'y': ['у', 'ý', 'ÿ', 'ŷ'],                                 # Cyrillic у, Latin variants
    }
    
    variations = []
    
    # Generate variations for different parts of the domain
    domain_parts = domain.split('.')
    
    # Function to generate character variations for a string
    def generate_string_variations(text, max_variations=10):
        string_variations = [text]  # Include original
        
        for char, substitutes in char_substitutions.items():
            if char in text.lower():
                for substitute in substitutes[:3]:  # Limit substitutes to avoid too many variations
                    new_text = text.lower().replace(char, substitute)
                    if new_text != text.lower() and new_text not in string_variations:
                        string_variations.append(new_text)
                        if len(string_variations) >= max_variations:
                            break
                if len(string_variations) >= max_variations:
                    break
        
        return string_variations[:max_variations]
    
    # Generate variations for the main domain part (gmail)
    main_domain = domain_parts[0]
    domain_variations = generate_string_variations(main_domain, 15)
    
    # Generate complete email variations
    for domain_var in domain_variations:
        if domain_var != main_domain:  # Skip the original
            new_email = f"{username}@{domain_var}.{'.'.join(domain_parts[1:])}"
            variations.append(new_email)
    
    # Also generate some mixed variations (multiple character substitutions)
    mixed_variations = []
    for i, domain_var in enumerate(domain_variations[1:6]):  # Take first 5 variations
        # Apply additional substitutions
        for char, substitutes in list(char_substitutions.items())[:3]:  # Limit iterations
            if char in domain_var:
                for substitute in substitutes[:2]:
                    mixed_domain = domain_var.replace(char, substitute, 1)  # Replace only first occurrence
                    if mixed_domain != domain_var:
                        mixed_email = f"{username}@{mixed_domain}.{'.'.join(domain_parts[1:])}"
                        if mixed_email not in variations:
                            mixed_variations.append(mixed_email)
                            break
            if len(mixed_variations) >= 10:
                break
        if len(mixed_variations) >= 10:
            break
    
    variations.extend(mixed_variations)
    
    return variations

def email_to_punycode(email):
    """
    Convert email to punycode format
    """
    try:
        username, domain = email.split('@')
        domain_parts = domain.split('.')
        
        # Encode each part of the domain to punycode
        encoded_parts = []
        for part in domain_parts:
            try:
                # Only encode if it contains non-ASCII characters
                if any(ord(char) > 127 for char in part):
                    encoded_part = part.encode('idna').decode('ascii')
                    encoded_parts.append(encoded_part)
                else:
                    encoded_parts.append(part)
            except:
                encoded_parts.append(part)
        
        encoded_domain = '.'.join(encoded_parts)
        return f"{username}@{encoded_domain}"
    except Exception as e:
        return f"Error encoding {email}: {str(e)}"

def main():
    original_email = "user@gmail.com"
    print(f"Original email: {original_email}")
    print("=" * 60)
    
    # Generate variations
    variations = generate_punycode_variations(original_email)
    
    print(f"\nGenerated {len(variations)} variations:\n")
    
    punycode_results = []
    for variation in variations:
        punycode_version = email_to_punycode(variation)
        # Only show results that actually have xn-- encoding
        if 'xn--' in punycode_version:
            punycode_results.append((variation, punycode_version))
    
    if punycode_results:
        print("Variations with actual punycode encoding (xn-- format):\n")
        for i, (original, punycode) in enumerate(punycode_results[:20], 1):
            print(f"{i:2d}. Unicode: {original}")
            print(f"    Punycode: {punycode}")
            print()
    else:
        print("No variations generated actual xn-- punycode. Showing regular variations:")
        for i, variation in enumerate(variations[:15], 1):
            punycode_version = email_to_punycode(variation)
            print(f"{i:2d}. Unicode: {variation}")
            print(f"    Encoded: {punycode_version}")
            print()
    
    # Show some specific examples that will definitely create xn-- format
    print("\nSpecific examples that create xn-- punycode format:")
    print("=" * 60)
    
    specific_examples = [
        "user@gmaïl.com",      # ï will create xn-- 
        "user@gmäil.com",      # ä will create xn--
        "user@gмail.com",      # Cyrillic м will create xn--
        "user@gmaіl.com",      # Cyrillic і will create xn--
        "user@gmaiℓ.com",      # Script ℓ will create xn--
        "user@ɡmail.com",      # Latin small letter script g
        "user@gmaìl.com",      # ì will create xn--
        "user@gmàil.com",      # à will create xn--
        "user@gmaíl.com",      # í will create xn--
        "user@ğmail.com",      # ğ will create xn--
    ]
    
    for i, example in enumerate(specific_examples, 1):
        punycode = email_to_punycode(example)
        print(f"{i:2d}. Unicode: {example}")
        print(f"    Punycode: {punycode}")
        print()
    
    print("\nNote: These variations use Unicode characters that require")
    print("punycode encoding (xn--) and may appear identical to gmail.com")
    print("This demonstrates potential homograph/punycode attacks.")

if __name__ == "__main__":
    main()
