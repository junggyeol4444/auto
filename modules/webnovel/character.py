"""
Character generation module
"""
import random


class CharacterGenerator:
    """Generate characters for web novels"""
    
    def __init__(self, template):
        self.template = template
        self.archetypes = template.get('character_archetypes', {})
    
    def generate_character(self, role='protagonist', custom_name=None, custom_traits=None):
        """Generate a character based on role and template"""
        if role not in self.archetypes:
            role = 'protagonist'
        
        archetype = self.archetypes[role]
        
        # Generate character details
        character = {
            'role': role,
            'name': custom_name or self._generate_name(role),
            'traits': custom_traits or random.sample(archetype.get('traits', ['평범한']), 
                                                     min(2, len(archetype.get('traits', [])))),
            'age': random.randint(18, 35) if role == 'protagonist' else random.randint(20, 50),
        }
        
        # Add role-specific attributes
        if 'backgrounds' in archetype:
            character['background'] = random.choice(archetype['backgrounds'])
        
        if 'roles' in archetype:
            character['specific_role'] = random.choice(archetype['roles'])
        
        if 'abilities' in archetype:
            character['abilities'] = random.sample(archetype['abilities'], 
                                                   min(2, len(archetype['abilities'])))
        
        # Generate description
        character['description'] = self._generate_description(character)
        
        return character
    
    def _generate_name(self, role):
        """Generate a random Korean name"""
        last_names = ['김', '이', '박', '최', '정', '강', '조', '윤', '장', '임']
        first_names_male = ['민준', '서준', '도윤', '예준', '시우', '주원', '하준', '지호', '준서', '건우']
        first_names_female = ['서연', '민서', '지우', '서현', '수아', '지민', '지아', '소율', '예은', '하은']
        
        last_name = random.choice(last_names)
        
        # Use female names for heroine, male for others
        if role == 'heroine':
            first_name = random.choice(first_names_female)
        else:
            first_name = random.choice(first_names_male)
        
        return f"{last_name}{first_name}"
    
    def _generate_description(self, character):
        """Generate character description"""
        desc_parts = []
        
        # Name and role
        name = character['name']
        desc_parts.append(f"{name}")
        
        # Age
        if 'age' in character:
            desc_parts.append(f"{character['age']}세")
        
        # Specific role
        if 'specific_role' in character:
            desc_parts.append(f"{character['specific_role']}")
        elif 'background' in character:
            desc_parts.append(f"{character['background']}")
        
        # Traits
        if character.get('traits'):
            trait_str = ', '.join(character['traits'])
            desc_parts.append(f"성격: {trait_str}")
        
        # Abilities
        if character.get('abilities'):
            ability_str = ', '.join(character['abilities'])
            desc_parts.append(f"능력: {ability_str}")
        
        return ' | '.join(desc_parts)
    
    def generate_cast(self, protagonist_name=None):
        """Generate a full cast of characters"""
        cast = {}
        
        # Generate protagonist
        cast['protagonist'] = self.generate_character('protagonist', custom_name=protagonist_name)
        
        # Generate other characters based on available archetypes
        for role in self.archetypes.keys():
            if role != 'protagonist' and role not in cast:
                try:
                    cast[role] = self.generate_character(role)
                except:
                    pass
        
        return cast
