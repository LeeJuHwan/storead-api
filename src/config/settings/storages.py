from config.env import ENV

FILE_MAX_SIZE = ENV.int("FILE_MAX_SIZE", default=10485760)


AWS_S3_ACCESS_KEY_ID = ENV("AWS_S3_ACCESS_KEY_ID", default="")
AWS_S3_SECRET_ACCESS_KEY = ENV("AWS_S3_SECRET_ACCESS_KEY", default="")
AWS_S3_REGION_NAME = ENV.str("AWS_S3_REGION_NAME", default="")
AWS_STORAGE_BUCKET_NAME = ENV.str("AWS_STORAGE_BUCKET_NAME", default="")
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
AWS_S3_URL = ENV("AWS_S3_URL", default="")

USE_S3 = ENV.bool("USE_S3", default=False)

if USE_S3:
    AWS_LOCATION = "static"
    STATIC_URL = f"https://{AWS_S3_URL}/{AWS_LOCATION}/"
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    AWS_LOCATION = "media"
    MEDIA_URL = f"https://{AWS_S3_URL}/{AWS_LOCATION}/"
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
