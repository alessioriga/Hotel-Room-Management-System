from functools import wraps
from flask import session, redirect, url_for


def login_required(f: object) -> object:
    """
    Decorator used to protect routes that require authentication.

    It checks if a user is logged in by verifying that the 'username'
    exists in the Flask session. If the user is not logged in,
    they are redirected to the login page.

    Args:
        f (object): The Flask view function being decorated.

    Returns:
        object: The wrapped function that first checks if the user
        is authenticated before executing the original function.
    """
    @wraps(f)
    def decorated(*args: object, **kwargs: object) -> object:
        """
        Wrapper function that performs the session authentication check
        before calling the original view function.

        Args:
            *args (object): Positional arguments passed to the view.
            **kwargs (object): Keyword arguments passed to the view.

        Returns:
            object: The response returned by the original view function
            or a redirect to the login page if the user is not authenticated.
        """
        if 'username' not in session:
            return redirect(url_for('login_bp.login'))
        
        return f(*args, **kwargs)
    
    return decorated