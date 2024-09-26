class ServiceError(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class WeatherServiceError(ServiceError):
    pass


class S3ServiceError(ServiceError):
    pass


class DynamoDBServiceError(ServiceError):
    pass
