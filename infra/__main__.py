"""An AWS Python Pulumi program"""

from iam import create_s3_full_access_iam_user
from s3 import config_aws_simple_storage_service

bucket = config_aws_simple_storage_service()
iam_user = create_s3_full_access_iam_user()
