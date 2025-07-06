

def encrypt_response_view(view_func):
    setattr(view_func, 'encrypt_response', True)
    return view_func
