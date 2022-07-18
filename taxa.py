
def is_non_finnish(taxon):

    # Note that these are used as partial match -> don't add very short names
    # Don't add too many taxa here, only those that are consistently identified given for a common Finnish species. Adding too many names here will hide valid observations of interesting taxa, like Formicarius rufipectus that was Numenius arquata.
    non_finnish_taxa = [
        "Engine",
        "Siren",
        "Canis lupus",
        "Pipilo ",
        "Vireo ",
        "Cardinalis ",
        "Myadestes ",
        "Poecile ",
        "Tympanuchus ",
        "Sialia ",
        "Brachyramphus ",
        "Baeolophus ",
        "Haemorhous ",
        "Piranga ",
        "Myiarchus ",
        "Brotogeris ",
        "Dryobates ",
        "Setophaga ",
        "Dendrocygna ",
        "Hylocichla mustelina",
        "Turdus migratorius",
        "Setophaga ",
        "Cyanocitta cristata",
        
        "LAST ITEM WITHOUT COMMA"
        ]

    for non_finnish in non_finnish_taxa:
        if non_finnish in taxon:
            return True

    return False
