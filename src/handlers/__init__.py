from aiogram import Router


def setup_routers() -> Router:
    from src.handlers import create_pairs_command, poll_answer_handler, send_poll_command

    router = Router()
    router.include_router(create_pairs_command.router)
    router.include_router(poll_answer_handler.router)
    router.include_router(send_poll_command.router)
    return router