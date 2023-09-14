cd() {
    # Change to the requested directory
    builtin cd "$@"

    # Check if a virtual environment exists in the current directory
    if [ -f .venv/bin/activate ]; then
        # Activate the virtual environment
        source .venv/bin/activate

        # Display a welcome message
        echo "Welcome to Hands-on GCP for Closer Academy"
        echo "Virtual environment 'venv' is activated."
    else
        # If no virtual environment is found, just display the welcome message
        echo "Welcome to Hands-on GCP for Closer Academy"
    fi
}