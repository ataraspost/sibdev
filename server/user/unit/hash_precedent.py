

def get_hash_precedent(user):
    hash_precedent = 0
    for item in user.precedents.all():
        hash_precedent += item.updated_at.timestamp()
    return str(hash_precedent)


