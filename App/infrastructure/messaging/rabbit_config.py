from App.infrastructure.log.logger import logger
from App.config.rabbit import get_rabbit_settings
from faststream.rabbit import RabbitBroker
from faststream import FastStream
from typing import Optional

class RabbitMQConfig:
    def __init__(self):
        self._broker: Optional[RabbitBroker] = None
        self._router: Optional[FastStream] = None

    @property
    def broker(self) -> RabbitBroker:
        try:
            if self._broker is None:
                self.settings = get_rabbit_settings()
                self._broker = RabbitBroker(
                    url=self.settings.rabbit_url,
                )
            return self._broker
        except Exception as e:
            logger.exception(f"Error in broker initialization: {e}")
        
    @property
    def router(self) -> FastStream:
        try:
            if self._router is None:
                self._router = FastStream(
                    self.broker,
                )
            return self._router
        except Exception as e:
            logger.exception(f"Error in router initialization: {e}")
    
    async def send_message(self, message: str | dict, queue: str) -> None:
        try:
            await self.broker.publish(
                message, queue, persist=True,
            )
            logger.info(f"The message '{message}' has been successfully send to the queue '{queue}'")
        except Exception as e:
            logger.exception(f"Rabbit send-message error: {e}")
            raise
    
    async def connect(self) -> None:
        try:
            await self.broker.start()
            logger.info("RabbitMQ successfully launched!")
        except Exception as e:
            logger.exception(f"RabbitMQ connect error: {e}")
            raise
    
    async def disconnect(self) -> None:
        try:
            await self.broker.stop()
            logger.info("RabbitMQ successfully stoped!")
        except Exception as e:
            logger.exception(f"RabbitMQ dissconect error: {e}")
        