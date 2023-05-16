import dotenv
from os import getenv

from src.utils.logger import get_logger
from src.utils.prepare_project import prepare_project_dir



dotenv.load_dotenv()
assert getenv("OPENAI_API_KEY") is not None, "OPENAI_API_KEY not set in .env"



if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(
        description="Launch block queue with authentication and server details")

    parser.add_argument("--username", dest="username",
                        default="admin", help="Authentication username")
    parser.add_argument("--password", dest="password",
                        default="1234@abcezIJK1", help="Authentication password")
    parser.add_argument("--concurrency", dest="concurrency", default=1,
                        type=int, help="Number of concurrent blocks to process")
    parser.add_argument("--debug", dest="debug",
                        action="store_true", help="Enable debug mode")
    parser.add_argument("--port", dest="port", default=8000,
                        type=int, help="Server port")
    parser.add_argument("--show-api", dest="show_api",
                        action="store_true", help="Show API details")

    args = parser.parse_args()

    # Usage:
    # python script.py --username admin --password 1234@abcezIJK1 --concurrency 10 --debug --port 8000 --show-api
    # or
    # python script.py -u admin -p 1234@abcezIJK1 -c 10 -d -o 8000 -s

    n_concurrency = args.concurrency
    username = args.username
    password = args.password
    debug = args.debug
    server_port = args.port
    is_show_api = args.show_api


    logger = get_logger()
    prepare_project_dir(logger=logger)

    logger.info(f"Starting server with config: {args}")

    from src.webui.web import web
    app = web()
    app.queue(concurrency_count=n_concurrency).launch(
        auth=(username, password),
        debug=debug,
        server_port=server_port,
        show_api=is_show_api
    )