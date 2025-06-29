CAT_ART = {
    "common": r"""
 /\_/\  
( o.o ) 
 > ^ <
    """,
    "rare": r"""
  /\_/\  
 ( ^.^ ) 
 /  \  \
    """,
    "legendary": r"""
  /\_/\  
 ( ◕ᴗ◕ ) 
 /[] []\
    """
}

def draw_cat(name, rarity):
    print(CAT_ART[rarity])
    print(f"К вам пришел {rarity} кот {name}!")