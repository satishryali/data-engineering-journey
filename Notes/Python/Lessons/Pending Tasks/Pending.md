# Pending Tasks
- Centrailized logging for all of my files.
    - using function :

        ```python
        # C:\GIT\TESTING\logger_config.py
        import logging
        from pathlib import Path

        # This always points to C:\GIT\TESTING\app.log, no matter where it is called from
        LOG_FILE = Path(__file__).resolve().parent / "app.log"

        def get_logger(name):
            logging.basicConfig(
                filename=LOG_FILE,
                filemode='a',   # 'a' appends so nothing gets erased
                level=logging.INFO,
                format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
            )
            return logging.getLogger(name)
        ```

    - using normal way :
        ```python
        logging.basicConfig(
            filename=LOG_FILE,
            filemode='a',   # 'a' appends so nothing gets erased
            level=logging.INFO,
            format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
        )
        ```
