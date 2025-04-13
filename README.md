## Setup Instructions for cmsSzt Project

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/xFELAx/cmsSzt.git
    ```

2.  **Navigate into the project directory:**
    ```bash
    cd cmsSzt
    ```

3.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

4.  **Activate the virtual environment:**
    *   **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    ![Virtual environment activation on Windows](https://github.com/user-attachments/assets/7339d994-9d91-4a85-8057-88fd9ae31932)

5.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

6.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

7.  **Create a superuser (administrator account):**
    ```bash
    python manage.py createsuperuser
    ```
    *(Follow the prompts to set a username, email, and password)*

8.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

## Accessing the Application

*   **Main Website:** [http://localhost:8000/](http://localhost:8000/)
*   **Administrator Panel:** [http://localhost:8000/dashboard/](http://localhost:8000/dashboard/)
