import uvicorn
from config import Config, get_config

CONFIG: Config = get_config()

uvicorn.run(
    app="main:app",
    host=CONFIG.service_host,
    port=CONFIG.service_port,
    log_level=CONFIG.log_level,
    log_config="/home/user/log.ini",
)
